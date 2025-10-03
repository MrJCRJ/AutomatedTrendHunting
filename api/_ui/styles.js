// UI Fragment: estilos base compartilhados entre páginas HTML serverless
export function buildStyles(){
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
