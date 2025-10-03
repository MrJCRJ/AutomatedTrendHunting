// UI Fragment: bloco de pré-visualização de estatísticas
export function buildStatsPreview() {
  return `<div id="stats-preview" class="stats-preview" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:14px;margin:10px 0 22px">
    <div class="sp" data-key="totalTrends"><div class="n">-</div><div class="l">Tendências</div></div>
    <div class="sp" data-key="newslettersSent"><div class="n">-</div><div class="l">Newsletters</div></div>
    <div class="sp" data-key="revenueEstimate"><div class="n">-</div><div class="l">Receita</div></div>
  </div>`;
}
