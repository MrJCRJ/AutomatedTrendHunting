// Serverless function: /api/dashboard-auth
// Método: POST
// Body: { password: string }
// Resposta: { token, expiresIn }
// Requer variável de ambiente: DASHBOARD_PASSWORD
// (Opcional) DASHBOARD_JWT_SECRET para assinatura mais forte

import crypto from 'crypto';

export default function handler(req, res) {
  // Headers básicos (simples; se precisar ampliar para CORS avançado ajustar aqui)
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');

  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method === 'GET') {
    // Health check simples
    return res.status(200).json({ status: 'ok', requires: 'POST password', expiresInSeconds: 3600 });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
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

    if (!expected) {
      return res.status(500).json({ error: 'Dashboard password not configured' });
    }

    if (!password) {
      return res.status(400).json({ error: 'Missing password' });
    }

    if (password !== expected) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Gera token simples (HMAC + timestamp)
    const secret = process.env.DASHBOARD_JWT_SECRET || expected;
    const exp = Date.now() + 1000 * 60 * 60; // 1h
    const payload = `${exp}`;
    const hmac = crypto.createHmac('sha256', secret).update(payload).digest('hex');
    const token = `${exp}.${hmac}`;

    return res.status(200).json({ token, expiresIn: 3600 });
  } catch (e) {
    return res.status(500).json({ error: 'Internal error', detail: String(e) });
  }
}
