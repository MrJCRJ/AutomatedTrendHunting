#!/usr/bin/env node
/**
 * CLI para invocar /api/operations
 * Uso:
 *  node scripts/operations-cli.js --host https://example.com --token $METRICS_TOKEN --action monetizar
 *  node scripts/operations-cli.js -h http://localhost:3000 -t $METRICS_TOKEN -a stats-update -p '{"premiumSubs":10}'
 */

import https from 'https';
import http from 'http';

function parseArgs(argv) {
  const out = { host: '', token: process.env.METRICS_TOKEN || '', action: '', payload: null, raw: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    const next = argv[i + 1];
    switch (a) {
      case '--host':
      case '-h': out.host = next; i++; break;
      case '--token':
      case '-t': out.token = next; i++; break;
      case '--action':
      case '-a': out.action = next; i++; break;
      case '--payload':
      case '-p': out.payload = next; i++; break;
      case '--raw': out.raw = true; break;
      case '--help':
        usage();
        process.exit(0);
      default:
        if (a.startsWith('-')) console.warn('Argumento ignorado:', a);
    }
  }
  return out;
}

function usage() {
  console.log(`CLI /api/operations\n\n` +
    `Variáveis: METRICS_TOKEN pode ser usada se --token omitido.\n\n` +
    `Exemplos:\n` +
    `  node scripts/operations-cli.js -h https://api.site -a monetizar -t $METRICS_TOKEN\n` +
    `  node scripts/operations-cli.js -h https://api.site -a stats-update -p '{"revenueEstimate":55}' -t $METRICS_TOKEN\n` +
    `  node scripts/operations-cli.js -h http://localhost:3000 -a executar-tendencias -t devtoken\n`);
}

async function main() {
  const { host, token, action, payload, raw } = parseArgs(process.argv);
  if (!host || !action) {
    usage();
    process.exit(1);
  }
  if (!token) {
    console.error('Token ausente: defina --token ou METRICS_TOKEN');
    process.exit(1);
  }
  let body = { action };
  if (payload) {
    try { body.payload = JSON.parse(payload); } catch (e) { console.error('Payload JSON inválido'); process.exit(1); }
  }
  const dataStr = JSON.stringify(body);
  const lib = host.startsWith('https') ? https : http;
  const url = new URL('/api/operations', host);
  const opts = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(dataStr),
      'x-admin-token': token
    }
  };

  const started = Date.now();
  const req = lib.request(url, opts, (res) => {
    let chunks = '';
    res.on('data', d => { chunks += d; });
    res.on('end', () => {
      const ms = Date.now() - started;
      if (raw) {
        console.log(chunks);
      } else {
        try {
          const json = JSON.parse(chunks);
          console.log('\nStatus:', res.statusCode, '- Duration (client):', ms + 'ms');
          console.log(JSON.stringify(json, null, 2));
        } catch (e) {
          console.log('Resposta (raw):', chunks);
        }
      }
    });
  });
  req.on('error', (e) => {
    console.error('Erro de requisição:', e.message);
    process.exitCode = 2;
  });
  req.write(dataStr);
  req.end();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
