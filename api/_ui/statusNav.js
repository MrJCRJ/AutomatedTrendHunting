// Fragmento UI: StatusNav inspirado no padrão React mostrado pelo usuário.
// Uso: buildStatusNav({ dependencies: { database: { status: 'online' }, webserver: { status: 'offline' } } }, { compact: false })
// Retorna HTML string.

const STATUS_COLORS = {
  online: '#40c057',
  ok: '#40c057',
  up: '#40c057',
  warning: '#ffd43b',
  degraded: '#ffd43b',
  offline: '#fa5252',
  down: '#fa5252',
  error: '#fa5252'
};

function dot(status) {
  const color = STATUS_COLORS[status] || '#999';
  return `<span class="status-nav-dot" style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color}"></span>`;
}

export function buildStatusNav(statusObj, opts = {}) {
  if (!statusObj || !statusObj.dependencies) {
    return '<p class="status-nav-error">Não foi possível carregar os dados.</p>';
  }
  const { dependencies } = statusObj;
  const compact = !!opts.compact;
  const items = [
    { id: 'database', label: compact ? 'DB' : 'Banco de Dados', data: dependencies.database },
    { id: 'webserver', label: compact ? 'WS' : 'Web Server', data: dependencies.webserver }
  ].filter(i => i.data);

  return `<div class="status-nav">${items.map(item => `
    <div class="status-nav-item">
      ${dot(item.data.status)}
      <span class="status-nav-label">${item.label}</span>
    </div>`).join('')}
  </div>`;
}
