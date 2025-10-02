// Endpoint de introspecção para diagnosticar ambiente em produção
// NÃO deixar em produção final sem proteger (remova depois de validar deploy)

export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');
  const envKeys = Object.keys(process.env).filter(k => k.startsWith('DASHBOARD') || k.startsWith('VERCEL_'));
  res.status(200).json({
    ok: true,
    message: 'API introspect ativa',
    node: process.version,
    envPresent: envKeys,
    time: new Date().toISOString(),
  });
}
