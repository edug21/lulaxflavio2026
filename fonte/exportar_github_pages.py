"""Gera fonte/saida/site (site publicável na Vercel) a partir de fonte/saida/site-claude/index.html,
gerado antes por build.py. Com --publicar, copia o site para a raiz do repositório (pasta acima de fonte/).

Configuração em config.json:
  site_url     endereço final do site (usado na prévia das redes e no link canônico)
  goatcounter  código da conta no GoatCounter ("SEU-CODIGO" desliga os contadores)
  contato      e-mail para avisos de erro (vazio: não mostra o e-mail)
"""
import json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
WEB = os.path.join(HERE, 'web')
OUT = os.path.join(HERE, 'saida', 'site')
CFG = json.load(open(os.path.join(HERE, 'config.json')))
SITE = CFG['site_url'].rstrip('/') + '/'

src = open(os.path.join(HERE, 'saida', 'site-claude', 'index.html')).read()
title = re.search(r'<title>.*?</title>', src).group(0)
body = src.replace(title, '', 1)

# Fontes hospedadas no próprio site, no lugar do Google Fonts
body = re.sub(r'<link rel="preconnect" href="https://fonts\.(googleapis|gstatic)\.com"[^>]*>\n?', '', body)
body = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">\n?', '', body)

# Retratos em WebP, com JPG de reserva
for n in ('lula', 'flavio'):
    body = body.replace(f'<img src="{n}.jpg" alt=""',
                        f'<picture><source srcset="{n}.webp" type="image/webp"><img src="{n}.jpg" alt=""', 1)
    body = re.sub(rf'(<img src="{n}\.jpg" alt=""[^>]*>)', r'\1</picture>', body, count=1)

# Fora do servidor (arquivo aberto no computador), compartilha o endereço oficial, não o do claude.ai
body = body.replace("var ARTIFACT_URL = 'https://claude.ai/artifact/5rgXw8Sz9Jop8jCnTMS1Wu';", f"var ARTIFACT_URL = '{SITE}';")

# Código do GoatCounter
if CFG.get('goatcounter'):
    body = body.replace("var GOATCOUNTER = 'SEU-CODIGO';", f"var GOATCOUNTER = '{CFG['goatcounter']}';")

desc = 'Lula e Flávio Bolsonaro lado a lado: propostas, efeitos, trajetórias, escândalos e indicadores, com a fonte de cada informação.'
og_desc = 'Lula foi reeleito com 51,79% dos votos válidos. Resultado, propostas e histórico dos dois candidatos, lado a lado, com fonte em cada informação.'
fonts_css = open(os.path.join(WEB, 'fonts.css')).read()

head = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{title}
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Lula × Flávio 2026">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="Lula × Flávio 2026: o resultado e os dois lado a lado">
<meta property="og:description" content="{og_desc}">
<meta property="og:image" content="{SITE}og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Retratos de Lula e Flávio Bolsonaro lado a lado, com o título Lula × Flávio 2026">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Lula × Flávio 2026: o resultado e os dois lado a lado">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="{SITE}og.jpg">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#0f1312">
<link rel="preload" href="fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/public-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>
{fonts_css}</style>
<!-- Vercel Web Analytics (só funciona com o site hospedado na Vercel e Web Analytics ativado no painel) -->
<script>
  window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
</script>
<script defer src="/_vercel/insights/script.js"></script>
<style>*,*::before,*::after{{box-sizing:border-box}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
'''

leia = None
if os.path.exists(os.path.join(OUT, 'LEIA-ME.md')):
    leia = open(os.path.join(OUT, 'LEIA-ME.md')).read()
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT, exist_ok=True)
if leia:
    open(os.path.join(OUT, 'LEIA-ME.md'), 'w').write(leia)

open(os.path.join(OUT, 'index.html'), 'w').write(head + body + '\n</body>\n</html>\n')
for f in ('lula.jpg', 'flavio.jpg'):
    shutil.copy(os.path.join(HERE, f), OUT)
for f in ('lula.webp', 'flavio.webp', 'og.jpg', 'favicon.svg', 'apple-touch-icon.png'):
    shutil.copy(os.path.join(WEB, f), OUT)
shutil.copytree(os.path.join(WEB, 'fonts'), os.path.join(OUT, 'fonts'))
open(os.path.join(OUT, '.nojekyll'), 'w').write('')

# Cache na Vercel: fontes nunca mudam; imagens e página revalidam
json.dump({
    "headers": [
        {"source": "/fonts/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        {"source": "/(.*)\\.(jpg|webp|png|svg)", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400, stale-while-revalidate=604800"}]},
        {"source": "/", "headers": [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]}
    ]
}, open(os.path.join(OUT, 'vercel.json'), 'w'), indent=2)

open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE}</loc></url></urlset>\n')

# Checagem semanal de links (GitHub Actions + lychee)
wf = os.path.join(OUT, '.github', 'workflows')
os.makedirs(wf)
open(os.path.join(wf, 'checar-links.yml'), 'w').write('''name: Checar links das fontes
on:
  schedule:
    - cron: "0 11 * * 1"   # toda segunda, 8h de Brasília
  workflow_dispatch:
jobs:
  links:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - uses: actions/checkout@v4
      - name: Verificar links
        id: lychee
        uses: lycheeverse/lychee-action@v2
        with:
          args: --no-progress --max-concurrency 4 --timeout 30 --accept 200,201,202,203,204,206,301,302,303,307,308,403,429 index.html
          fail: false
      - name: Abrir issue com links quebrados
        if: steps.lychee.outputs.exit_code != 0
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: Links quebrados nas fontes
          content-filepath: ./lychee/out.md
          labels: links
''')
print('ok', OUT)

# --publicar: copia o site para a raiz do repositório (nunca apaga nada lá)
import sys
if '--publicar' in sys.argv:
    DEST = ROOT
    for f in os.listdir(OUT):
        src_f = os.path.join(OUT, f)
        if f in ('LEIA-ME.md', '.github'):
            continue
        if os.path.isdir(src_f):
            shutil.copytree(src_f, os.path.join(DEST, f), dirs_exist_ok=True)
        else:
            shutil.copy(src_f, os.path.join(DEST, f))
    print('publicado em', os.path.abspath(DEST))
