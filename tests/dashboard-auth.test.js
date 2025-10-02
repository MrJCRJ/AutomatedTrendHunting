// Teste inicial para handler dashboard-auth
// Requer Node >=18

import assert from 'assert';
import { ok as httpOk } from 'node:assert';
import handler from '../api/dashboard-auth.js';

function mockRes() {
  return {
    statusCode: 0,
    headers: {},
    body: '',
    setHeader(k, v) { this.headers[k] = v; },
    end(payload) { this.body = payload; },
  };
}

function runHandler(method, body, env = {}) {
  const req = { method, body };
  const res = mockRes();
  const prev = { ...process.env };
  Object.assign(process.env, env);
  try {
    handler(req, res);
  } finally {
    process.env = prev;
  }
  return res;
}

// Simples execução manual (não usando jest/mocha por enquanto)
(function () {
  const resGet = runHandler('GET', null);
  assert.strictEqual(resGet.statusCode, 200, 'GET deve retornar 200');

  const resNoEnv = runHandler('POST', { password: 'x' });
  assert.strictEqual(resNoEnv.statusCode, 500, 'Sem env deve falhar 500');

  const password = 'segredo';
  const resBad = runHandler('POST', { password: 'errado' }, { DASHBOARD_PASSWORD: password });
  assert.strictEqual(resBad.statusCode, 401, 'Senha errada deve retornar 401');

  const resOk = runHandler('POST', { password }, { DASHBOARD_PASSWORD: password });
  assert.strictEqual(resOk.statusCode, 200, 'Senha correta deve retornar 200');

  console.log('dashboard-auth.test.js OK');
})();
