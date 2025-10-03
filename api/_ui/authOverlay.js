// UI Fragment: overlay de autenticação reutilizável
export function buildAuthOverlay() {
  return `<div id="auth-overlay"><div id="auth-box">
  <h2>🔒 Acesso Restrito</h2>
  <p>Ambiente interno. Autentique-se para acessar o painel e ações.</p>
  <form id="auth-form">
    <input id="auth-password" type="password" placeholder="Senha" autocomplete="current-password" />
    <button type="submit">Entrar</button>
    <div id="auth-error"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:-4px">
      <label class="rem"><input id="remember-session" type="checkbox"/>Manter logado</label>
      <button type="button" class="clear-session" id="clear-session">Limpar</button>
    </div>
  </form>
  <div class="info">Auth: POST <code>/api/dashboard-auth</code></div>
</div></div>`;
}
