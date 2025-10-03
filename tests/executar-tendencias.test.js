// Testes para /api/executar-tendencias
import handler from '../api/executar-tendencias.js';
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
  // Limpa arquivo de stats para previsibilidade
  try { fs.unlinkSync(dataFile); } catch(e) {}
  fs.mkdirSync(path.dirname(dataFile), { recursive: true });
  fs.writeFileSync(dataFile, JSON.stringify({ totalTrends:0, newslettersSent:0, premiumSubs:0, revenueEstimate:0, lastUpdated:new Date().toISOString() }));
});

describe('API /api/executar-tendencias', () => {
  test('Rejeita métodos não-POST', () => {
    const res = run('GET');
    expect(res.statusCode).toBe(405);
  });

  test('Incrementa totalTrends entre 1 e 3', () => {
    const before = JSON.parse(fs.readFileSync(dataFile,'utf-8'));
    const res = run('POST');
    expect(res.statusCode).toBe(200);
    const inc = res.payload.increment;
    expect([1,2,3]).toContain(inc);
    const after = res.payload.data.totalTrends;
    expect(after - before.totalTrends).toBe(inc);
  });
});
