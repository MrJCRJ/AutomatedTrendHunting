import fs from 'fs';
import path from 'path';
import { validateMetrics } from './statsSchema.js';

const DATA_DIR = path.join(process.cwd(), 'data');
const STATS_FILE = path.join(DATA_DIR, 'stats.json');
const HISTORY_FILE = path.join(DATA_DIR, 'stats-history.json');

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

export function loadStats() {
  ensureDir();
  if (!fs.existsSync(STATS_FILE)) return null;
  try {
    const raw = fs.readFileSync(STATS_FILE, 'utf-8');
    const json = JSON.parse(raw);
    const validated = validateMetrics(json);
    if (!validated.ok) {
      return { error: 'INVALID_SCHEMA', issues: validated.errors };
    }
    return validated.data;
  } catch (e) {
    return { error: 'READ_ERROR', detail: String(e) };
  }
}

export function saveStats(stats) {
  ensureDir();
  fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
}

export function appendHistory(stats) {
  ensureDir();
  const entry = { ts: new Date().toISOString(), ...stats };
  let arr = [];
  if (fs.existsSync(HISTORY_FILE)) {
    try { arr = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8')); } catch { arr = []; }
  }
  arr.push(entry);
  // Mantém só últimos 200 registros
  if (arr.length > 200) arr = arr.slice(arr.length - 200);
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(arr, null, 2));
}

export function computeDelta24h(current) {
  if (!fs.existsSync(HISTORY_FILE)) return { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 };
  try {
    const arr = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8'));
    const cutoff = Date.now() - 24 * 60 * 60 * 1000;
    const past = [...arr].reverse().find(r => new Date(r.ts).getTime() <= cutoff);
    if (!past) return { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 };
    return {
      totalTrends: current.totalTrends - past.totalTrends,
      newslettersSent: current.newslettersSent - past.newslettersSent,
      premiumSubs: current.premiumSubs - past.premiumSubs,
      revenueEstimate: current.revenueEstimate - past.revenueEstimate,
    };
  } catch {
    return { totalTrends: 0, newslettersSent: 0, premiumSubs: 0, revenueEstimate: 0 };
  }
}
