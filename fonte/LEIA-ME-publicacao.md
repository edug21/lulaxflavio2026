# Lula × Flávio 2026: como publicar e manter

Esta pasta é o site pronto. Envie tudo para a raiz de um repositório no GitHub, incluindo os arquivos ocultos `.nojekyll` e `.github/`.

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `index.html` | O site |
| `lula.webp`, `flavio.webp` (+ `.jpg` de reserva) | Retratos |
| `fonts/` | Fontes hospedadas no próprio site, sem depender do Google Fonts |
| `og.jpg` | Imagem de prévia no WhatsApp e nas redes (1200×630) |
| `favicon.svg`, `apple-touch-icon.png` | Ícone da aba e do atalho no celular |
| `vercel.json` | Cache das fontes e imagens na Vercel |
| `robots.txt`, `sitemap.xml` | Para buscadores |
| `.github/workflows/checar-links.yml` | Checagem semanal de links quebrados |

## 1. Contadores no topo

**Compartilhamentos** já funcionam, sem cadastro: o site usa o contador público Abacus (abacus.jasoncameron.dev), na chave `lulaxflavio2026/compartilhamentos`. Cada rede conta uma vez por visita (WhatsApp, X, copiar link etc.). O total aparece no topo a partir do primeiro compartilhamento e no painel de compartilhar. O contador expira se ficar 6 meses sem uso.

**Visitas** usam o GoatCounter (grátis):

1. Crie uma conta em https://www.goatcounter.com/signup e escolha um código, como `lulaflavio`.
2. No painel, abra **Settings** e marque **"Allow adding visitor counts on your website"**. Salve.
3. Coloque o código em `fonte/config.json` (campo `goatcounter`) e rode a exportação de novo (veja a seção 5). Se for editar à mão, troque `SEU-CODIGO` no `index.html`.

## 2. Vercel e Vercel Web Analytics

1. Em https://vercel.com, use **Add New → Project** e importe o repositório. Em *Framework Preset*, escolha **Other** e deixe o build em branco.
2. No projeto, abra **Analytics**, clique em **Enable** e faça um novo deploy.
3. Visitas aparecem em qualquer plano. Compartilhamentos e cópias de link por tema chegam como o evento `Compartilhar`, mas só aparecem nos planos Pro ou Enterprise.
4. Se o painel mostrar outro endereço de script (`/<caminho-único>/script.js`), troque `/_vercel/insights/script.js` no `index.html`.

Com o repositório ligado à Vercel, cada envio ao GitHub publica o site sozinho.

## 3. Prévia nas redes

A prévia usa o endereço em `fonte/config.json` (`site_url`, hoje `https://lulaxflavio2026.vercel.app/`). Se o domínio mudar, atualize o campo e exporte de novo.

Para testar, cole o link em https://www.opengraph.xyz. O WhatsApp guarda a prévia antiga por alguns dias. Para forçar uma nova, compartilhe o link com `?v=2` no final.

## 4. Checagem semanal de links

O arquivo em `.github/workflows/` roda toda segunda às 8h (horário de Brasília) e abre uma *issue* no repositório se alguma das 213 fontes estiver fora do ar. Para rodar na hora, use **Actions → Checar links das fontes → Run workflow**.

## 5. Atualizar o conteúdo

O código-fonte está na pasta `fonte/` do projeto completo.

```
cd fonte
python3 build.py                  # gera site-claude/index.html
python3 exportar_github_pages.py  # gera esta pasta (mantém este LEIA-ME)
```

A cada atualização:
1. Mude a data em `template.html` ("Atualizado em").
2. Registre a mudança na lista `MUDOU` em `build.py`. Ela aparece na seção "O que mudou".

Para mostrar um e-mail de correções no site, preencha `contato` em `fonte/config.json`.
