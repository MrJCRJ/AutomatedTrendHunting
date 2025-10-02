# ✅ Guia de Verificação Google AdSense

Se o AdSense mostra: "Não foi possível verificar seu site" siga este checklist.

## 1. Itens Obrigatórios no Site
| Item | Status Esperado |
|------|-----------------|
| Script AdSense global | `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7400152355684556" crossorigin="anonymous"></script>` no `<head>` |
| `ads.txt` acessível | https://SEU_DOMINIO/ads.txt |
| Política de Privacidade | Link visível no rodapé |
| Conteúdo original | Texto suficiente (≥ 300 palavras) |
| Sem conteúdo adulto/polêmico | OK |
| Indexável (robots) | `Allow: /` configurado |

## 2. Corrigir Script AdSense
No seu `index.html`, troque o snippet (atual sem client) por este NO TOPO DO `<head>`:
```html
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7400152355684556" crossorigin="anonymous"></script>
```
Remova duplicados se houver. Só precisa UMA vez.

## 3. Verificar `ads.txt`
Arquivo criado em `ads.txt` com conteúdo:
```
google.com, pub-7400152355684556, DIRECT, f08c47fec0942fa0
```
Teste no navegador: https://SEU_DOMINIO/ads.txt

## 4. Política de Privacidade
Já criada em `politica-privacidade.html` (ok). Certifique-se de que está acessível publicamente (`https://SEU_DOMINIO/politica-privacidade.html`).

## 5. Search Console (Opcional, Recomendado)
1. Acesse https://search.google.com/search-console
2. Adicione sua propriedade (domínio ou URL prefix)
3. Verifique via DNS ou HTML
4. Envie sitemap futuramente (`sitemap.xml`)

## 6. Aguardar Aprovação
Após corrigir, no painel AdSense:
1. Clique em "Verificar novamente" ou "Estou pronto"
2. Aguarde 24h a 7 dias
3. Monitore email para notificações

## 7. Logs e Debug
Use DevTools → Network → Filtrar por `ads?client=`
- Se carrega: OK
- Se bloqueado: verifique bloqueadores/adblock/testes locais

## 8. Problemas Comuns
| Problema | Causa | Solução |
|----------|-------|---------|
| Script sem `client=` | Uso de snippet antigo | Substituir pelo novo completo |
| `ads.txt` 404 | Não deployou arquivo | Rebuild/redeploy e aguardar cache |
| Sem anúncios após aprovação | Conteúdo insuficiente | Adicionar mais blocos e texto |
| Página em revisão por dias | Domínio novo | Aguardar ou adicionar Search Console |

## 9. Próximos Passos (Após Aprovação)
- Ativar anúncios automáticos no painel (Auto Ads)
- Criar blocos fixos (in-article, anchor, vignette)
- Monitorar RPM no AdSense

## 10. Checklist Rápido Final
```bash
[ ] Script com client atualizado
[ ] ads.txt acessível
[ ] Política de privacidade linkada
[ ] Conteúdo relevante e legível
[ ] Robots.txt permitindo indexação
[ ] Domínio ativo há alguns dias
[ ] Sem bloqueio regional / firewall
```

Se tudo acima estiver OK e ainda falhar → abra ticket no suporte do AdSense anexando prints.
