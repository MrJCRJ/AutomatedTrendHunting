// Serverless function: /api/dashboard-auth
// Método: POST
// Body: { password: string }
// Resposta: { token, expiresIn }
// Requer variável de ambiente: DASHBOARD_PASSWORD
// (Opcional) DASHBOARD_JWT_SECRET para assinatura mais forte

import crypto from 'crypto';

export default function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { password } = req.body || {};
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
