// Testes para /api/operations action stats-update
import handler from '../api/operations.js';
import fs from 'fs';
import path from 'path';

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

async function run(method, body = {}) {
  const req = { method, headers: { 'x-admin-token': 'TEST' }, body };
  const res = mockRes();
  await handler(req, res);
  return res;
}

const dataFile = path.join(process.cwd(), 'data', 'stats.json');

beforeEach(() => {
  try { fs.unlinkSync(dataFile); } catch (e) { }
  fs.mkdirSync(path.dirname(dataFile), { recursive: true });
  fs.writeFileSync(dataFile, JSON.stringify({ totalTrends: 10, newslettersSent: 3, premiumSubs: 2, revenueEstimate: 50, lastUpdated: new Date().toISOString() }));
  process.env.METRICS_TOKEN = 'TEST';
});

describe('API /api/operations action stats-update', () => {
  test('Rejeita métodos não-POST', async () => {
    const res = await run('GET');
    expect(res.statusCode).toBe(405);
    expect(res.payload.ok).toBe(false);
    expect(res.payload.error.code).toBe('METHOD_NOT_ALLOWED');
  });

  test('Retorna 401 sem token', async () => {
    const req = { method: 'POST', headers: {}, body: { action: 'stats-update', payload: { totalTrends: 11 } } };
    const res = mockRes();
    await handler(req, res);
    expect(res.statusCode).toBe(401);
    expect(res.payload.ok).toBe(false);
  });

  test('Atualiza parcialmente métricas', async () => {
    const before = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
    const res = await run('POST', { action: 'stats-update', payload: { totalTrends: before.totalTrends + 5 } });
    expect(res.statusCode).toBe(200);
    expect(res.payload.ok).toBe(true);
    expect(res.payload.data.stats.totalTrends).toBe(before.totalTrends + 5);
    // Campos não enviados devem permanecer
    expect(res.payload.data.stats.newslettersSent).toBe(before.newslettersSent);
  });

  test('Falha validação com valor negativo', async () => {
    const res = await run('POST', { action: 'stats-update', payload: { totalTrends: -1 } });
    expect(res.statusCode).toBe(400);
    expect(res.payload.ok).toBe(false);
    expect(res.payload.error.code).toBe('VALIDATION_ERROR');
  });
});
