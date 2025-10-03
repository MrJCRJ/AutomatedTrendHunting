import { randomUUID } from 'crypto';

function mapErrorStatus(err) {
  switch (err.code) {
    case 'VALIDATION_ERROR': return 400;
    case 'NOT_FOUND': return 404;
    case 'UNAUTHORIZED': return 401;
    case 'FORBIDDEN': return 403;
    case 'CONFLICT': return 409;
    case 'DEPENDENCY_UNAVAILABLE': return 503;
    case 'METHOD_NOT_ALLOWED': return 405;
    default: return 500;
  }
}

function buildMeta(start, requestId) {
  return {
    requestId,
    durationMs: +(performance.now() - start).toFixed(2),
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION || 'dev'
  };
}

export function httpHandler(fn, opts = {}) {
  const { methods = ['GET'], cors = true } = opts;
  return async function handler(req, res) {
    const start = performance.now();
    const requestId = randomUUID();
    res.setHeader('X-Request-Id', requestId);

    if (cors) {
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', methods.join(','));
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      if (req.method === 'OPTIONS') return res.status(200).end();
    }

    if (!methods.includes(req.method)) {
      const meta = buildMeta(start, requestId);
      return res.status(405).json({ ok: false, data: null, error: { code: 'METHOD_NOT_ALLOWED', message: 'Method not allowed' }, meta });
    }

    try {
      const data = await fn({ req, res, requestId });
      if (res.headersSent) return;
      const meta = buildMeta(start, requestId);
      return res.status(200).json({ ok: true, data, error: null, meta });
    } catch (err) {
      const status = mapErrorStatus(err);
      const meta = buildMeta(start, requestId);
      return res.status(status).json({
        ok: false,
        data: null,
        error: { code: err.code || 'INTERNAL_ERROR', message: err.publicMessage || 'Internal error' },
        meta
      });
    }
  };
}
