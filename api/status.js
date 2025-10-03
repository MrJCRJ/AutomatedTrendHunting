import { httpHandler } from '../src/server/core/httpHandler.js';
import { loadStats } from '../src/server/lib/statsUtil.js';

async function statusHandler() {
  // Usa stats como proxy de saúde (ex: arquivo legível)
  let statsOk = false;
  try {
    const stats = loadStats();
    statsOk = !!stats && !stats.error;
  } catch {
    statsOk = false;
  }
  const databaseDep = { status: statsOk ? 'healthy' : 'unknown' };
  const webserverDep = { status: 'healthy', environment: process.env.NODE_ENV || 'development' };
  const statuses = [databaseDep.status, webserverDep.status];
  let overall = 'healthy';
  if (statuses.some(s => ['unreachable', 'offline', 'error'].includes(s))) overall = 'offline';
  else if (statuses.some(s => s !== 'healthy')) overall = 'degraded';
  return {
    pong: true,
    time: Date.now(),
    dependencies: { database: databaseDep, webserver: webserverDep, overall }
  };
}

export default httpHandler(statusHandler, { methods: ['GET'] });
