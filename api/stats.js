import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method !== 'GET') {
    res.status(405).json({ success: false, error: 'Method not allowed' });
    return;
  }

  try {
    const filePath = path.join(process.cwd(), 'data', 'stats.json');
    if (!fs.existsSync(filePath)) {
      return res.status(200).json({ success: true, data: { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0, lastUpdated: null }, stale: true });
    }
    const raw = fs.readFileSync(filePath, 'utf-8');
    const data = JSON.parse(raw);
    return res.status(200).json({ success: true, data });
  } catch (e) {
    return res.status(500).json({ success: false, error: 'Failed to load stats', detail: String(e) });
  }
}
