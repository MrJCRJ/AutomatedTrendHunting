import { loadStats, computeDelta24h, saveStats, appendHistory } from '../src/server/lib/statsUtil.js';
import { validateMetrics } from '../src/server/lib/statsSchema.js';

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'GET') {
    res.status(405).json({ success: false, error: 'Method not allowed' });
    return;
  }

  const stats = loadStats();
  if (!stats) {
    return res.status(200).json({ success: true, data: { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0, delta24h: { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 }, lastUpdated: null }, stale: true });
  }
  if (stats.error) {
    return res.status(500).json({ success: false, error: 'Failed to load stats', detail: stats });
  }
  // Recalcula delta24h se ausente
  if (!stats.delta24h) {
    stats.delta24h = computeDelta24h(stats);
    stats.lastUpdated = stats.lastUpdated || new Date().toISOString();
    saveStats(stats);
    appendHistory(stats);
  }
  const validation = validateMetrics(stats);
  if (!validation.ok) {
    return res.status(500).json({ success: false, error: 'Invalid stats schema', issues: validation.errors });
  }
  return res.status(200).json({ success: true, data: validation.data });
}
