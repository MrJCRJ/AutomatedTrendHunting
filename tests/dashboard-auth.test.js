// Testes Jest para /api/dashboard-auth
import handler from '../api/dashboard-auth.js';

function mockRes() {
  const res = {};
  res.headers = {};
  res.statusCode = 200;
  res.setHeader = (k, v) => { res.headers[k] = v; };
  res.status = (code) => { res.statusCode = code; return res; };
  res.payload = undefined;
  res.json = (obj) => { res.payload = obj; return res; };
  res.end = (data) => { res.payload = data; return res; };
  return res;
}

function run(method, { body, headers } = {}, envOverride = {}) {
  const req = { method, headers: headers || {}, body };
  const res = mockRes();
  const snapshot = { ...process.env };
  Object.assign(process.env, envOverride);
  try {
    handler(req, res);
  } finally {
    Object.keys(process.env).forEach(k => { if (!(k in snapshot)) delete process.env[k]; });
    Object.assign(process.env, snapshot);
  }
  // Se payload for string JSON, tenta parse
  if (typeof res.payload === 'string') {
    try { res.payload = JSON.parse(res.payload); } catch(_) {}
  }
  return res;
}

describe('API /api/dashboard-auth', () => {
  test('GET health responde 200 com status ok', () => {
    process.env.DASHBOARD_PASSWORD = 'X';
    const res = run('GET');
    expect(res.statusCode).toBe(200);
    expect(res.payload.success).toBe(true);
    expect(res.payload.data.status).toBe('ok');
  });

  test('POST sem senha retorna 400', () => {
    process.env.DASHBOARD_PASSWORD = 'X';
    const res = run('POST', { body: {} });
    expect(res.statusCode).toBe(400);
    expect(res.payload.success).toBe(false);
  });

  test('POST senha incorreta retorna 401', () => {
    process.env.DASHBOARD_PASSWORD = 'Segredo';
    const res = run('POST', { body: { password: 'errada' } });
    expect(res.statusCode).toBe(401);
    expect(res.payload.success).toBe(false);
  });

  test('POST senha correta retorna token', () => {
    process.env.DASHBOARD_PASSWORD = 'Segredo';
    const res = run('POST', { body: { password: 'Segredo' } });
    expect(res.statusCode).toBe(200);
    expect(res.payload.success).toBe(true);
    expect(res.payload.data.token).toMatch(/\./);
    expect(res.payload.data.expiresIn).toBe(3600);
  });

  test('Sem variável de ambiente retorna 500', () => {
    delete process.env.DASHBOARD_PASSWORD;
    const res = run('POST', { body: { password: 'qualquer' } });
    expect(res.statusCode).toBe(500);
  });

  test('Rate limiting após múltiplas tentativas inválidas', () => {
    process.env.DASHBOARD_PASSWORD = 'Segredo';
    // 5 tentativas com senha errada
    for (let i = 0; i < 5; i++) {
      const res = run('POST', { body: { password: 'errada' } });
      expect(res.statusCode).toBe(401);
    }
    // 6ª deve retornar mensagem de bloqueio (usamos 401 com mensagem Too many attempts)
    const bloqueado = run('POST', { body: { password: 'errada' } });
    expect(bloqueado.statusCode).toBe(401);
    expect(JSON.stringify(bloqueado.payload).toLowerCase()).toMatch(/too many/);
  });
});
