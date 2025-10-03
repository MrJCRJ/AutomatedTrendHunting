// UI Fragment: barra de ações
export function buildActionsBar(){
  return `<div class="actions">
    <a class="btn primary" href="/api/dashboard" rel="nofollow">Ir para o Dashboard</a>
    <button class="btn secondary" id="btn-trends">Executar Tendências</button>
    <button class="btn secondary" id="btn-monet">Executar Monetização</button>
    <button class="btn danger" id="btn-refresh">↻ Stats</button>
  </div>`;
}
