// Endpoint: POST /api/monetizar
// Objetivo: simular distribuição/monetização e atualizar métricas

import { loadStats, saveStats, computeDelta24h, appendHistory } from './_lib/statsUtil.js';
import { validateMetrics } from './_lib/statsSchema.js';

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  const current = loadStats();
  if (current && current.error) {
    return res.status(500).json({ success: false, error: 'Failed to load current stats', detail: current });
  }
  const base = current && !current.error ? current : { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 };

  // Simulação: +1 newsletter, receita estimada +5.00
  const updated = {
    totalTrends: base.totalTrends,
    newslettersSent: base.newslettersSent + 1,
    premiumSubs: base.premiumSubs,
    revenueEstimate: parseFloat((base.revenueEstimate + 5).toFixed(2)),
    lastUpdated: new Date().toISOString()
  };
  updated.delta24h = computeDelta24h(updated);

  const validation = validateMetrics(updated);
  if (!validation.ok) {
    return res.status(500).json({ success: false, error: 'Validation failed', issues: validation.errors });
  }

  saveStats(validation.data);
  appendHistory(validation.data);

  return res.status(200).json({ success: true, data: validation.data, increment: { newsletters: +1, revenue: +5 } });
}
