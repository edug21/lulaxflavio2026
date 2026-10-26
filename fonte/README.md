# Código-fonte do site

Esta pasta gera o site publicado na raiz do repositório. Ela **não é publicada** na Vercel (está no `.vercelignore`).

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `build.py` | Monta a página: seções, dados e fontes. As citações usam `[[n]]` ou `[[n,m]]`, onde `n` é o número da fonte. |
| `template.html` | Visual, CSS e scripts da página. Lá fica a data "Atualizado em". |
| `impacto.py`, `escandalos.py`, `legal.py` | Dados das propostas de maior impacto e dos escândalos. |
| `refs.json` | Bibliografia da pesquisa original (fontes 1 a 154). As fontes 201 em diante estão em `build.py` e `escandalos.py`. |
| `config.json` | Endereço do site, código do GoatCounter e e-mail de correções. |
| `web/` | Fontes tipográficas, ícones, retratos em WebP e a imagem de prévia (`og.jpg`, gerada a partir de `og-imagem.html`). |
| `exportar_github_pages.py` | Gera a versão publicável e, com `--publicar`, copia para a raiz do repositório. |
| `LEIA-ME-publicacao.md` | Como funcionam a Vercel, os contadores e a prévia nas redes. |

## Como atualizar

Requer Python 3, sem bibliotecas extras.

```
cd fonte
python3 build.py                              # gera saida/site-claude/index.html
python3 exportar_github_pages.py --publicar   # gera saida/site e copia para a raiz
cd ..
git add -A && git commit -m "Atualização" && git push
```

A cada atualização, registre a mudança na lista `MUDOU` em `build.py` (aparece em "O que mudou" no site). A pasta `saida/` é temporária e não vai para o repositório.
