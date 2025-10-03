// Endpoint unificado: POST /api/operations
// Body: { action: string, payload?: any }
// Ações suportadas:
// - executar-tendencias
// - monetizar
// - stats-update
// Autenticação simples: header x-admin-token (mesma lógica de stats-update) para TODAS as ações mutáveis.

import { httpHandler } from '../src/server/core/httpHandler.js';
import { loadStats, saveStats, computeDelta24h, appendHistory } from './_lib/statsUtil.js';
import { validateMetrics } from './_lib/statsSchema.js';

function requireToken(req) {
  const token = req.headers['x-admin-token'];
  if (!process.env.METRICS_TOKEN || token !== process.env.METRICS_TOKEN) {
    const err = new Error('Unauthorized');
    err.code = 'UNAUTHORIZED';
    throw err;
  }
}

function baseStatsOrDefault() {
  const current = loadStats();
  if (current && current.error) {
    const err = new Error('Failed to load current stats');
    err.code = 'DEPENDENCY_UNAVAILABLE';
    throw err;
  }
  if (!current || current.error) {
    return { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 };
  }
  return current;
}

function validateAndPersist(updated, extra = {}) {
  updated.delta24h = computeDelta24h(updated);
  const validation = validateMetrics(updated);
  if (!validation.ok) {
    const err = new Error('Invalid payload');
    err.code = 'VALIDATION_ERROR';
    err.publicMessage = 'Validation failed';
    err.detail = validation.errors;
    throw err;
  }
  saveStats(validation.data);
  appendHistory(validation.data);
  return { stats: validation.data, ...extra };
}

async function operationsHandler({ req }) {
  if (req.method !== 'POST') {
    const err = new Error('Method not allowed');
    err.code = 'METHOD_NOT_ALLOWED';
    throw err;
  }

  let body = req.body;
  if (!body || typeof body !== 'object') {
    try { body = JSON.parse(req.body || '{}'); } catch { body = {}; }
  }
  const { action, payload = {} } = body;
  if (!action) {
    const err = new Error('Missing action');
    err.code = 'VALIDATION_ERROR';
    err.publicMessage = 'Missing action field';
    throw err;
  }

  // Requer token para qualquer mutação
  requireToken(req);

  // Switch das ações
  switch (action) {
    case 'executar-tendencias': {
      const base = baseStatsOrDefault();
      const inc = 1 + Math.floor(Math.random() * 3);
      const updated = {
        totalTrends: base.totalTrends + inc,
        newslettersSent: base.newslettersSent,
        premiumSubs: base.premiumSubs,
        revenueEstimate: base.revenueEstimate,
        lastUpdated: new Date().toISOString()
      };
      return validateAndPersist(updated, { increment: { totalTrends: inc } });
    }
    case 'monetizar': {
      const base = baseStatsOrDefault();
      const updated = {
        totalTrends: base.totalTrends,
        newslettersSent: base.newslettersSent + 1,
        premiumSubs: base.premiumSubs,
        revenueEstimate: parseFloat((base.revenueEstimate + 5).toFixed(2)),
        lastUpdated: new Date().toISOString()
      };
      return validateAndPersist(updated, { increment: { newsletters: 1, revenue: 5 } });
    }
    case 'stats-update': {
      const base = baseStatsOrDefault();
      const updated = {
        totalTrends: payload.totalTrends ?? base.totalTrends,
        newslettersSent: payload.newslettersSent ?? base.newslettersSent,
        premiumSubs: payload.premiumSubs ?? base.premiumSubs,
        revenueEstimate: payload.revenueEstimate ?? base.revenueEstimate,
        lastUpdated: new Date().toISOString()
      };
      return validateAndPersist(updated);
    }
    default: {
      const err = new Error('Unknown action');
      err.code = 'NOT_FOUND';
      err.publicMessage = 'Action not supported';
      throw err;
    }
  }
}

export default httpHandler(operationsHandler, { methods: ['POST'] });
