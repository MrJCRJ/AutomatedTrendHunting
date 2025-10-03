// Versão modular usando fragments movidos para src/server/ui
import { buildStyles } from '../src/server/ui/styles.js';
import { buildAuthOverlay } from '../src/server/ui/authOverlay.js';
import { buildStatsPreview } from '../src/server/ui/statsPreview.js';
import { buildActionsBar } from '../src/server/ui/actionsBar.js';
import { buildBaseScript } from '../src/server/ui/scriptBase.js';
// import { buildStatusNav } from '../src/server/ui/statusNav.js'; // Exemplo: futura inclusão de barra de status

function buildCard() {
  return `<div class="card" id="root-card">
    <h1>TrendHunter <span class="badge">Internal</span></h1>
    <p class="lead">Hub interno para coleta de tendências e distribuição multicanal. A versão pública será reativada futuramente.</p>
    <!-- Exemplo de como inserir a barra de status no futuro:
    ${'${/* buildStatusNav({ dependencies: { database: { status: "online" }, webserver: { status: "offline" } } }) */}'}
    -->
    ${buildStatsPreview()}
    ${buildActionsBar()}
    <div class="small">Modo Interno • Build Serverless</div>
  </div>`;
}

function buildHtml() {
  return `<!DOCTYPE html><html lang="pt-BR"><head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <meta name="robots" content="noindex,nofollow"/>
  <meta name="description" content="TrendHunter - Hub interno para operações de tendências e monetização"/>
  <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
  <meta name="color-scheme" content="dark light"/>
  <title>TrendHunter - Início</title>
  <style>${buildStyles()}</style>
  </head><body>
  ${buildAuthOverlay()}
  ${buildCard()}
  <script>${buildBaseScript()}</script>
  </body></html>`;
}

export default function handler(req, res) {
  const html = buildHtml();
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  return res.status(200).send(html);
}
