// Serverless function: /api/dashboard-auth
// Método: POST
// Body: { password: string }
// Resposta: { token, expiresIn }
// Requer variável de ambiente: DASHBOARD_PASSWORD
// (Opcional) DASHBOARD_JWT_SECRET para assinatura mais forte

import crypto from 'crypto';
import { ok, badRequest, unauthorized, methodNotAllowed, serverError } from './_lib/apiResponse.js';

// Rate limiting em memória (MVP). Importante: em ambiente serverless múltiplas instâncias
// não compartilham esse mapa. Aceitável para fase inicial.
const rateMap = new Map(); // chave: ip => { attempts: number, first: timestamp }
const MAX_ATTEMPTS = 5;
const WINDOW_MS = 5 * 60 * 1000; // 5 minutos

function rateLimited(ip) {
  const now = Date.now();
  const entry = rateMap.get(ip);
  if (!entry) {
    rateMap.set(ip, { attempts: 1, first: now });
    return false;
  }
  if (now - entry.first > WINDOW_MS) {
    // janela expirada - reset
    rateMap.set(ip, { attempts: 1, first: now });
    return false;
  }
  entry.attempts += 1;
  if (entry.attempts > MAX_ATTEMPTS) return true;
  return false;
}

export default function handler(req, res) {
  // Headers básicos (simples; se precisar ampliar para CORS avançado ajustar aqui)
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');

  // Validação antecipada de ambiente essencial
  if (!process.env.DASHBOARD_PASSWORD) {
    return serverError(res, 'Missing environment: DASHBOARD_PASSWORD');
  }

  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method === 'GET') {
    return ok(res, { status: 'ok', requires: 'POST password', expiresInSeconds: 3600 });
  }

  if (req.method !== 'POST') {
    return methodNotAllowed(res, ['GET', 'POST', 'OPTIONS']);
  }

  try {
    // Verificação básica de rate limit (apenas em POST auth attempts)
    const ip = (req.headers['x-forwarded-for'] || req.connection?.remoteAddress || req.socket?.remoteAddress || 'unknown').toString().split(',')[0].trim();
    if (req.method === 'POST') {
      if (rateLimited(ip)) {
        res.setHeader('Retry-After', '300'); // 5 minutos
        return unauthorized(res, 'Too many attempts. Try again later.');
      }
    }
    let body = req.body;
    if (!body || typeof body !== 'object') {
      // Tenta parse manual se vier string
      try {
        body = JSON.parse(req.body || '{}');
      } catch (_) {
        body = {};
      }
    }
    const { password } = body;
    const expected = process.env.DASHBOARD_PASSWORD;

    if (!password) {
      return badRequest(res, 'Missing password');
    }

    if (password !== expected) {
      return unauthorized(res, 'Invalid credentials');
    }

    // Gera token simples (HMAC + timestamp)
    const secret = process.env.DASHBOARD_JWT_SECRET || expected;
    const exp = Date.now() + 1000 * 60 * 60; // 1h
    const payload = `${exp}`;
    const hmac = crypto.createHmac('sha256', secret).update(payload).digest('hex');
    const token = `${exp}.${hmac}`;

    return ok(res, { token, expiresIn: 3600 });
  } catch (e) {
    return serverError(res, e);
  }
}
