// Testes para /api/monetizar
import handler from '../api/monetizar.js';
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

function run(method) {
  const req = { method, headers: {}, body: {} };
  const res = mockRes();
  handler(req, res);
  return res;
}

const dataFile = path.join(process.cwd(), 'data', 'stats.json');

beforeEach(() => {
  try { fs.unlinkSync(dataFile); } catch (e) { }
  fs.mkdirSync(path.dirname(dataFile), { recursive: true });
  fs.writeFileSync(dataFile, JSON.stringify({ totalTrends: 2, newslettersSent: 5, premiumSubs: 1, revenueEstimate: 10, lastUpdated: new Date().toISOString() }));
});

describe('API /api/monetizar', () => {
  test('Rejeita métodos não-POST', () => {
    const res = run('GET');
    expect(res.statusCode).toBe(405);
  });

  test('Incrementa newslettersSent e revenueEstimate corretamente', () => {
    const before = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
    const res = run('POST');
    expect(res.statusCode).toBe(200);
    expect(res.payload.increment).toEqual({ newsletters: 1, revenue: 5 });
    const data = res.payload.data;
    expect(data.newslettersSent).toBe(before.newslettersSent + 1);
    expect(data.revenueEstimate).toBeCloseTo(before.revenueEstimate + 5, 5);
  });
});
