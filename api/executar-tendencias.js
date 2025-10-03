// Endpoint: POST /api/executar-tendencias
// Objetivo: simular processamento de tendências e atualizar stats
// Requer persistência simples via statsUtil

import { loadStats, saveStats, computeDelta24h, appendHistory } from './_lib/statsUtil.js';
import { validateMetrics } from './_lib/statsSchema.js';

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  // Carrega stats atuais
  const current = loadStats();
  if (current && current.error) {
    return res.status(500).json({ success: false, error: 'Failed to load current stats', detail: current });
  }
  const base = current && !current.error ? current : { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 };

  // Simulação: incrementa entre 1 e 3 tendências
  const inc = 1 + Math.floor(Math.random() * 3);
  const updated = {
    totalTrends: base.totalTrends + inc,
    newslettersSent: base.newslettersSent,
    premiumSubs: base.premiumSubs,
    revenueEstimate: base.revenueEstimate,
    lastUpdated: new Date().toISOString()
  };
  updated.delta24h = computeDelta24h(updated);

  const validation = validateMetrics(updated);
  if (!validation.ok) {
    return res.status(500).json({ success: false, error: 'Validation failed', issues: validation.errors });
  }

  saveStats(validation.data);
  appendHistory(validation.data);

  return res.status(200).json({ success: true, data: validation.data, increment: inc });
}
