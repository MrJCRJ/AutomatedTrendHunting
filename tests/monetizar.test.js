// Testes para /api/monetizar
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
  fs.writeFileSync(dataFile, JSON.stringify({ totalTrends: 2, newslettersSent: 5, premiumSubs: 1, revenueEstimate: 10, lastUpdated: new Date().toISOString() }));
  process.env.METRICS_TOKEN = 'TEST';
});

describe('API /api/monetizar', () => {
  test('Rejeita métodos não-POST', async () => {
    const res = await run('GET');
    expect(res.statusCode).toBe(405);
    expect(res.payload.ok).toBe(false);
    expect(res.payload.error.code).toBe('METHOD_NOT_ALLOWED');
  });

  test('Incrementa newslettersSent e revenueEstimate via action monetizar', async () => {
    const before = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
    const res = await run('POST', { action: 'monetizar' });
    expect(res.statusCode).toBe(200);
    expect(res.payload.ok).toBe(true);
    expect(res.payload.data.increment).toEqual({ newsletters: 1, revenue: 5 });
    const stats = res.payload.data.stats;
    expect(stats.newslettersSent).toBe(before.newslettersSent + 1);
    expect(stats.revenueEstimate).toBeCloseTo(before.revenueEstimate + 5, 5);
  });
});
