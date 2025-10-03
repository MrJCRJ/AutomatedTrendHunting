// Versão modular usando fragments em api/_ui
import { buildStyles } from './_ui/styles.js';
import { buildAuthOverlay } from './_ui/authOverlay.js';
import { buildStatsPreview } from './_ui/statsPreview.js';
import { buildActionsBar } from './_ui/actionsBar.js';
import { buildBaseScript } from './_ui/scriptBase.js';

function buildCard(){
  return `<div class="card" id="root-card">
    <h1>TrendHunter <span class="badge">Internal</span></h1>
    <p class="lead">Hub interno para coleta de tendências e distribuição multicanal. A versão pública será reativada futuramente.</p>
    ${buildStatsPreview()}
    ${buildActionsBar()}
    <div class="small">Modo Interno • Build Serverless</div>
  </div>`;
}

function buildHtml(){
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

export default function handler(req,res){
  const html = buildHtml();
  res.setHeader('Content-Type','text/html; charset=utf-8');
  res.setHeader('Cache-Control','no-store');
  return res.status(200).send(html);
}
