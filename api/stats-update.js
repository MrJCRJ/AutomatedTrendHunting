// Endpoint protegido para atualizar métricas.
// Proteção simples via header x-admin-token comparando com process.env.METRICS_TOKEN

import { loadStats, saveStats, computeDelta24h, appendHistory } from './_lib/statsUtil.js';
import { validateMetrics } from './_lib/statsSchema.js';

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'POST') {
    res.status(405).json({ success: false, error: 'Method not allowed' });
    return;
  }

  const token = req.headers['x-admin-token'];
  if (!process.env.METRICS_TOKEN || token !== process.env.METRICS_TOKEN) {
    return res.status(401).json({ success: false, error: 'Unauthorized' });
  }

  let body = req.body;
  if (!body || typeof body !== 'object') {
    try { body = JSON.parse(req.body || '{}'); } catch { body = {}; }
  }

  const current = loadStats();
  if (current && current.error) {
    return res.status(500).json({ success: false, error: 'Failed to load current stats', detail: current });
  }

  const updated = {
    totalTrends: body.totalTrends ?? (current?.totalTrends || 0),
    newslettersSent: body.newslettersSent ?? (current?.newslettersSent || 0),
    premiumSubs: body.premiumSubs ?? (current?.premiumSubs || 0),
    revenueEstimate: body.revenueEstimate ?? (current?.revenueEstimate || 0),
    lastUpdated: new Date().toISOString()
  };
  // Recalcula delta24h após merge
  updated.delta24h = computeDelta24h(updated);

  const validation = validateMetrics(updated);
  if (!validation.ok) {
    return res.status(400).json({ success: false, error: 'Invalid payload', issues: validation.errors });
  }

  saveStats(updated);
  appendHistory(updated);

  return res.status(200).json({ success: true, data: validation.data });
}
