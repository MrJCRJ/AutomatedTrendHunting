#!/usr/bin/env node
// Script para atualizar métricas via API interna ou update direto no arquivo.
// Uso: METRICS_TOKEN=seu_token node scripts/update-stats.js --totalTrends 450 --revenueEstimate 6000

import fs from 'fs';
import path from 'path';
import https from 'https';

const args = process.argv.slice(2);
const payload = {};
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a.startsWith('--')) {
    const key = a.replace(/^--/, '');
    const val = args[i + 1];
    if (val && !val.startsWith('--')) {
      const num = Number(val);
      payload[key] = Number.isFinite(num) ? num : val;
      i++;
    } else {
      payload[key] = true;
    }
  }
}

function localUpdate() {
  const file = path.join(process.cwd(), 'data', 'stats.json');
  let current = {};
  if (fs.existsSync(file)) {
    try { current = JSON.parse(fs.readFileSync(file, 'utf-8')); } catch { current = {}; }
  }
  const merged = { ...current, ...payload, lastUpdated: new Date().toISOString() };
  fs.writeFileSync(file, JSON.stringify(merged, null, 2));
  console.log('Local stats.json atualizado:', merged);
}

async function remoteUpdate() {
  const token = process.env.METRICS_TOKEN;
  const url = process.env.METRICS_ENDPOINT || process.env.VERCEL_URL && `https://${process.env.VERCEL_URL}/api/stats-update`;
  if (!token || !url) {
    console.log('Variáveis METRICS_TOKEN ou METRICS_ENDPOINT ausentes. Fazendo update local...');
    return localUpdate();
  }
  const data = JSON.stringify(payload);
  const u = new URL(url);
  const options = {
    method: 'POST',
    hostname: u.hostname,
    path: u.pathname,
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data),
      'x-admin-token': token
    }
  };
  await new Promise((resolve) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        console.log('Resposta:', res.statusCode, body);
        resolve();
      });
    });
    req.on('error', (e) => { console.error('Erro request', e); resolve(); });
    req.write(data);
    req.end();
  });
}

remoteUpdate();
