// Edge Runtime version of dashboard-auth
// Método: POST
// Body JSON: { password }
// Resposta: { token, expiresIn }
// Requer: DASHBOARD_PASSWORD (e opcional DASHBOARD_JWT_SECRET)
// Diferenças: Usa Web Crypto API e Response/Request padrão

export const config = { runtime: 'edge' };

async function hmacSHA256(secret, data) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(data));
  const bytes = Array.from(new Uint8Array(sig));
  return bytes.map(b => b.toString(16).padStart(2, '0')).join('');
}

function json(status, payload, headers = {}) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...headers,
    },
  });
}

const ok = (data) => json(200, { success: true, data });
const badRequest = (msg) => json(400, { success: false, error: msg });
const unauthorized = (msg) => json(401, { success: false, error: msg });
const methodNotAllowed = (methods) => json(405, { success: false, error: 'Method not allowed', allow: methods.join(', ') });
const serverError = (detail) => json(500, { success: false, error: 'Internal error', detail: String(detail) });

export default async function handler(req) {
  if (!process.env.DASHBOARD_PASSWORD) {
    return serverError('Missing environment: DASHBOARD_PASSWORD');
  }

  if (req.method === 'OPTIONS') {
    return json(204, {}, {
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
  }

  if (req.method === 'GET') {
    return ok({ status: 'ok', requires: 'POST password', expiresInSeconds: 3600, runtime: 'edge' });
  }

  if (req.method !== 'POST') {
    return methodNotAllowed(['GET', 'POST', 'OPTIONS']);
  }

  try {
    let body;
    try {
      body = await req.json();
    } catch {
      body = {};
    }
    const { password } = body;
    const expected = process.env.DASHBOARD_PASSWORD;
    if (!password) return badRequest('Missing password');
    if (password !== expected) return unauthorized('Invalid credentials');

    const secret = process.env.DASHBOARD_JWT_SECRET || expected;
    const exp = Date.now() + 1000 * 60 * 60;
    const payload = `${exp}`;
    const hmac = await hmacSHA256(secret, payload);
    const token = `${exp}.${hmac}`;
    return ok({ token, expiresIn: 3600 });
  } catch (e) {
    return serverError(e);
  }
}
