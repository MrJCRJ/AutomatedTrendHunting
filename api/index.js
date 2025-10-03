// Refatorado para facilitar manutenção: seções nomeadas e composição clara.

function buildStyles() {
  return `:root{--grad:linear-gradient(135deg,#667eea 0%,#764ba2 100%);--bg-panel:#1f1f2e;--accent:#667eea;--accent-hover:#5a6fd8;--danger:#d63939;--ok:#40c057;--warn:#ffd43b;--font:Segoe UI,Tahoma,sans-serif}
body{font-family:var(--font);background:var(--grad);margin:0;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:30px}
.card{background:var(--bg-panel);border-radius:22px;padding:46px 50px;max-width:680px;width:100%;box-shadow:0 18px 50px -12px rgba(0,0,0,.55);position:relative;overflow:hidden}
.card:before{content:"";position:absolute;inset:0;background:linear-gradient(145deg,rgba(255,255,255,.06),rgba(255,255,255,0));pointer-events:none}
h1{margin:0 0 10px;font-size:2.15rem;letter-spacing:.5px;display:flex;gap:.55rem;align-items:center}
h1 span.badge{background:#2d2d44;padding:4px 10px;border-radius:40px;font-size:.55rem;letter-spacing:.7px;text-transform:uppercase;position:relative;top:-2px}
p.lead{margin:0 0 22px;line-height:1.55;color:#e5e5f0;font-size:.92rem}
.actions{display:flex;flex-wrap:wrap;gap:14px;margin-top:10px}
a.btn,button.btn{border:none;border-radius:10px;padding:12px 20px;font-weight:600;cursor:pointer;font-size:.8rem;letter-spacing:.5px;display:inline-flex;align-items:center;gap:6px;text-decoration:none;transition:.25s}
.primary{background:var(--accent);color:#fff}
.secondary{background:#2d2d44;color:#fff}
.danger{background:#3a1f27;color:#ffb3c1}
.primary:hover{background:var(--accent-hover);transform:translateY(-2px)}
.secondary:hover{background:#373755;transform:translateY(-2px)}
.danger:hover{background:#4a2731;transform:translateY(-2px)}
.small{font-size:.65rem;opacity:.75;margin-top:25px;letter-spacing:.5px}
#auth-overlay{position:fixed;inset:0;background:rgba(10,10,18,.92);display:flex;align-items:center;justify-content:center;z-index:9999}
#auth-box{background:#fff;color:#222;max-width:360px;width:100%;padding:34px 38px;border-radius:18px;box-shadow:0 10px 40px -8px rgba(0,0,0,.45);font-family:system-ui;position:relative}
#auth-box h2{margin:0 0 10px;font-size:1.25rem;display:flex;align-items:center;gap:.5rem}
#auth-box p{margin:0 0 16px;font-size:.7rem;color:#555;line-height:1.45}
#auth-form{display:flex;flex-direction:column;gap:.75rem}
#auth-form input{padding:.8rem .9rem;border:2px solid #e4e6ef;border-radius:10px;font-size:.82rem;letter-spacing:.3px}
#auth-form button{background:#667eea;color:#fff;border:none;padding:.8rem .9rem;font-weight:600;border-radius:10px;font-size:.8rem;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:.4rem;box-shadow:0 4px 14px -3px rgba(102,126,234,.55);transition:.25s}
#auth-form button:hover{background:#5a6fd8}
#auth-error{min-height:16px;font-size:.6rem;color:#d63939;font-weight:500}
label.rem{display:flex;align-items:center;gap:.35rem;font-size:.55rem;color:#666;letter-spacing:.5px;text-transform:uppercase;font-weight:600}
button.clear-session{background:none;border:none;color:#888;font-size:.55rem;cursor:pointer;text-transform:uppercase;letter-spacing:.5px}
.info{margin-top:.9rem;padding:.55rem .65rem;background:#f5f7ff;border:1px solid #e3e9ff;border-radius:8px;font-size:.55rem;line-height:1.25;color:#4a4f63}
@media (max-width:620px){.card{padding:34px}body{padding:18px}h1{font-size:1.7rem}}`;
}

function buildAuthOverlay() {
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

function buildStatsPreview() {
  return `<div id="stats-preview" class="stats-preview" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:14px;margin:10px 0 22px">
    <div class="sp" data-key="totalTrends"><div class="n">-</div><div class="l">Tendências</div></div>
    <div class="sp" data-key="newslettersSent"><div class="n">-</div><div class="l">Newsletters</div></div>
    <div class="sp" data-key="revenueEstimate"><div class="n">-</div><div class="l">Receita</div></div>
  </div>`;
}

function buildActions() {
  return `<div class="actions">
    <a class="btn primary" href="/api/dashboard" rel="nofollow">Ir para o Dashboard</a>
    <button class="btn secondary" id="btn-trends">Executar Tendências</button>
    <button class="btn secondary" id="btn-monet">Executar Monetização</button>
    <button class="btn danger" id="btn-refresh">↻ Stats</button>
  </div>`;
}

function buildCard() {
  return `<div class="card" id="root-card">
    <h1>TrendHunter <span class="badge">Internal</span></h1>
    <p class="lead">Hub interno para coleta de tendências e distribuição multicanal. A versão pública será reativada futuramente.</p>
    ${buildStatsPreview()}
    ${buildActions()}
    <div class="small">Modo Interno • Build Serverless</div>
  </div>`;
}

function buildScript() {
  return `<script>(function(){
    const QS=(s,p=document)=>p.querySelector(s);const QSA=(s,p=document)=>[...p.querySelectorAll(s)];
    const overlay=QS('#auth-overlay'),form=QS('#auth-form'),pw=QS('#auth-password'),err=QS('#auth-error'),remember=QS('#remember-session'),clearBtn=QS('#clear-session'),K='dashboardAuthToken',KE='dashboardAuthExp';
    const btnTrends=QS('#btn-trends'),btnMonet=QS('#btn-monet'),btnRefresh=QS('#btn-refresh'),statsWrap=QS('#stats-preview');
    function getToken(){return localStorage.getItem(K)||sessionStorage.getItem(K)||null}
    function hasValid(){const t=getToken();if(!t)return false;const exp=parseInt(localStorage.getItem(KE)||sessionStorage.getItem(KE)||'0',10);if(Date.now()>exp){[localStorage,sessionStorage].forEach(s=>{s.removeItem(K);s.removeItem(KE)});return false}return t.split('.').length===2}
    function unlock(){overlay.style.opacity='0';overlay.style.pointerEvents='none';setTimeout(()=>overlay.remove(),320);loadStats();}
    async function auth(password){const resp=await fetch('/api/dashboard-auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password})});const data=await resp.json();if(!resp.ok)throw new Error(data.error||'Falha');const store=remember.checked?localStorage:sessionStorage;store.setItem(K,data.token);store.setItem(KE,(Date.now()+data.expiresIn*1000).toString());return true}
    function tokenHeader(){const t=getToken();return t?{'X-Dashboard-Token':t}:{}}
    async function loadStats(){if(!statsWrap) return;statsWrap.classList.add('loading');try{const r=await fetch('/api/stats',{headers:tokenHeader()});if(!r.ok)throw 0;const j=await r.json();if(!j||!j.data)return;QSA('.sp',statsWrap).forEach(el=>{const key=el.getAttribute('data-key');const num=el.querySelector('.n');let val=j.data[key];if(key==='revenueEstimate') val='R$ '+Number(val).toFixed(2);num.textContent=val;});}catch(e){console.warn('Falha stats',e);}finally{statsWrap.classList.remove('loading');}}
    async function exec(endpoint, btn){if(!btn)return;btn.disabled=true;const original=btn.textContent;btn.textContent='...';try{const r=await fetch(endpoint,{method:'POST',headers:tokenHeader()});if(r.ok){loadStats();}else{console.warn('Falha op',endpoint);} }finally{btn.textContent=original;btn.disabled=false;}}
    if(hasValid())unlock();
    form.addEventListener('submit',async ev=>{ev.preventDefault();err.textContent='';const value=pw.value.trim();if(!value){err.textContent='Informe a senha';return}const btn=form.querySelector('button[type=submit]');btn.disabled=true;btn.style.opacity='.6';try{await auth(value);unlock();}catch(e){err.textContent=e.message}finally{btn.disabled=false;btn.style.opacity='1';}});
    clearBtn.addEventListener('click',()=>{[localStorage,sessionStorage].forEach(s=>{s.removeItem(K);s.removeItem(KE)});err.style.color='#1f6feb';err.textContent='Sessão limpa';pw.focus();});
    btnTrends.addEventListener('click',()=>exec('/api/executar-tendencias',btnTrends));
    btnMonet.addEventListener('click',()=>exec('/api/monetizar',btnMonet));
    btnRefresh.addEventListener('click',()=>loadStats());
  })();</script>`;
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
  ${buildScript()}
  </body></html>`;
}

export default function handler(req, res) {
  const html = buildHtml();
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  return res.status(200).send(html);
}
