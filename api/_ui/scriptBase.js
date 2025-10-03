// UI Fragment: script base de interatividade para index/dashboard minimalista
export function buildBaseScript() {
  return `(function(){
    const QS=(s,p=document)=>p.querySelector(s);const QSA=(s,p=document)=>[...p.querySelectorAll(s)];
    const overlay=QS('#auth-overlay'),form=QS('#auth-form'),pw=QS('#auth-password'),err=QS('#auth-error'),remember=QS('#remember-session'),clearBtn=QS('#clear-session'),K='dashboardAuthToken',KE='dashboardAuthExp';
    const btnTrends=QS('#btn-trends'),btnMonet=QS('#btn-monet'),btnRefresh=QS('#btn-refresh'),statsWrap=QS('#stats-preview');
    function getToken(){return localStorage.getItem(K)||sessionStorage.getItem(K)||null}
    function hasValid(){const t=getToken();if(!t)return false;const exp=parseInt(localStorage.getItem(KE)||sessionStorage.getItem(KE)||'0',10);if(Date.now()>exp){[localStorage,sessionStorage].forEach(s=>{s.removeItem(K);s.removeItem(KE)});return false}return t.split('.').length===2}
    function unlock(){overlay.style.opacity='0';overlay.style.pointerEvents='none';setTimeout(()=>overlay.remove(),320);loadStats();}
    async function auth(password){const resp=await fetch('/api/dashboard-auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password})});const data=await resp.json();if(!resp.ok)throw new Error(data.error||'Falha');const store=remember.checked?localStorage:sessionStorage;store.setItem(K,data.token);store.setItem(KE,(Date.now()+data.expiresIn*1000).toString());return true}
    function tokenHeader(){const t=getToken();return t?{'X-Dashboard-Token':t}:{}}
    async function loadStats(){if(!statsWrap) return;statsWrap.classList.add('loading');try{const r=await fetch('/api/stats',{headers:tokenHeader()});if(!r.ok)throw 0;const j=await r.json();if(!j||!j.data)return;QSA('.sp',statsWrap).forEach(el=>{const key=el.getAttribute('data-key');const num=el.querySelector('.n');let val=j.data[key];if(key==='revenueEstimate') val='R$ '+Number(val).toFixed(2);num.textContent=val;});}catch(e){console.warn('Falha stats',e);}finally{statsWrap.classList.remove('loading');}}
  async function execAction(action, btn, extraPayload={}){if(!btn)return;btn.disabled=true;const original=btn.textContent;btn.textContent='...';try{const r=await fetch('/api/operations',{method:'POST',headers:{'Content-Type':'application/json',...tokenHeader()},body:JSON.stringify({action,payload:extraPayload})});if(r.ok){loadStats();}else{console.warn('Falha op',action);} }finally{btn.textContent=original;btn.disabled=false;}}
    if(hasValid())unlock();
    form.addEventListener('submit',async ev=>{ev.preventDefault();err.textContent='';const value=pw.value.trim();if(!value){err.textContent='Informe a senha';return}const btn=form.querySelector('button[type=submit]');btn.disabled=true;btn.style.opacity='.6';try{await auth(value);unlock();}catch(e){err.textContent=e.message}finally{btn.disabled=false;btn.style.opacity='1';}});
    clearBtn.addEventListener('click',()=>{[localStorage,sessionStorage].forEach(s=>{s.removeItem(K);s.removeItem(KE)});err.style.color='#1f6feb';err.textContent='Sessão limpa';pw.focus();});
  if(btnTrends)btnTrends.addEventListener('click',()=>execAction('executar-tendencias',btnTrends));
  if(btnMonet)btnMonet.addEventListener('click',()=>execAction('monetizar',btnMonet));
    if(btnRefresh)btnRefresh.addEventListener('click',()=>loadStats());
  })();`;
}
