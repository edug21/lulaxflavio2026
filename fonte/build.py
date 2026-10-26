import os as _os
import json, re, html

refs = {int(k): v for k, v in json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'refs.json'))).items()}
used = set()
NEW = {
 201: ('Câmara terá 121 deputados do PL e 70 do PT — Gazeta SP, 5/10/2026', 'https://www.gazetasp.com.br/politica/camara-tera-121-deputados-do-pl-e-70-do-pt-confira-como-ficaram-as-513-cadeiras-por-partido-e-os-mais-votados-das-eleicoes-de-2026-no-brasil/'),
 202: ('Mapa do poder: PL domina Congresso após 1º turno — Correio da Manhã', 'https://www.correiodamanha.com.br/politica/2026/10/324418-mapa-do-poder-pl-domina-congresso-e-amplia-presenca-nos-estados-apos-primeiro-turno.html'),
 203: ('Veja como fica o tamanho dos partidos no Congresso — Congresso em Foco', 'https://www.congressoemfoco.com.br/noticia/122910/veja-como-fica-o-tamanho-dos-partidos-no-congresso-apos-as-eleicoes'),
 204: ('Constituição Federal, art. 60 (quórum de PEC) — Planalto', 'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm'),
 205: ('Flávio vence em 14 estados; Lula domina Nordeste — Congresso em Foco', 'https://www.congressoemfoco.com.br/noticia/122887/flavio-vence-em-14-estados-lula-leva-13-e-domina-nordeste'),
 206: ('Mapa das eleições: Flávio vence em 14 estados e DF, Lula em 12 — Correio', 'https://www.correio24horas.com.br/eleicoes/mapa-das-eleicoes-flavio-bolsonaro-vence-em-14-estados-lula-em-12-1026'),
 207: ('PP e União Brasil declaram apoio a Flávio no 2º turno — Congresso em Foco', 'https://www.congressoemfoco.com.br/noticia/123048/pp-e-uniao-brasil-declaram-apoio-a-flavio-no-segundo-turno'),
 208: ('Flávio soma Republicanos e ex-candidatos no 2º turno — Seu Dinheiro, 7/10/2026', 'https://www.seudinheiro.com/2026/politica/flavio-soma-republicanos-e-ex-candidatos-no-xadrez-do-segundo-turno-lula-busca-reacao-no-alvorada-o-dia-na-politica-ccgg/'),
 209: ('Romeu Zema declara apoio a Flávio no 2º turno — Diário do Nordeste', 'https://diariodonordeste.verdesmares.com.br/pontopoder/romeu-zema-declara-apoio-a-flavio-bolsonaro-no-2-turno-das-eleicoes-2026-1.3796722'),
 210: ('Caiado apoia Flávio Bolsonaro — Tribuna de Jundiaí', 'https://tribunadejundiai.com.br/politica/eleicoes-2026/caiado-apoia-flavio-bolsonaro/'),
 211: ('Lula reúne sete partidos em aliança e consolida chapa com Alckmin — Jornal Grande Bahia', 'https://jornalgrandebahia.com.br/?p=1374769'),
 212: ('Datafolha divulga 1ª pesquisa do 2º turno entre Lula e Flávio — O Povo, 8/10/2026', 'https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/08/datafolha-divulga-1-pesquisa-do-2-turno-entre-lula-e-flavio.html'),
 213: ('Primeira pesquisa sobre Lula x Flávio no 2º turno (PoderData) — Revista Fórum', 'https://revistaforum.com.br/politica/primeira-pesquisa-2-turno-lula-flavio-bolsonaro/'),
 214: ('Calendário de debates do 2º turno é atualizado — TVT News, 8/10/2026', 'https://tvtnews.com.br/?p=805639'),
 215: ('Lula e Flávio terão primeiro debate do 2º turno na Band em 18/10 — Times Brasil', 'https://timesbrasil.com.br/eleicoes-2026/decisao-2026-lula-e-flavio-bolsonaro-terao-primeiro-debate-do-2o-turno-na-band-em-18-de-outubro/'),
 216: ('Declaração de bens dos candidatos à Presidência — Congresso em Foco', 'https://www.congressoemfoco.com.br/noticia/121320/saiba-qual-foi-a-declaracao-de-bens-dos-candidatos-a-presidencia'),
 217: ('Patrimônio declarado de Flávio sobe 211% em termos reais desde 2018 — Poder360', 'https://www.poder360.com.br/poder-eleicoes-2026/patrimonio-declarado-de-flavio-sobe-211-desde-2018/'),
 218: ('Flávio Bolsonaro lidera arrecadação eleitoral — BNews, 9/9/2026', 'https://www.bnewssaopaulo.com.br/noticias/politica/flavio-bolsonaro-lidera-arrecadacao-eleitoral-com-r-443-milhoes.html'),
 219: ('Presidenciáveis já gastaram R$ 74 milhões com campanha (teto de gastos) — TNH1', 'https://www.tnh1.com.br/noticia/nid/presidenciaveis-ja-gastaram-r-74-milhoes-com-campanha-veja-as-principais-despesas/'),
 220: ('Alckmin é confirmado como vice e vai reeditar chapa de Lula — Poder360', 'https://www.poder360.com.br/poder-eleicoes-2026/alckmin-e-confirmado-como-vice-e-vai-reeditar-chapa-vitoriosa-de-lula/'),
 221: ('Flávio anuncia Alfredo Gaspar como candidato a vice — Estado de Minas', 'https://www.em.com.br/politica/2026/08/7474191-flavio-bolsonaro-anuncia-alfredo-gaspar-como-candidato-a-vice.html'),
 222: ('Flávio anuncia Alfredo Gaspar, relator da comissão do INSS, como vice — Bem Paraná', 'https://www.bemparana.com.br/eleicoes-2026/flavio-bolsonaro-anuncia-alfredo-gaspar-relator-da-comissao-do-inss-como-vice/'),
 223: ('Fim da 6x1, soberania e segurança: o plano de Lula — Congresso em Foco', 'https://www.congressoemfoco.com.br/noticia/121276/fim-da-6x1-soberania-e-seguranca-o-plano-de-lula-para-novo-mandato'),
 224: ('EUA, Tesouraço e presídios: o que prevê o plano de Flávio — Congresso em Foco', 'https://www.congressoemfoco.com.br/noticia/121271/eua--tesouraco-e-presidios-o-que-preve-o-plano-de-governo-de-flavio'),
 225: ('Plano de Flávio ignora Mercosul e quer reaproximar Israel — SBT News', 'https://sbtnews.sbt.com.br/noticia/politica/plano-de-flavio-ignora-mercosul-e-quer-reaproximar-israel'),
 226: ('Planos dos presidenciáveis trazem propostas para Previdência, INSS e idosos — Correio da Manhã', 'https://www.correiodamanha.com.br/economia/previdencia/2026/10/323750-planos-dos-presidenciaveis-trazem-propostas-para-previdencia-inss-e-idosos.html'),
 227: ('Flávio Bolsonaro: nova reforma da Previdência e retomar a trabalhista — Gazeta do Povo', 'https://www.gazetadopovo.com.br/republica/flavio-bolsonaro-nova-reforma-previdencia-retomar-trabalhista/'),
 285: ('PCB e PSTU farão apoio crítico a Lula e ao PT no 2º turno — Times Brasil, 7/10/2026', 'https://timesbrasil.com.br/eleicoes-2026/pcb-e-pstu-farao-apoio-critico-a-lula-e-ao-pt-no-segundo-turno/'),
 286: ('Unidade Popular declara apoio a Lula no 2º turno — Piranot, 11/10/2026', 'https://www.piranot.com.br/2026/10/11/noticias/politica/eleicoes/unidade-popular-apoia-lula-eleicao/'),
 287: ('Augusto Cury declara apoio a Flávio Bolsonaro no 2º turno — Poder360, 8/10/2026', 'https://www.poder360.com.br/poder-eleicoes-2026/augusto-cury-declara-apoio-a-flavio-bolsonaro-no-2o-turno/'),
 288: ('Flávio tem 51,1% e Lula 45,7% no 2º turno, mostra AtlasIntel — Forbes Brasil, 9/10/2026', 'https://forbes.com.br/geral/2026/10/flavio-tem-511-e-lula-457-das-intencoes-de-voto-no-2o-turno-mostra-atlas/'),
 305: ('Pesquisa Datafolha: Flávio Bolsonaro e Lula empatam em 50% dos votos válidos — Exame, 22/10/2026', 'https://exame.com/brasil/pesquisa-datafolha-flavio-bolsonaro-lula-empatam-numericamente/'),
 306: ('Datafolha divulga pesquisa do 2º turno entre Lula e Flávio — Estado de Minas, 22/10/2026', 'https://www.em.com.br/politica/2026/10/7525469-datafolha-divulga-pesquisa-do-2-turno-entre-lula-e-flavio.html'),
 307: ('Quaest: Flávio Bolsonaro tem 45% e Lula, 44%, no 2º turno — Metrópoles, 21/10/2026', 'https://www.metropoles.com/brasil/quaest-flavio-bolsonaro-tem-45-e-lula-44-no-2o-turno'),
 308: ('Lula e Flávio fazem primeiro debate das eleições na Band — Agência Brasil, 18/10/2026', 'https://agenciabrasil.ebc.com.br/politica/noticia/2026-10/lula-e-flavio-fazem-primeiro-debate-das-eleicoes-na-band'),
 309: ('Lula e Flávio Bolsonaro confirmam debate na Globo nesta sexta (23/10) — O Tempo, 21/10/2026', 'https://www.otempo.com.br/eleicoes/2026/presidentes/2026/10/21/lula-e-flavio-bolsonaro-confirmam-debate-na-globo-nesta-sexta-23-10-veja-horario-e-regras'),
 310: ('Presidente do TSE anuncia reeleição de Lula e faz balanço do 2º turno — TSE, 26/10/2026', 'https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/presidente-do-tse-anuncia-reeleicao-de-lula-e-faz-balanco-do-2o-turno-das-eleicoes-2026'),
 311: ('Lula é reeleito para quarto mandato de presidente — Agência Senado, 25/10/2026', 'https://www12.senado.leg.br/noticias/materias/2026/10/25/lula-e-reeleito-para-quarto-mandato-de-presidente'),
 312: ('MAPA: veja como ficou a votação para presidente em cada estado no 2º turno — Exame, 10/2026', 'https://exame.com/brasil/mapa-veja-como-ficou-a-votacao-para-presidente-em-cada-estado-no-2o-turno/'),
 313: ('Lula vence em 13 estados no 2º turno; Flávio, em 13 e no DF — Poder360, 10/2026', 'https://www.poder360.com.br/poder-eleicoes-2026/lula-vence-em-13-estados-no-2o-turno-flavio-nos-outros-13-e-no-df/'),
 314: ('Eleições 2026: Lula é reeleito; confira resultado do 2º turno em SP — TRE-SP, 10/2026', 'https://www.tre-sp.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-lula-e-reeleito-presidente-da-republica-confira-resultado-do-2o-turno-em-sp'),
 315: ('Zanin prorroga eleição até as 19h deste domingo em todo o país — CNN Brasil, 25/10/2026', 'https://www.cnnbrasil.com.br/eleicoes/zanin-prorroga-eleicao-ate-as-19h-deste-domingo-em-todo-o-pais/'),
 316: ('Flávio critica decisão de Zanin, mas PL também pediu prorrogação da votação — Metrópoles, 25/10/2026', 'https://www.metropoles.com/brasil/flavio-critica-decisao-de-zanin-mas-pl-tambem-pediu-prorrogacao-da-votacao'),
 317: ('Flávio não aceita derrota e diz que pedirá a anulação do resultado — Poder360, 25/10/2026', 'https://www.poder360.com.br/poder-eleicoes-2026/flavio-nao-aceita-derrota-e-diz-que-pedira-a-anulacao-do-resultado/'),
 318: ('Lula agradece votos e diz que teve de vencer intromissão vinda de fora — Agência Brasil, 25/10/2026', 'https://agenciabrasil.ebc.com.br/politica/noticia/2026-10/lula-agradece-votos-e-diz-que-teve-de-vencer-intromissao-vinda-de-fora'),
 319: ('Posse presidencial em 2027 será em 5 de janeiro — Rádio Senado, 5/1/2026', 'https://www12.senado.leg.br/radio/1/noticia/2026/01/05/posse-presidencial-em-2027-sera-em-5-de-janeiro-e-governadores-tomam-posse-no-dia-6'),
 320: ('Veja como foi o debate na Globo entre Flávio e Lula — Gazeta do Povo, 23/10/2026', 'https://www.gazetadopovo.com.br/eleicoes/2026/debate-globo-flavio-bolsonaro-lula-segundo-turno-como-foi/'),
 321: ('Datafolha, Quaest e AtlasIntel mostram disputa indefinida na véspera da eleição — RED, 24/10/2026', 'https://red.org.br/noticias/datafolha-e-quaest-mostram-disputa-presidencial-indefinida-na-vespera-da-eleicao/'),
 296: ('Congresso promulga emenda do fim da 6x1; escala 5x2 começa em 60 dias — Agência Brasil, 16/10/2026', 'https://agenciabrasil.ebc.com.br/politica/noticia/2026-10/congresso-promulga-emenda-do-fim-da-6x1-escala-5x2-comeca-em-60-dias'),
 297: ('Congresso promulga o fim da escala 6x1 e aposentadoria de agentes de saúde — Agência Senado, 16/10/2026', 'https://www12.senado.leg.br/noticias/materias/2026/10/16/congresso-promulga-o-fim-da-escala-6x1-e-aposentadoria-de-agentes-de-saude'),
 298: ('Em vitória do governo Lula, Senado aprova PEC do fim da escala 6x1 — Metrópoles, 14/10/2026', 'https://www.metropoles.com/brasil/senado-pec-escala-6x1'),
 299: ('Flávio vota pelo fim da 6x1 após assinar PEC do Trabalho Flexível — Poder360, 14/10/2026', 'https://www.poder360.com.br/poder-congresso/flavio-vota-a-favor-do-fim-da-6-x-1-apos-assinar-pec-do-trabalho-flexivel/'),
 300: ('Saiba como estão Lula e Flávio nas pesquisas a 8 dias do 2º turno — Poder360, 10/2026', 'https://www.poder360.com.br/poder-eleicoes-2026/leia-como-estao-lula-e-flavio-nas-pesquisas-a-8-dias-do-2o-turno/'),
 301: ('Datafolha e Quaest divulgam novas pesquisas sobre 2º turno — O Povo, 14/10/2026', 'https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/14/datafolha-e-quaest-divulgam-novas-pesquisas-sobre-2-turno-entre-lula-e-flavio.html'),
 302: ('Flávio diz que vai ao debate da Band após Lula confirmar presença — CNN Brasil, 14/10/2026', 'https://www.cnnbrasil.com.br/eleicoes/flavio-confirma-ida-ao-debate-da-band/'),
 303: ('Dark Horse: PF pede mais 90 dias para investigação sobre filme de Bolsonaro — Metrópoles, 16/10/2026', 'https://www.metropoles.com/colunas/manoela-alcantara/dark-horse-pf-pede-mais-90-dias-para-investigacao-sobre-filme-de-bolsonaro'),
 304: ('PF avalia fatiar caso Dark Horse e deixar apuração sobre Flávio para etapa posterior — Jornal Grande Bahia, 14/10/2026', 'https://jornalgrandebahia.com.br/2026/10/pf-avalia-fatiar-caso-dark-horse-concluir-suspeitas-contra-daniel-vorcaro-e-deixar-apuracao-sobre-flavio-bolsonaro-para-etapa-posterior/'),
 294: ('Congresso promulga PEC da Transição — Agência Brasil, 21/12/2022', 'https://agenciabrasil.ebc.com.br/politica/noticia/2022-12/congresso-promulga-pec-da-transicao'),
 295: ('Editada MP que amplia os beneficiários do Auxílio Reconstrução — Agência Senado, ago/2024', 'https://www12.senado.leg.br/noticias/audios/2024/08/editada-mp-que-amplia-os-beneficiarios-do-auxilio-reconstrucao'),
 292: ('AtlasIntel: Flávio abre 5,4 pontos sobre Lula no 2º turno e vai a 51% dos votos — InfoMoney, 9/10/2026', 'https://www.infomoney.com.br/politica/atlasintel-flavio-abre-54-pontos-sobre-lula-no-2o-turno-e-vai-a-51-dos-votos/'),
 293: ('AtlasIntel: Flávio tem 52,8% no 2º turno em votos válidos; Lula soma 47,2% — Metrópoles, 9/10/2026', 'https://www.metropoles.com/brasil/atlasintel-flavio-tem-528-e-lula-472-no-2o-turno-em-votos-validos'),
 289: ('Emissora cancela debate entre Lula e Flávio Bolsonaro — O Povo, 9/10/2026', 'https://www.opovo.com.br/noticias/politica/eleicoes/2026/10/09/emissora-cancela-debate-entre-lula-e-flavio-bolsonaro.html'),
 290: ('Fim da escala 6x1 passa pela 3ª sessão de discussão no Plenário — Agência Senado, 8/10/2026', 'https://www12.senado.leg.br/noticias/materias/2026/10/08/fim-da-escala-6x1-passa-pela-3a-sessao-de-discussao-no-plenario'),
 291: ('Fim da escala 6x1 será votado no Senado na quarta-feira — Forbes Brasil, 10/10/2026', 'https://forbes.com.br/forbes-money/2026/10/fim-escala-6x1-votacao-senado-reducao-jornada/'),
}
import sys; sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
from legal import NEWREFS, LEG, INST
NEW.update(NEWREFS)
for k, (t, u) in NEW.items():
    refs[k] = {'t': t, 'u': u}

def R(s):
    """Replace [[1,2]] with linked source markers."""
    def rep(m):
        nums = [int(x) for x in m.group(1).split(',')]
        out = []
        for n in nums:
            used.add(n)
            r = refs[n]
            out.append(f'<a class="ref" href="{html.escape(r["u"])}" target="_blank" rel="noopener" title="{html.escape(r["t"])}">{n}</a>')
        return '<span class="refs">' + ''.join(out) + '</span>'
    return re.sub(r'\[\[([\d,\s]+)\]\]', rep, s)

CHIP = {
    'tse': ('Plano TSE', 'c-tse'),
    'fala': ('Fala pública', 'c-fala'),
    'cond': ('Depende do Congresso', 'c-cond'),
    'cont': ('Continuidade', 'c-cont'),
    'nova': ('Proposta nova', 'c-nova'),
    'lei': ('Lei aprovada', 'c-lei'),
    'pend': ('Não aprovado', 'c-pend'),
    'inv': ('Investigação', 'c-inv'),
    'anul': ('Decisão processual', 'c-anul'),
    'fato': ('Fato documentado', 'c-fato'),
    'interp': ('Interpretação de fonte', 'c-interp'),
}

def chips(keys):
    return ''.join(f'<span class="chip {CHIP[k][1]}">{CHIP[k][0]}</span>' for k in keys)

def cell(who, c):
    items = ''.join(f'<li>{R(i)}</li>' for i in c['items'])
    return (f'<div class="cell cell-{who}"><span class="who who-{who}">{"Lula" if who=="l" else "Flávio Bolsonaro"}</span>'
            f'<div class="chips">{chips(c.get("tags", []))}</div><ul>{items}</ul></div>')

def row(r):
    note = f'<p class="note"><b>Comparação:</b> {R(r["note"])}</p>' if r.get('note') else ''
    return (f'<article class="row" id="{r["id"]}"><h3>{r["t"]}</h3><div class="pair">{cell("l", r["l"])}{cell("f", r["f"])}</div>{note}</article>')

# ---------------- CONTENT ----------------
perfil = [
 dict(id='candidatura', t='Candidatura 2026',
  l=dict(tags=['fato'], items=[
   'Partido: <b>PT</b>. Vice: <b>Geraldo Alckmin</b>. [[96,97]]',
   'Registro da chapa validado pelo TSE, por unanimidade, em 2/9/2026. [[96,97]]',
   'Disputa o cargo enquanto exerce o 3º mandato (posse em 1/1/2023). [[89,97]]']),
  f=dict(tags=['fato'], items=[
   'Partido: <b>PL</b> (filiado desde 30/11/2021). Vice: <b>Alfredo Gaspar</b>. [[96,117]]',
   'Registro da chapa validado pelo TSE em 2/9/2026. [[96]]',
   'Primeira disputa pela Presidência; mandato de senador pelo RJ vai até 2027. [[116,97]]'])),
 dict(id='alianca', t='Partidos aliados',
  l=dict(tags=['fato'], items=[
   'Aliança anunciada na convenção de 2/8/2026: <b>PT, PCdoB, PV, PSB, PSOL, Rede e PDT</b>. [[211]]',
   'Inclui duas federações: Brasil da Esperança (PT, PCdoB, PV) e PSOL-Rede. [[211]]']),
  f=dict(tags=['fato'], items=[
   'Chapa formada só pelo <b>PL</b>: Flávio disse que tentou uma coligação, mas "não foi possível". [[221]]',
   'No 1º turno, recebeu apoio de Tarcísio de Freitas (Republicanos) e Ricardo Nunes (MDB), sem coligação formal. [[221]]'])),
 dict(id='vices', t='Candidatos a vice',
  l=dict(tags=['fato'], items=[
   '<b>Geraldo Alckmin</b> (PSB), 73 anos, vice-presidente desde 2023. [[220]]',
   'Governou São Paulo; foi ministro do Desenvolvimento, Indústria e Comércio até o início de 2026. [[220]]',
   'Ficou 33 anos no PSDB; disputou a Presidência em 2006 e 2018. [[220]]']),
  f=dict(tags=['fato'], items=[
   '<b>Alfredo Gaspar</b> (PL), deputado federal por Alagoas. [[221,222]]',
   'Ex-procurador-geral de Justiça do Ministério Público de Alagoas. [[221,222]]',
   'Relator da CPMI do INSS; trocou o União Brasil pelo PL em março de 2026. [[222]]'])),
 dict(id='bens', t='Bens declarados ao TSE',
  l=dict(tags=['fato'], items=[
   '<b>R$ 4,78 milhões</b>, em grande parte em planos de previdência privada. [[216]]',
   'Em 2022, havia declarado cerca de R$ 7,4 milhões. [[216]]']),
  f=dict(tags=['fato'], items=[
   '<b>R$ 8,19 milhões</b>; o principal bem é uma casa em Brasília. [[216,217]]',
   'Em 2018, declarou cerca de R$ 1,74 milhão: alta real de 211% (corrigida pelo IPCA). [[217]]']),
  note='Valores declarados ao TSE nem sempre refletem preço de mercado. [[216]]'),
 dict(id='arrecadacao', t='Arrecadação de campanha (até 8/9/2026)',
  l=dict(tags=['fato'], items=[
   '<b>R$ 35,9 milhões</b>, dos quais R$ 35 milhões repassados pelo PT do fundo eleitoral. [[218]]']),
  f=dict(tags=['fato'], items=[
   '<b>R$ 44,3 milhões</b>, dos quais R$ 42 milhões repassados pelo PL do fundo eleitoral. [[218]]',
   'Maiores doações individuais: R$ 500 mil (duas) e R$ 400 mil. [[218]]']),
  note='Dado parcial. O teto de gastos é R$ 88,9 milhões no 1º turno e R$ 44,5 milhões no 2º. A prestação de contas final vence em 14/11. [[218,219]]'),
 dict(id='turno1', t='1º turno (4/10/2026)',
  l=dict(tags=['fato'], items=[
   '<b>53.876.617 votos</b> — 45,16% dos válidos. [[140,97]]',
   'Classificado para o 2º turno, marcado para 25/10/2026. [[97,134]]']),
  f=dict(tags=['fato'], items=[
   '<b>56.104.268 votos</b> — 47,03% dos válidos. [[140,97]]',
   'Classificado para o 2º turno, marcado para 25/10/2026. [[97,134]]']),
  note='Diferença de cerca de 2,2 milhões de votos, com 99,99% das urnas apuradas. Brancos: 1,84% e nulos: 2,93% do total de votos. Até 8/10 não havia eleito. [[97,140]]'),
 dict(id='plano', t='Plano de governo registrado',
  l=dict(tags=['tse'], items=[
   '<i>Diretrizes para o Programa de Transformação do Brasil</i>: 13 diretrizes. [[67,68]]',
   'Novo plano protocolado pela Executiva Nacional do PT em 8/8/2026. [[68]]']),
  f=dict(tags=['tse'], items=[
   '<i>Para o Brasil Vencer o Atraso</i> (2027–2030): 76 páginas e 11 capítulos. [[78,79]]',
   'A Agência Brasil o resumiu em nove eixos (diferença só de organização). [[81]]']),
  note='Estar no TSE prova que o plano foi apresentado. O TSE não avalia custo, viabilidade nem aprovação das medidas. [[66]]'),
]

propostas = [
 dict(id='economia', t='Economia e tributos',
  l=dict(tags=['tse','cont'], items=[
   'Manter o arcabouço fiscal e controlar o crescimento da despesa. [[69]]',
   'Justiça tributária e progressividade na implementação da reforma tributária. [[69]]',
   'Isenção de IR até R$ 5 mil aparece como medida <b>já feita</b>, não como promessa nova. [[69,70]]',
   'Em fala na SBPC (28/7), citou recursos para ciência "por fora" do arcabouço, mas disse que não o desrespeitaria. [[74]]']),
  f=dict(tags=['tse','fala'], items=[
   '"Tesouraço": cortar ao menos <b>10 ministérios</b>, cargos e despesas; combater supersalários. [[81,82]]',
   'Retomar desestatizações, fortalecer a Lei das Estatais; Caixa como "Banco da Prosperidade". [[81]]',
   'Redimensionar a reforma tributária e reduzir o IVA (sem alíquota no plano). [[81,82]]',
   'Em fala na CNI (22/6), citou IVA de 20% e R$ 190 bi em cortes — números que <b>não</b> estão no plano. [[83]]']),
  note='Lula propõe manter as regras fiscais atuais; Flávio propõe reduzir o tamanho do Estado e dos tributos. [[69,81]]'),
 dict(id='trabalho', t='Trabalho e jornada',
  l=dict(tags=['tse','cond'], items=[
   'Atuar pelo <b>fim da escala 6x1</b> e jornada de <b>40 horas</b> sem redução de salário. [[69]] Já aprovado: promulgado em 16/10/2026 como Emenda Constitucional 141. [[296]]',
   'Proteção a trabalhadores de aplicativos, transparência de algoritmos e combate à "pejotização" fraudulenta. [[69]]',
   'Plataforma pública de empregabilidade com IA no Sine. [[69]]']),
  f=dict(tags=['tse','fala'], items=[
   'Contratos de menor custo para jovens de 18–24 anos (1º emprego) e pessoas 50+ desempregadas há 12 meses. [[83]]',
   'Negociado sobre o legislado, jornadas flexíveis, banco nacional de vagas. [[83]]',
   'O plano <b>não</b> menciona o fim da 6x1; em falas, criticou a redução sem corte salarial e defendeu salário por hora. [[73,84,86]]',
   'Como senador, <b>votou a favor</b> da PEC do fim da 6x1 em 14/10, embora tenha dito considerar o texto mal formulado e prejudicial à economia. [[299]]']),
  note='O fim da 6x1 já foi promulgado e vale ganhe quem ganhar: escala 5x2 e jornada de 42h em até 60 dias, 40h depois de 14 meses. Outras mudanças de jornada e direitos dependem do Congresso. [[296,297,84]]'),
 dict(id='social', t='Proteção social e cuidado',
  l=dict(tags=['tse','cont'], items=[
   'Manter, aperfeiçoar e ampliar o Bolsa Família (sem novo valor definido). [[68,71]]',
   'Ampliar Minha Casa, Minha Vida, priorizando os mais pobres. [[71]]',
   'Política Nacional de Cuidados: Cuidotecas, lavanderias públicas, cozinhas solidárias. [[71]]',
   'Manter cotas e ações afirmativas; fortalecer PAA e agricultura familiar. [[68,71]]']),
  f=dict(tags=['tse','nova'], items=[
   'Manter programas assistenciais, combater fraudes e usá-los como ponte para emprego. [[81,88]]',
   'Proibir uso de benefícios em apostas. [[81]]',
   '"Ganha-Ganha" (voluntário): bom histórico gera juros menores, crédito e cashback. [[81,88]]',
   '"Brasil por Elas": voucher-creche e Rede Nacional de Cuidado; centros para TEA e saúde mental. [[81,88]]']),
  note='Os dois mantêm programas de transferência; diferem no desenho e nas condicionalidades.'),
 dict(id='saude', t='Saúde',
  l=dict(tags=['tse','cont'], items=[
   'Teleconsulta e prontuário único pela RNDS, com marcação no celular. [[69]]',
   'IA para organizar a fila por risco clínico. [[69]]',
   'Ampliar Agora Tem Especialistas, Mais Médicos, Brasil Sorridente, CAPS e rede oncológica. [[69,71]]']),
  f=dict(tags=['tse','fala'], items=[
   'Corrigir a tabela SUS e ampliar a Saúde da Família. [[81,88]]',
   'Contratar rede privada ociosa; modernizar hospitais universitários (EBSERH). [[81,88]]',
   'Telessaúde, remédios em casa e prontuário único ligado ao CPF/Gov.br. [[81,88]]',
   'No debate da Band (18/10), disse que nomearia Cláudio Lottenberg, presidente do Hospital Albert Einstein, ministro da Saúde, para levar um "padrão Einstein" ao SUS. [[308]]']),
  note='Ambos apostam em saúde digital e IA; nenhum detalha custos o suficiente para comparar orçamento. [[69,88]]'),
 dict(id='educacao', t='Educação',
  l=dict(tags=['tse','nova','cont'], items=[
   'Meta: <b>80%</b> das crianças alfabetizadas na idade certa. [[68,69]]',
   'Creches, tempo integral e conectividade em todas as escolas. [[68,69]]',
   'Fortalecer o Pé-de-Meia, ampliar Institutos Federais e cumprir o PNE 2026–2036. [[68,69]]']),
  f=dict(tags=['tse'], items=[
   'Método fônico e reforço escolar remunerado. [[81,88]]',
   'Escolas cívico-militares, robótica e IA, tempo integral. [[81,88]]',
   'Voucher onde faltar vaga pública; empréstimo estudantil pago conforme a renda. [[81,88]]']),
  note='Números de matrículas e escolas conectadas no plano de Lula são balanço do mandato atual, não metas novas. [[69]]'),
 dict(id='seguranca', t='Segurança pública',
  l=dict(tags=['tse','cond','fala'], items=[
   'Mais coordenação federal (SUSP), inteligência, fronteiras e asfixia financeira do crime. [[72,77]]',
   'Ministério da Segurança <b>só se aprovada a PEC</b> enviada pelo Executivo. [[72,77]]',
   'R$ 10 bi do FIIS para estados e municípios; rastreio de armas; câmeras corporais. [[72]]',
   'Em fala (22/8): prender e retomar territórios, sem operações com muitas mortes. [[72]]']),
  f=dict(tags=['tse','cond'], items=[
   'Facções tratadas como <b>narcoterroristas</b>; fronteiras com as Forças Armadas. [[81,88]]',
   'Reduzir a maioridade penal de 18 para 16 anos (PEC 32/2019, de sua autoria, parada na CCJ). [[81,118]]',
   '5 presídios federais, 500 mil vagas, castração química, fim da progressão para hediondos. [[81,88]]',
   '"Muralha Brasileira": reconhecimento facial e mais de 1 milhão de câmeras. [[81,88]]']),
  note='Lula enfatiza coordenação e prevenção; Flávio, endurecimento penal e vigilância. Ministério, maioridade e progressão exigem Congresso. [[85]]'),
 dict(id='ambiente', t='Meio ambiente e energia',
  l=dict(tags=['tse'], items=[
   'Reduzir emissões líquidas em 59%–67% até 2035 (base 2005). [[75]]',
   'Desmatamento líquido zero até 2030; mercado de carbono, PSA e monitoramento por satélite e IA. [[75]]',
   'Transição energética (renováveis, H₂, biocombustíveis) mantendo petróleo e gás. [[75]]',
   'Análise independente: o plano não traz proposta específica de licenciamento. [[75]]']),
  f=dict(tags=['tse'], items=[
   'Zerar desmatamento <b>ilegal</b> até 2029; fiscalização por IA e satélite; mercado de carbono. [[81,88]]',
   'Licenciamento mais rápido, com licença por decurso de prazo. [[81,88]]',
   'Fracking sob regras ambientais, petróleo e gás, biocombustíveis e biogás. [[81,88]]']),
  note='As metas medem coisas diferentes: desmatamento líquido (Lula) e desmatamento ilegal (Flávio). [[75]]'),
 dict(id='infra', t='Infraestrutura e habitação',
  l=dict(tags=['tse','cont'], items=[
   'Nova edição ou expansão do Novo PAC, com investimento público e privado. [[69,76]]',
   'Concessões, ferrovias, portos e aeroportos regionais. [[76]]',
   'Urbanização de favelas, saneamento, mobilidade coletiva e adaptação climática. [[69]]']),
  f=dict(tags=['tse'], items=[
   '<b>R$ 900 bi</b> em quatro anos, via PPPs, concessões e BNDES. [[81,82]]',
   'Ferrogrão, Trem do Nordeste e Transnordestina. [[81]]',
   'Casa Verde e Amarela com meta de <b>2,5 milhões</b> de moradias; Lixão Zero. [[81,82]]']),
  note='Um valor-meta e uma diretriz de "ampliar" não são comparáveis sem orçamento, prazo e fonte de recursos.'),
 dict(id='instituicoes', t='Instituições e tecnologia',
  l=dict(tags=['tse'], items=[
   'Participação social, PPA 2028–2031 participativo, transparência com dados abertos. [[77]]',
   'Regulação de redes contra desinformação, preservando a liberdade de expressão. [[77]]',
   'Soberania digital: datacenters nacionais, modelos de IA em português, fibra e 5G. [[77]]']),
  f=dict(tags=['tse','cond'], items=[
   'Limitar decisões monocráticas e tirar competências criminais do STF. [[85,88]]',
   'Fim da reeleição presidencial; "Tesouraço na Censura". [[85,88]]',
   '100% dos serviços federais digitais, Gov.br, IA "ClarIA" e IA para pequenas empresas. [[88]]',
   'Em 7/10, ligou as mudanças constitucionais à obtenção de maioria no Congresso. [[85]]']),
  note='Mudanças constitucionais exigem PEC e quórum qualificado.'),
 dict(id='externa', t='Política externa',
  l=dict(tags=['tse','cont'], items=[
   'Política externa "universalista", com a soberania como eixo do programa. [[223]]',
   'Aprofundar BRICS e Sul Global, fortalecer o Mercosul, reformar ONU, OMC, FMI e Banco Mundial. [[223]]',
   'Responder a tarifaços dos EUA com base em regras internacionais; mercado comum de energia na América do Sul. [[223]]']),
  f=dict(tags=['tse','nova'], items=[
   'Reaproximar o Brasil de EUA, Argentina e Israel. [[224,225]]',
   'Negociar com China, União Europeia e EUA "conforme o interesse brasileiro", sem afinidade ideológica. [[224]]',
   'Retomar a adesão à OCDE e buscar saída diplomática para sanções comerciais. [[224,225]]',
   'Segundo o SBT News, o plano não menciona o Mercosul. [[225]]']),
  note='Lula prioriza BRICS, Mercosul e Sul Global; Flávio prioriza EUA, Israel e OCDE.'),
 dict(id='previdencia', t='Previdência, INSS e salário mínimo',
  l=dict(tags=['tse','cont'], items=[
   'Manter a valorização real do salário mínimo, com efeito em aposentadorias e BPC. [[223,226]]',
   'Contribuição previdenciária mais flexível para quem alterna emprego e informalidade, incluindo trabalhadores de aplicativos. [[226]]',
   'Para idosos: Centros-Dia, atendimento domiciliar e mais vagas em instituições de longa permanência. [[226]]']),
  f=dict(tags=['tse','fala'], items=[
   'INSS mais digital, para reduzir o tempo de análise de benefícios. [[226]]',
   'Pacote antifraude e mais controle no crédito consignado contra descontos não autorizados. [[226]]',
   '"Casa Segura para Envelhecer": subsídio para adaptar casas de idosos de baixa renda. [[226]]',
   'Em março, o coordenador Rogério Marinho falou em nova reforma da Previdência; o tema não aparece no plano. [[227]]']),
  note='Nenhum dos dois planos, segundo as reportagens, detalha mudança em regras de aposentadoria. [[226]]'),
 dict(id='armas', t='Armas',
  l=dict(tags=['tse','cont'], items=[
   'Manter a política de controle de armas e munições. [[223]]',
   'Rastreabilidade de armas e câmeras corporais nas polícias. [[72,223]]']),
  f=dict(tags=['interp'], items=[
   'Análise da PUC-SP vê deslocamento da ênfase armamentista do governo Jair para combate a facções, vigilância e endurecimento penal. [[87]]']),
  note='Na pesquisa e nas reportagens consultadas, nenhum dos planos trata de aborto ou de política de drogas.'),
]

trajetoria = [
 dict(id='inicio', t='Início da carreira',
  l=dict(tags=['fato'], items=[
   'Presidente do Sindicato dos Metalúrgicos de São Bernardo e Diadema em 1975 (92% dos votos). [[90,93]]',
   'Liderou greves de 1978–1980; preso por 31 dias em 1980 (Lei de Segurança Nacional), depois absolvido pelo STM. [[90]]',
   'Um dos fundadores do PT (1980), fundação coletiva. [[90]]']),
  f=dict(tags=['fato'], items=[
   'Eleito deputado estadual no RJ em 2002, aos 21 anos, com 31.293 votos. [[113]]',
   'Quatro mandatos seguidos na Alerj (2003–2019). [[113]]',
   'Presidiu comissões de Segurança Pública, Legislação Constitucional e Defesa Civil. [[113]]'])),
 dict(id='eleicoes', t='Eleições e cargos',
  l=dict(tags=['fato'], items=[
   '1982: 4º lugar para governador de SP. 1986: deputado federal mais votado do país; constituinte. [[91,92]]',
   'Perdeu para presidente em 1989, 1994 e 1998. [[94]]',
   'Eleito presidente em 2002 e reeleito em 2006 (mandatos 2003–2010). [[91]]',
   'Eleito em 2022 com 50,83% dos válidos; 3º mandato desde 2023. [[95,89]]']),
  f=dict(tags=['fato'], items=[
   '2016: 4º lugar para prefeito do Rio (PSC), com 14% dos votos. [[116]]',
   '2018: senador pelo RJ (PSL), cerca de 4,37 milhões de votos (31,3%). [[115,116]]',
   'Em 2025, eleito presidente da Comissão de Segurança Pública do Senado. [[114]]']),
  ),
 dict(id='legislativo', t='Atuação legislativa e de governo',
  l=dict(tags=['fato','interp'], items=[
   'Governos 2003–2010: Fome Zero, Bolsa Família, valorização real do salário mínimo, resposta à crise de 2008. [[98]]',
   'Acadêmicos divergem na leitura desse período (ex.: "neodesenvolvimentismo"). São interpretações. [[98,99]]',
   ]),
  f=dict(tags=['fato','interp'], items=[
   'Contagens variam: a Folha não achou projeto de autoria própria virado lei até maio/2026; duas leis em coautoria. [[121]]',
   'Relator do projeto que restringiu a "saidinha" (Lei 14.843/2024). [[119,120]]',
   'Na Alerj, segurança foi o tema dominante em 68% dos discursos (levantamento independente). [[123]]',
   'De 2020 a 2026, indicou R$ 271 milhões em emendas empenhadas, concentradas em segurança. Empenho não é pagamento. [[121]]',
   'Análise da PUC-SP: relação mais próxima com o Centrão do que o governo Jair no início, e posição contrária à pena de morte. [[87]]']),
  note='Lula já exerceu a Presidência; Flávio teve carreira só no Legislativo.'),
]

juridico = [
 dict(id='processos', t='Situação jurídica (até 8/10/2026)',
  l=dict(tags=['anul','fato'], items=[
   'Lava Jato: condenado no triplex (2017) e no sítio; preso por <b>580 dias</b> (2018–2019). [[101,103,111,102]]',
   'Em 2021 o STF anulou as condenações (juízo incompetente) e declarou Moro parcial no triplex. [[104,105,106,107]]',
   'Anulação <b>não é absolvição</b> de mérito; os casos prescreveram. Não há condenação válida em vigor. [[108,109]]',
   'Comitê de Direitos Humanos da ONU (2022) apontou violação ao devido processo. [[110]]']),
  f=dict(tags=['anul','inv'], items=[
   'Rachadinhas: denunciado pelo MP-RJ em 2020; a denúncia foi rejeitada em 2022 porque o STF anulou as provas do Coaf. <b>Não é absolvição</b> de mérito; sem condenação. [[124,125,126,127,128]]',
   'Inquérito "Dark Horse" (STF, julho/2026): apura financiamento de filme sobre Jair Bolsonaro; sem denúncia. Flávio nega irregularidade. [[130,131,132]]',
   'Emenda de 2023 negociada com Robson Calixto: indícios apontados pelo TCU, apuração sob sigilo. Flávio diz que seguiu a lei. [[133]]',
   'Homenagens a Adriano da Nóbrega e familiares dele no gabinete: fatos documentados, sem decisão judicial contra Flávio. [[129]]']),
  note='Investigação, denúncia e anulação de provas não equivalem a culpa nem a inocência. Nenhum dos dois tinha condenação válida em vigor no corte. [[97,109,127]]'),
]

governos = [
 dict(id='gov-leis', t='Principais leis e reformas',
  l=dict(tags=['lei'], items=[
   'Regime Fiscal Sustentável (LC 200/2023), no lugar do teto de gastos. [[145]]',
   'Reforma tributária do consumo (EC 132/2023, promulgada pelo Congresso). [[146,147]]',
   'Volta do Bolsa Família (Lei 14.601/2023) e do Minha Casa, Minha Vida (Lei 14.620/2023). [[148,149]]',
   'Pé-de-Meia (2024), igualdade salarial (2023), novo ensino médio (2024). [[150,151,152]]',
   'Licenciamento ambiental (Lei 15.190/2025, controversa) e isenção de IR até R$ 5 mil (efeito em 2026). [[153,154]]']),
  f=dict(tags=['lei','pend'], items=[
   'Reforma da Previdência (EC 103/2019, promulgada pelo Congresso). [[1,3]]',
   'Liberdade Econômica (Lei 13.874/2019), autonomia do Banco Central (LC 179/2021), Marco das Startups. [[4,6,8]]',
   'Pacote anticrime (2019), Marco do Saneamento (2020), privatização da Eletrobras (2021–2022). [[9,21,23,24]]',
   'Auxílio Emergencial (criado pelo Congresso, sancionado em 2020) e Auxílio Brasil (2021). [[11,12,17]]',
   '<b>Não aprovados:</b> Future-se, reforma administrativa e homeschooling. [[37,38,39]]']),
  note='Sanção ou promulgação não é o mesmo que execução. Várias medidas nasceram no Congresso, não no Executivo.'),
 dict(id='gov-2022', t='Medidas temporárias e emergenciais',
  l=dict(tags=['lei'], items=[
   'Isenção de IR até R$ 5 mil (Lei 15.270/2025), com efeito a partir de 2026: aprovada no fim do mandato, sem resultado observado ainda. [[154]]']),
  f=dict(tags=['lei'], items=[
   'Auxílio Emergencial (2020): R$ 600 por mês; 29,4 milhões de domicílios (43%) receberam em junho de 2020. TCU estimou 7 milhões de pagamentos fora do público-alvo. [[12,13]]',
   'EC 123/2022 (promulgada pelo Congresso): +R$ 200 no Auxílio Brasil, R$ 1.000 a caminhoneiros e auxílio a taxistas, só entre agosto e dezembro de 2022. [[18]]']),
  note='As medidas de 2020 e 2022 ajudam a explicar por que esses anos são atípicos nos indicadores de pobreza e fiscais. [[14,18]]'),
 dict(id='gov-contro', t='Pontos de controvérsia no período',
  l=dict(tags=['fato'], items=[
   'Lei de licenciamento ambiental: debate público sobre o alcance das simplificações e riscos ambientais. [[153]]',
   'A lista é seletiva: a pesquisa não traz inventário completo de execução do Lula III.']),
  f=dict(tags=['fato','interp','inv'], items=[
   'Pandemia: TCU apontou demora em compras de vacinas; CPI recomendou indiciamento de Bolsonaro (CPI não é sentença). [[15,16]]',
   'Armas: flexibilização por decretos, parte suspensa pelo STF. [[34]]',
   'Meio ambiente: Observatório do Clima estima alta de ~60% no desmatamento médio (avaliação da sociedade civil). [[31]]'])),
]

# ---------------- INDICATORS ----------------
years = ['2019','2020','2021','2022','2023','2024','2025']
ind = [
 ('PIB real (variação anual, %)', ['1,2','-3,3','4,8','3,0','3,2','3,4','2,3'], '1,4', '3,0', 'até 2º tri; sem anual', [42,44]),
 ('IPCA (acumulado no ano, %)', ['4,31','4,52','10,06','5,79','4,62','4,83','4,26'], '6,17', '4,57', '3,11 até ago.', [45,46]),
 ('Desocupação (média anual, %)', ['11,8','13,8','13,2','9,6','7,8','6,6','5,6'], '12,1', '6,7', '—', [47,48,49]),
 ('Pobreza (US$ 6,85 PPC/dia, %)', ['32,6','31,1','36,8','31,6','27,3','23,1','—'], '', '', '—', [50,51]),
 ('Extrema pobreza (US$ 2,15 PPC/dia, %)', ['7,4','6,1','9,0','5,9','4,4','3,5','—'], '', '', '—', [50,51]),
 ('Desmatamento PRODES (km²)', ['10.129','10.851','13.038','11.594','9.064','6.518','5.731'], '', '', 'sem taxa', [53,54]),
 ('Tríplice viral D1 (cobertura, %)', ['93,1','79,5','74,8','80,7','86,9','95,7','92,9'], '', '', '—', [55,57,58]),
 ('Mortes violentas (MVI por 100 mil)', ['23,0','24,1','23,0','22,7','21,9','20,8','19,1'], '', '', '—', [60,61]),
 ('Dívida bruta (DBGG, % do PIB, dez.)', ['74,44','86,94','77,31','71,68','73,83','76,27','78,64'], '', '', '82,86 em ago.', [63]),
 ('Resultado primário do Governo Central (% do PIB)', ['-1,29','-9,77','-0,39','+0,46','-2,09','-0,36','-0,48'], '', '', 'sem anual', [64,65]),
 ('Desigualdade (índice de Gini)', ['0,543','—','—','—','—','0,504','0,511'], '', '', '—', [51,52]),
]
def ind_table():
    head = ''.join(f'<th class="y{" lula" if y>="2023" else " bolso"}">{y}</th>' for y in years)
    rows = ''
    for name, vals, a, b, y26, rf in ind:
        tds = ''.join(f'<td class="{"p2" if i>=4 else "p1"}">{v}</td>' for i, v in enumerate(vals))
        rows += f'<tr><th scope="row">{name} {R("[["+",".join(map(str,rf))+"]]")}</th>{tds}<td class="p3">{y26}</td></tr>'
    return (f'<div class="tablewrap"><table><thead><tr><th>Indicador</th>{head}<th>2026*</th></tr>'
            f'<tr class="band"><th></th><th colspan="4" class="band-b">Governo Jair Bolsonaro</th><th colspan="3" class="band-l">Governo Lula III</th><th></th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

medias = [
 ('PIB real, média anual', '3,0%', '1,4%', [42,44]),
 ('Desocupação, média', '6,7%', '12,1%', [47,49]),
 ('IPCA, média anual', '4,57%', '6,17%', [45]),
 ('Pobreza (último ano)', '23,1% (2024)', '31,6% (2022)', [51]),
 ('Desmatamento (último ano)', '5.731 km² (2025)', '11.594 km² (2022)', [54]),
 ('Dívida bruta (dez. do último ano)', '78,64% do PIB (2025)', '71,68% do PIB (2022)', [63]),
]
def medias_html():
    out = ''
    for n, l, f, rf in medias:
        out += (f'<div class="mrow"><div class="mname">{n} {R("[["+",".join(map(str,rf))+"]]")}</div>'
                f'<div class="mval mval-l"><span class="who who-l">Lula III · 2023–2025</span><b>{l}</b></div>'
                f'<div class="mval mval-f"><span class="who who-f">Jair Bolsonaro · 2019–2022</span><b>{f}</b></div></div>')
    return out

def section(sid, eyebrow, title, intro, rows):
    return (f'<section class="sec" id="{sid}"><header class="sechead"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>'
            f'{"<p class=lede>"+R(intro)+"</p>" if intro else ""}</header>{"".join(row(r) for r in rows)}</section>')

# ---------- 2º turno ----------
UF = {  # uf: (col,row, winner, pct)
 'RR':(1,0,'f','71,06'),'AP':(3,0,'l','45,71'),
 'AM':(1,1,'l','48,23'),'PA':(2,1,'l','49,91'),'MA':(3,1,'l','63,99'),'CE':(4,1,'l','63,29'),'RN':(5,1,'l','59,75'),
 'AC':(0,2,'f','64,56'),'RO':(1,2,'f','67,45'),'TO':(2,2,'f','50,44'),'PI':(3,2,'l','70,99'),'PE':(4,2,'l','63,45'),'PB':(5,2,'l','61,31'),
 'MT':(1,3,'f','65,15'),'GO':(2,3,'f','53,60'),'BA':(3,3,'l','66,17'),'SE':(4,3,'l','62,75'),'AL':(5,3,'l','54,73'),
 'MS':(1,4,'f','58,60'),'DF':(2,4,'f','51,31'),'MG':(3,4,'f','48,24'),'ES':(4,4,'f','54,78'),
 'SP':(2,5,'f','51,93'),'RJ':(3,5,'f','53,01'),
 'PR':(2,6,'f','59,91'),'SC':(2,7,'f','66,65'),'RS':(2,8,'f','55,64'),
}
UF2_L = {'AL','AP','AM','BA','CE','MA','MG','PA','PB','PE','PI','RN','SE'}
UF2_PCT = {'MG':'50,43','PI':'75,88','RR':'72,46','SP':'53,85'}
def ufmap2():
    tiles=''
    for u,(c,r,w,p) in UF.items():
        w2='l' if u in UF2_L else 'f'; nome='Lula' if w2=='l' else 'Flávio'; pc=UF2_PCT.get(u)
        tiles+=f'<div class="uf uf2 uf-{w2}" style="grid-column:{c+1};grid-row:{r+1}" title="{u}: venceu {nome}{(" com "+pc+"%") if pc else ""}"><b>{u}</b><span>{(pc+"%") if pc else nome}</span></div>'
    return f'<div class="ufmap" role="img" aria-label="Mapa de estados vencidos no 2º turno: Lula em 13 estados, Flávio em 13 estados e no DF">{tiles}</div>'
def ufmap():
    tiles = ''.join(f'<div class="uf uf-{w}" style="grid-column:{c+1};grid-row:{r+1}" title="{u}: venceu {"Lula" if w=="l" else "Flávio"} com {p}%"><b>{u}</b><span>{p}%</span></div>' for u,(c,r,w,p) in UF.items())
    return f'<div class="ufmap" role="img" aria-label="Mapa de estados vencidos no 1º turno">{tiles}</div>'

turno2 = [
 dict(id='estados', t='Onde cada um venceu no 1º turno',
  l=dict(tags=['fato'], items=[
   'Venceu em <b>12 estados</b>: os 9 do Nordeste, mais Pará, Amazonas e Amapá. [[205,206]]',
   'Maiores votações: Piauí (70,99%), Bahia (66,17%) e Maranhão (63,99%). [[205]]']),
  f=dict(tags=['fato'], items=[
   'Venceu em <b>14 estados e no DF</b>: todo o Sul, Sudeste e Centro-Oeste, mais Acre, Rondônia, Roraima e Tocantins. [[205,206]]',
   'Maiores votações: Roraima (71,06%), Rondônia (67,45%) e Santa Catarina (66,65%). [[205]]'])),
 dict(id='apoios', t='Apoios declarados para o 2º turno (até 11/10)',
  l=dict(tags=['fato'], items=[
   '<b>PCB e PSTU</b> (7/10): "voto crítico" em Lula contra a volta dos Bolsonaro, sem apoio a um eventual governo. [[285]]',
   '<b>Unidade Popular</b> (11/10), sem integrar formalmente a campanha. [[286]]',
   'Até 11/10, não havia registro de apoio de partidos de centro ou de direita a Lula nas fontes consultadas. [[287]]']),
  f=dict(tags=['fato'], items=[
   '<b>PP e União Brasil</b> (6/10), que antes estavam neutros. [[207]]',
   '<b>Republicanos</b> (7/10), <b>Novo</b>, <b>Podemos</b> e 17 diretórios estaduais do <b>MDB</b>. [[208,287]]',
   'Ex-candidatos Augusto Cury (Avante, 3º colocado, em 8/10), Ronaldo Caiado (PSD), Romeu Zema (Novo) e Clariana Barão (DC). [[287,208,209,210]]']),
  note='Renan Santos (Missão) descartou apoiar Lula ou Flávio. Apoio de partido ou candidato não transfere votos automaticamente. [[208,286]]'),
 dict(id='pesquisas', t='Pesquisas do 2º turno (até 22/10)',
  l=dict(tags=['fato'], items=[
   'Datafolha (20 a 22/10): <b>50%</b> dos válidos; 46% do total. [[305,306]]',
   'Quaest (17 a 20/10): <b>44%</b> do total. [[307]]']),
  f=dict(tags=['fato'], items=[
   'Datafolha (20 a 22/10): <b>50%</b> dos válidos; 47% do total. [[305,306]]',
   'Quaest (17 a 20/10): <b>45%</b> do total. [[307]]']),
  note='Empate técnico nas duas. Datafolha: 2.520 entrevistas, margem de 2 pontos, registro BR-09709/2026; brancos e nulos 5%, indecisos 2%. Quaest: 2.154 entrevistas, margem de 2 pontos, registro BR-08535/2026; brancos e nulos 9%, indecisos 2%. Na rodada anterior (divulgada em 14 e 15/10), o Datafolha tinha Flávio com 51% e Lula com 49% dos válidos, e a Quaest, 46% a 44% do total. "Válidos" exclui brancos, nulos e indecisos; "total" os inclui. Pesquisa é retrato do momento, não previsão. [[305,306,307,301]]'),
]
debates = '''<div class="debates"><h3>Debates do 2º turno</h3><ul>
<li class="cancel"><b>11/10</b><span>Record · <strong>cancelado</strong> em 9/10, por conflito de agendas</span></li>
<li><b>18/10</b><span>Band · <strong class="ok">realizado</strong>, com os dois</span></li>
<li><b>23/10</b><span>Globo · <strong class="ok">realizado</strong>, com os dois</span></li></ul>
<p class="small"><b>Como foi o da Band:</b> Flávio disse que nomearia Cláudio Lottenberg, presidente do Hospital Albert Einstein, ministro da Saúde, para levar um "padrão Einstein" ao SUS; Lula perguntou se ele pretende privatizar o sistema. Em segurança, Flávio repetiu facções como narcoterroristas e 500 mil vagas em presídios; Lula, o Ministério da Segurança. Flávio disse ter votado pelo fim da 6x1 depois de ouvir trabalhadores. Lula desafiou Flávio a abrir os sigilos bancário e telefônico e citou Vorcaro e o caso Marielle; Flávio citou o filho de Lula e as fraudes no INSS, que começaram no governo de Jair Bolsonaro. Não houve debates entre os dois no 1º turno. ''' + R('[[308,309,214,289]]') + '</p>' + '<p class="small"><b>Como foi o da Globo:</b> Flávio cobrou obras paradas, poder de compra, filas no SUS e o endividamento das famílias; Lula defendeu a valorização do salário mínimo, o PAC e o Desenrola, e atribuiu ao governo Bolsonaro mortes na pandemia. Discutiram também segurança, o marco do saneamento e o filme sobre Jair Bolsonaro. Nas considerações finais, Lula pediu desculpas pelo tom e disse que o eleitor escolheria entre manter "a democracia funcionando" ou ter "um miliciano governando este país"; Flávio negou ser investigado por relação com milícias e prometeu combatê-las. ' + R('[[320]]') + '</p></div>'

def sec_turno2():
    return (f'<section class="sec" id="turno2"><header class="sechead"><span class="eyebrow">Rumo a 25/10</span><h2>O 2º turno</h2>'
            f'<p class="lede">Dados de reportagens publicadas até 8/10/2026. Pesquisas e apoios mudam rápido: confira as fontes antes de compartilhar.</p></header>'
            f'<article class="row"><h3>Mapa do 1º turno</h3><div class="mapwrap">{ufmap()}<div class="maplegend"><span class="lg-l">Lula venceu</span><span class="lg-f">Flávio venceu</span><span class="small">% dos válidos do vencedor no estado</span></div></div></article>'
            + ''.join(row(r) for r in turno2) + debates + '</section>')

# ---------- Congresso ----------
camara = [('PL',121),('PT',70),('União',46),('PSD',43),('PP',41),('Republicanos',41),('MDB',36),('Podemos',27),('PSB',15),('PSOL',14),('PCdoB',11),('PSDB',11),('Novo',10),('PV',7),('PDT',6),('Avante',5),('PRD',5),('Solidariedade',2),('Rede',1),('Missão',1)]
def sec_congresso():
    mx = 121
    bars = ''.join(f'<div class="cb" role="listitem" aria-label="{p}: {n} cadeiras"><span class="cbn" aria-hidden="true">{p}</span><span class="cbt"><span class="cbf{" cb-l" if p=="PT" else " cb-f" if p=="PL" else ""}" style="width:{n/mx*100:.1f}%"></span></span><span class="cbv" aria-hidden="true">{n}</span></div>' for p,n in camara)
    return f'''<section class="sec" id="congresso"><header class="sechead"><span class="eyebrow">Congresso eleito · posse em fev/2027</span><h2>Quem vai votar as propostas</h2>
<p class="lede">Muitas propostas dos dois planos dependem de PEC, que exige <b>308 dos 513 deputados</b> e <b>49 dos 81 senadores</b>, em dois turnos em cada Casa. {R("[[204]]")} Nenhum partido terá maioria sozinho. {R("[[202]]")}</p></header>
<div class="congress"><div><h3>Câmara: cadeiras por partido</h3><div class="cbars" role="list">{bars}</div>
<p class="small">PL (partido de Flávio) e PT (partido de Lula) em destaque. Federações: Brasil da Esperança (PT, PCdoB, PV) soma 88; União Progressista (União, PP), 87. {R("[[201,202,203]]")}</p></div>
<div><h3>Senado: maiores bancadas</h3><div class="sen">
<div><b class="t-f">28</b><span>PL</span></div><div><b>11</b><span>União Progressista</span></div><div><b class="t-l">9</b><span>PT</span></div><div><b>8</b><span>MDB</span></div></div>
<p class="small">Soma eleitos em 2026 e senadores com mandato em curso. Contagens das demais bancadas variam entre veículos. {R("[[202,203]]")}</p></div></div>
<p class="note">Partidos não votam em bloco fixo: o alinhamento ao futuro governo depende de negociação, inclusive entre legendas que hoje apoiam um ou outro candidato.</p></section>'''


def leg_card(c):
    insts=''.join(f'<span class="inst {INST[i][2]}"><b>{INST[i][0]}</b>{INST[i][1]}</span>' for i in c['inst'])
    parts=f'<h4>{c["t"]}</h4><div class="insts">{insts}</div><p class="st">{R(c["status"])}</p>'
    if c.get('obst'): parts+=f'<p class="obst"><b>Obstáculo jurídico</b>{R(c["obst"])}</p>'
    if c.get('pro') or c.get('contra'):
        parts+='<div class="pc">'
        if c.get('pro'): parts+=f'<p class="pro"><b>Argumentos a favor</b>{R(c["pro"])}</p>'
        if c.get('contra'): parts+=f'<p class="con"><b>Argumentos contra</b>{R(c["contra"])}</p>'
        parts+='</div>'
    return f'<div class="lcard">{parts}</div>'
def sec_legal():
    rows=''
    for r in LEG:
        L=''.join(leg_card(c) for c in r['l']); F=''.join(leg_card(c) for c in r['f'])
        rows+=(f'<article class="row" id="{r["id"]}"><h3>{r["t"]}</h3><div class="pair">'
               f'<div class="cell cell-l"><span class="who who-l">Lula</span>{L}</div>'
               f'<div class="cell cell-f"><span class="who who-f">Flávio Bolsonaro</span>{F}</div></div></article>')
    legend=''.join(f'<div class="lg"><span class="inst {v[2]}"><b>{v[0]}</b></span><span>{v[1]}</span></div>' for v in INST.values())
    return (f'<section class="sec" id="baselegal"><header class="sechead"><span class="eyebrow">Na prática</span><h2>O que cada proposta exige e o que pode causar</h2>'
            f'<p class="lede">Para as propostas de maior impacto: o tipo de norma necessária, onde ela está no Congresso, se esbarra em decisão do STF ou na Constituição, e os argumentos e efeitos apontados a favor e contra. As opiniões são atribuídas às fontes; a página não indica qual lado tem razão.</p></header>'
            f'<div class="legend instlegend">{legend}</div>{rows}'
            f'<p class="note">O plano de Lula se concentra em manter ou ampliar políticas que já existem em lei, por isso tem menos itens que exigem norma nova. O de Flávio propõe mais mudanças constitucionais e penais, que exigem quórum maior no Congresso.</p></section>')

T='<b class="grp">Trabalhadores:</b> '
E_='<b class="grp">Empresas:</b> '
efeitos = [
 dict(id='ef-jornada', t='Jornada e contratação',
  l=dict(tags=['cond'], items=[
   'Fim da 6x1 e 40 horas sem corte de salário (promulgado em 16/10/2026: EC 141). [[296]]',
   T+'dois dias de folga por semana e menos horas para quem tem carteira assinada. [[229]]',
   E_+'Ipea estima custo extra médio de 7,8% com mão de obra e cerca de 1% no custo total de comércio e indústria; CNI projeta preços 6,2% mais altos em média e −0,7% no PIB; CNC estima +21% na folha. [[230]]',
   'Firmas com até 9 empregados (cerca de 25% dos formais) podem precisar de apoio na transição, segundo o Ipea. [[230]]']),
  f=dict(tags=['tse','fala'], items=[
   'Contratos de menor custo para jovens de 18–24 anos e pessoas 50+; jornada por hora e negociado sobre o legislado. [[83,86]]',
   E_+'contratar fica mais barato e a jornada mais flexível; o plano aposta em mais vagas. [[83]]',
   T+'no precedente de 2019 (Contrato Verde e Amarelo), o modelo reduzia FGTS e multa rescisória; o DIEESE diz que desonerar a folha teve efeito pequeno ou nulo no emprego. [[231]]',
   'Críticos da jornada por hora dizem que o trabalhador tem pouco poder de negociação. [[228]]'])),
 dict(id='ef-impostos', t='Impostos',
  l=dict(tags=['lei'], items=[
   'Isenção de IR até R$ 5 mil, com desconto decrescente até R$ 7.350, em vigor desde 2026. [[154]]',
   T+'quem ganha até R$ 5 mil por mês deixa de pagar IR. [[154]]',
   E_+'a compensação vem da tributação mínima de altas rendas, que pode atingir sócios e donos de empresa de renda alta. [[154]]']),
  f=dict(tags=['tse','fala'], items=[
   'Reduzir o IVA e as exceções da reforma tributária; em fala, citou 20%. [[81,83]]',
   E_+'setores hoje com alíquota cheia, como serviços, pagariam menos. [[235,236]]',
   T+'como consumidores, especialistas dizem que itens da cesta básica e remédios, hoje com alíquota menor, podem ficar mais caros. [[235]]',
   'Menos imposto sobre energia e combustíveis beneficia empresas e consumidores. [[81]]'])),
 dict(id='ef-renda', t='Renda e proteção social',
  l=dict(tags=['cont','cond'], items=[
   T+'salário mínimo com ganho real de 0,6% a 2,5% ao ano até 2030, com efeito em aposentadorias e BPC. [[233,226]]',
   T+'trabalhadores de aplicativo teriam acesso a aposentadoria e cobertura por acidente e maternidade. [[226]]',
   E_+'as plataformas passariam a contribuir; não há estimativa de custo nas fontes consultadas.',
   'Cada R$ 1 a mais no mínimo custa cerca de R$ 392 milhões aos cofres públicos. [[233]]']),
  f=dict(tags=['tse'], items=[
   T+'programas sociais mantidos, mas usados como ponte para qualificação e emprego; proibição de usar benefícios em apostas. [[81,88]]',
   T+'"Ganha-Ganha" voluntário: emprego formal e pagamento em dia rendem juros menores e crédito. [[81,88]]',
   'Não detalha mudança no salário mínimo; o coordenador da campanha falou em nova reforma da Previdência, que não está no plano. [[227]]'])),
 dict(id='ef-negocios', t='Custo de investir e Estado',
  l=dict(tags=['cont'], items=[
   E_+'mantém concessões, leilões e o Novo PAC com investimento privado. [[69,76]]',
   'O plano não traz proposta específica de licenciamento ambiental, segundo análise independente. [[75]]']),
  f=dict(tags=['tse'], items=[
   E_+'privatizações, licenciamento mais rápido (licença por decurso de prazo) e R$ 900 bi em infraestrutura via PPPs e concessões. [[81,82,88]]',
   'Tesouraço: corte de ministérios, cargos e supersalários atinge servidores do topo, não o setor privado. [[81]]',
   'Não há estimativa de efeito sobre emprego ou meio ambiente nas fontes consultadas.'])),
]
def sec_efeitos():
    return (f'<section class="sec" id="efeitos"><header class="sechead"><span class="eyebrow">Quem ganha, quem paga</span><h2>Efeitos para trabalhadores e empresas</h2>'
            f'<p class="lede">Efeitos projetados pelas fontes, não resultados garantidos. Os grupos não são homogêneos: o impacto muda entre formais e informais e entre empresas pequenas e grandes.</p></header>'
            + ''.join(row(r) for r in efeitos) +
            '<div class="leitura"><h3>Leitura geral</h3><div class="pair">'
            '<p><b class="t-l">Lula</b> concentra medidas que transferem renda ou direitos a assalariados de renda baixa e média, com custo maior para empresas, sobretudo pequenas, e para quem tem renda alta.</p>'
            '<p><b class="t-f">Flávio</b> concentra medidas que reduzem custos e regras para quem contrata e investe, apostando em mais emprego, com menos proteção legal para parte dos trabalhadores.</p></div>'
            '<p class="small">Nos dois casos, há especialistas que contestam a promessa central: os efeitos negativos sobre a economia (Lula) ou o ganho de emprego (Flávio). O resultado final depende do Congresso e do desenho de cada medida.</p></div></section>')


import sys; sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
from impacto import IMP, INST2, LINKS
from escandalos import ESC, ESC_REFS, STAGES, ESC_REL
for k,(t,u) in ESC_REFS.items(): refs[k]={'t':t,'u':u}

# ---------- limpeza de dados ----------
DROP_TAGS = {'fato', 'nova', 'pend'}
def clean_tags(lst):
    for r in lst:
        for k in ('l','f'):
            r[k]['tags'] = [t for t in r[k].get('tags', []) if t not in DROP_TAGS]
for lst in (perfil, propostas, trajetoria, juridico, governos, turno2):
    clean_tags(lst)

PR = {r['id']: r for r in propostas}
# Armas -> Segurança ; Previdência -> Proteção social
PR['seguranca']['l']['items'] += PR['armas']['l']['items']
PR['seguranca']['f']['items'] += PR['armas']['f']['items']
PR['seguranca']['f']['tags'] = PR['seguranca']['f']['tags'] + ['interp']
PR['social']['t'] = 'Proteção social, Previdência e idosos'
PR['social']['l']['items'] = PR['social']['l']['items'] + PR['previdencia']['l']['items']
PR['social']['f']['items'] += PR['previdencia']['f']['items']
PR['social']['f']['tags'] = PR['social']['f']['tags'] + ['fala']
PR['social']['note'] = PR['previdencia']['note']
propostas = [r for r in propostas if r['id'] not in ('armas', 'previdencia')]
# notas de comparação que só repetiam as colunas
for k in ('economia', 'trabalho', 'instituicoes', 'externa'):
    PR[k]['note'] = None
PR['seguranca']['note'] = 'Lula enfatiza coordenação e prevenção; Flávio, endurecimento penal e vigilância. [[72,81]]'
for r in trajetoria:
    if r['id'] == 'legislativo': r['note'] = None
P = {r['id']: r for r in perfil}
P['plano']['note'] = None
# gov-2022: tirar a repetição da isenção de IR
G = {r['id']: r for r in governos}
G['gov-2022']['l']['items'] = [
  'EC 126/2022, a "PEC da Transição" (promulgada pelo Congresso em 21/12/2022, antes da posse): R$ 145 bi fora do teto de gastos só em 2023, dos quais R$ 70 bi para manter o Bolsa Família em R$ 600. [[294]]',
  'Auxílio Reconstrução (2024): R$ 5.100 em parcela única para famílias desalojadas ou desabrigadas pelas enchentes no Rio Grande do Sul. [[295]]']
G['gov-2022']['l']['tags'] = ['lei']
G['gov-leis']['note'] = None

# links do catálogo para a análise
def add_links(items):
    out = []
    for it in items:
        for pat, cid in LINKS:
            if pat in it:
                it = it + f' <a class="golink" href="#{cid}">ver análise ↓</a>'
                break
        out.append(it)
    return out
for r in propostas:
    for k in ('l','f'):
        r[k]['items'] = add_links(r[k]['items'])

def cell(who, c):
    items = ''.join(f'<li>{R(i)}</li>' for i in c['items'])
    tg = c.get('tags', [])
    ch = f'<div class="chips">{chips(tg)}</div>' if tg else ''
    return (f'<div class="cell cell-{who}"><span class="who who-{who}">{"Lula" if who=="l" else "Flávio Bolsonaro"}</span>{ch}<ul>{items}</ul></div>')
def row(r):
    note = f'<p class="note">{R(r["note"])}</p>' if r.get('note') else ''
    return (f'<article class="row" id="{r["id"]}"><h3>{r["t"]}</h3><div class="pair">{cell("l", r["l"])}{cell("f", r["f"])}</div>{note}</article>')

def open_sec(sid, eyebrow, title, intro='', cls=''):
    return (f'<section class="sec {cls}" id="{sid}"><header class="sechead"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>'
            f'{"<p class=lede>"+R(intro)+"</p>" if intro else ""}</header>')

def benef(c):
    chips=lambda xs,cls: ''.join(f'<span class="bchip {cls}">{x}</span>' for x in xs)
    if not c.get('gan') and not c.get('pag'):
        return '<p class="benef benef-none">Muda regras: não transfere dinheiro diretamente para um grupo nem cobra de outro.</p>'
    h='<div class="benef">'
    if c.get('gan'): h+=f'<div class="bf"><span class="bf-l">Quem ganha</span><span class="bf-c">{chips(c["gan"],"b-g")}</span></div>'
    if c.get('pag'): h+=f'<div class="bf"><span class="bf-l">Quem paga</span><span class="bf-c">{chips(c["pag"],"b-p")}</span></div>'
    return h+'</div>'
def benef_resumo():
    def col(side):
        items=''.join(f'<li><a href="#{c["id"]}">{c["t"]}</a><span class="bf-c">{"".join(f"<span class=\"bchip b-g\">{x}</span>" for x in c["gan"])}</span></li>'
                      for g in IMP for c in g[side] if c.get('gan'))
        return f'<ul class="bres">{items}</ul>'
    return ('<article class="row" id="quem-ganha"><h3>Quem ganha com cada proposta</h3>'
            '<p class="note" style="margin:0 0 12px">Resumo dos cartões abaixo. Propostas que só mudam regras (segurança, instituições) não aparecem aqui. Toque na proposta para ver quem paga a conta e as fontes.</p>'
            f'<div class="pair"><div class="cell cell-l"><span class="who who-l">Lula</span>{col("l")}</div>'
            f'<div class="cell cell-f"><span class="who who-f">Flávio Bolsonaro</span>{col("f")}</div></div></article>')
def imp_card(c):
    insts = ''.join(f'<span class="inst {INST2[i][1]}"><b>{INST2[i][0]}</b></span>' for i in c['inst'])
    h = f'<div class="lcard" id="{c["id"]}"><h4>{c["t"]}</h4>{benef(c)}<div class="insts">{insts}</div><p class="st">{R(c["status"])}</p>'
    if c.get('ganha') or c.get('paga'):
        h += '<div class="gp">'
        if c.get('ganha'): h += f'<p class="gp-g"><b>Quem ganha</b>{R(c["ganha"])}</p>'
        if c.get('paga'): h += f'<p class="gp-p"><b>Quem paga</b>{R(c["paga"])}</p>'
        h += '</div>'
    if c.get('obst'): h += f'<p class="obst"><b>Obstáculo jurídico</b>{R(c["obst"])}</p>'
    if c.get('pro') or c.get('contra'):
        h += '<div class="pc">'
        if c.get('pro'): h += f'<p class="pro"><b>Argumento a favor</b>{R(c["pro"])}</p>'
        if c.get('contra'): h += f'<p class="con"><b>Argumento contra</b>{R(c["contra"])}</p>'
        h += '</div>'
    return h + '</div>'

camara_top = [(p,n) for p,n in camara if n >= 10]
outros = sum(n for p,n in camara if n < 10)
def congresso_block():
    mx = 121
    bars = ''.join(f'<div class="cb" role="listitem" aria-label="{p}: {n} cadeiras"><span class="cbn" aria-hidden="true">{p}</span><span class="cbt"><span class="cbf{" cb-l" if p=="PT" else " cb-f" if p=="PL" else ""}" style="width:{n/mx*100:.1f}%"></span></span><span class="cbv" aria-hidden="true">{n}</span></div>' for p,n in camara_top)
    bars += f'<div class="cb" role="listitem" aria-label="Outros 7 partidos: {outros} cadeiras"><span class="cbn" aria-hidden="true">7 outros</span><span class="cbt"><span class="cbf" style="width:{outros/mx*100:.1f}%"></span></span><span class="cbv" aria-hidden="true">{outros}</span></div>'
    return (f'<div class="congress"><div><h3>Câmara eleita: cadeiras por partido</h3><div class="cbars" role="list">{bars}</div>'
            f'<p class="small">PL (de Flávio) e PT (de Lula) em destaque. "7 outros" são PV 7, PDT 6, Avante 5, PRD 5, Solidariedade 2, Rede 1 e Missão 1. Federações: Brasil da Esperança (PT, PCdoB, PV) soma 88; União Progressista (União, PP), 87. {R("[[201,202,203]]")}</p></div>'
            '<div><h3>Senado: maiores bancadas</h3><div class="sen">'
            '<div><b class="t-f">28</b><span>PL</span></div><div><b>11</b><span>União Progressista</span></div><div><b class="t-l">9</b><span>PT</span></div><div><b>8</b><span>MDB</span></div></div>'
            f'<p class="small">Soma eleitos em 2026 e senadores com mandato em curso; as demais bancadas variam entre veículos. Nenhum partido terá maioria sozinho. {R("[[202,203]]")}</p></div></div>')

def esc_card(c):
    steps=''.join(f'<li class="{"on" if i<=c["etapa"] else ""}{" cur" if i==c["etapa"] else ""}"><span>{st}</span></li>' for i,st in enumerate(STAGES))
    def blk(lbl,txt,cls=''): return f'<div class="eb {cls}"><dt>{lbl}</dt><dd>{R(txt)}</dd></div>' if txt else ''
    return (f'<article class="esc" id="{c["id"]}"><header><h4>{c["t"]}</h4><span class="eper">{c["periodo"]}</span></header>'
            f'<div class="ewt"><span class="ewl">Etapa mais grave alcançada</span><ol class="stages" aria-label="Etapa: {STAGES[c["etapa"]]}">{steps}</ol>'
            f'<span class="esit {c["sit_cls"]}">{c["situacao"]}</span></div>'
            f'<dl>{blk("Ligação com o candidato",c.get("quem"),"eb-quem")}{blk("O que é",c["oque"])}{blk("O que está comprovado",c["comprovado"])}{blk("O que mudou ou segue em aberto",c["aberto"])}'
            f'{blk("Consequências",c["consequencias"])}{blk("Culpa reconhecida pela Justiça?",c["culpa"],"eb-culpa")}{blk("O que diz o candidato",c["diz"])}</dl></article>')
def esc_pair(d, ll='Lula', lf='Flávio Bolsonaro', cls=''):
    L=''.join(esc_card(c) for c in d['l']); F=''.join(esc_card(c) for c in d['f'])
    return (f'<div class="pair escpair {cls}"><div class="cell cell-l"><span class="who who-l">{ll}</span>{L}</div>'
            f'<div class="cell cell-f"><span class="who who-f">{lf}</span>{F}</div></div>')
def sec_escandalos():
    return (open_sec('escandalos', 'Escândalos', 'Escândalos e investigações',
            'O peso de cada caso é medido pela <b>etapa mais grave que alcançou na Justiça</b> (fatos ou reportagens, investigação, denúncia, condenação) e pelas consequências concretas, não por avaliação da página. Investigação e denúncia não são culpa; anulação e rejeição de denúncia não são absolvição.')
            + '<h3 class="subhead" id="esc-diretos">Casos que envolvem os candidatos</h3>'
            + '<p class="lede sublede">Casos em que o próprio candidato ou pessoas próximas a ele foram investigados, acusados ou julgados.</p>'
            + esc_pair(ESC)
            + '<p class="note">Situação até 11/10/2026. Nenhum dos dois candidatos tinha condenação criminal válida em vigor nessa data. ' + R('[[97,109,127]]') + '</p>'
            + '<h3 class="subhead" id="esc-relacionados">Escândalos relacionados</h3>'
            + '<p class="lede sublede">Casos dos governos de referência de cada candidato: os do PT (Lula e Dilma Rousseff) e o de Jair Bolsonaro, pai de Flávio. <b>Não acusam os candidatos</b>; mostram o histórico dos grupos políticos que eles representam. É uma seleção dos casos de maior repercussão, não uma lista completa.</p>'
            + esc_pair(ESC_REL, 'Governos do PT (Lula e Dilma)', 'Governo Jair Bolsonaro', 'rel')
            + '</section>')

body = ''
# 1. Resultado
resultado = dict(id='resultado', t='Resultado do 2º turno (25/10/2026)',
  l=dict(tags=['fato'], items=[
   '<span class="res-tag">Reeleito</span><span class="res-num">51,79%</span><span class="res-sub">64.256.232 votos válidos</span> [[310]]',
   'Venceu em <b>13 estados</b>: os 9 do Nordeste, mais Pará, Amazonas, Amapá e Minas Gerais. Em relação a 2022, ganhou o Amapá e perdeu o Tocantins. [[313,312]]',
   'Discurso da vitória: agradeceu à juventude, aos idosos e às mulheres; prometeu regular as plataformas digitais, cobrar impostos das grandes empresas de tecnologia e ampliar a participação popular no governo. [[318]]']),
  f=dict(tags=['fato'], items=[
   '<span class="res-num">48,21%</span><span class="res-sub">59.826.041 votos válidos</span> [[310]]',
   'Venceu em <b>13 estados e no DF</b>: todo o Sul, Sudeste (menos Minas) e Centro-Oeste, mais Acre, Rondônia, Roraima e Tocantins. Em São Paulo teve 53,85%. [[313,312,314]]',
   'Não reconheceu o resultado: chamou-o de "inaceitável" e disse que pedirá a anulação, alegando que a prorrogação do horário de votação quebrou a isonomia entre os estados. Até a última atualização, não havia decisão judicial sobre o pedido. [[317]]']),
  note='Diferença de cerca de 4,4 milhões de votos. Compareceram 128,2 milhões de eleitores; a abstenção ficou em cerca de 19,2%, abaixo dos 21,08% do 1º turno. O TSE declarou Lula reeleito às 21h08. A posse será em 5/1/2027, primeira vez nessa data, pela Emenda Constitucional 111/2021. As últimas pesquisas, de 23 e 24/10, davam empate técnico, com Flávio numericamente à frente (51% a 49% dos válidos no Datafolha e na Quaest; 50,8% a 49,2% na AtlasIntel). [[310,311,319,321]]')
prorrog = dict(id='prorrogacao', t='Prorrogação do horário de votação',
  l=dict(tags=['fato'], items=[
   'A coligação de Lula pediu a prorrogação alegando que prefeituras da Bahia e de São Paulo reduziram a frota de ônibus no domingo; em Salvador, o secretário de mobilidade foi preso por ordem da Justiça Eleitoral. [[315]]']),
  f=dict(tags=['fato'], items=[
   'Antes da decisão, a campanha de Flávio também pediu ao TSE prorrogação em municípios de SP, PR, MG, RS e SC, por causa de chuvas e alagamentos. [[316]]']),
  note='O pedido de Lula foi feito primeiro ao presidente do TSE, Kassio Nunes Marques, que pediu esclarecimentos às prefeituras. A coligação então acionou o STF, e o ministro Cristiano Zanin prorrogou o fim da votação em duas horas, até as 19h, em todas as seções do país. [[315]]')
comparativo = dict(id='comparacao', t='Do 1º para o 2º turno',
  l=dict(tags=['fato'], items=[
   'Votos válidos: <b>45,16% → 51,79%</b> (+6,63 pontos). [[97,310]]',
   'Votos: 53,9 milhões → 64,3 milhões (+10,4 milhões). [[97,310]]',
   'Estados: 12 → <b>13</b>. Manteve os 9 do Nordeste, Pará, Amazonas e Amapá e virou <b>Minas Gerais</b>. [[205,313,312]]']),
  f=dict(tags=['fato'], items=[
   'Votos válidos: <b>47,03% → 48,21%</b> (+1,18 ponto). [[97,310]]',
   'Votos: 56,1 milhões → 59,8 milhões (+3,7 milhões). [[97,310]]',
   'Estados: 14 e o DF → <b>13 e o DF</b>. Manteve Sul, Centro-Oeste, SP, RJ, ES, Acre, Rondônia, Roraima e Tocantins; perdeu Minas Gerais. [[205,313,312]]']),
  note='No 1º turno Flávio ficou cerca de 2,2 milhões de votos à frente; no 2º, Lula venceu por cerca de 4,4 milhões. A abstenção caiu de 21,08% para cerca de 19,2%. Votos do 1º turno arredondados a partir dos totais do TSE. [[97,310]]')
body += (open_sec('resultado-sec', '2º turno · 25/10/2026', 'Resultado')
         + row(resultado) + row(comparativo)
         + '<article class="row" id="mapas"><h3>Mapa: 1º turno × 2º turno</h3><div class="mapas2">'
         + f'<figure><figcaption>1º turno (4/10)</figcaption>{ufmap()}</figure><figure><figcaption>2º turno (25/10)</figcaption>{ufmap2()}</figure></div>'
         + '<div class="maplegend maplegend-row"><span class="lg-l">Lula venceu</span><span class="lg-f">Flávio venceu</span><span class="small">% dos válidos do vencedor; no 2º turno, só onde as fontes informam (MG, PI, RR e SP)</span></div>'
         + f'<p class="note">A única troca entre os turnos foi Minas Gerais, que passou de Flávio para Lula. {R("[[205,313,312,314]]")}</p></article>'
         + row(prorrog) + '</section>')

body += (open_sec('disputa', 'Até 25/10', 'A disputa até a votação')
         + f'<article class="row"><h3>Mapa do 1º turno</h3><div class="mapwrap">{ufmap()}<div class="maplegend"><span class="lg-l">Lula venceu</span><span class="lg-f">Flávio venceu</span><span class="small">% dos válidos do vencedor no estado</span></div></div>'
         + f'<p class="note">Flávio ficou cerca de 2,2 milhões de votos à frente, com 99,99% das urnas apuradas. Brancos: 1,84% e nulos: 2,93% do total. {R("[[97,140,134]]")}</p></article>'
         + ''.join(row(r) for r in turno2) + debates + '</section>')

# 2. Como ler
legend_items = [
 ('tse','Está no plano entregue ao TSE.'),('fala','Dito em entrevista ou evento; não está no plano.'),
 ('cond','Precisa de PEC, lei ou maioria no Congresso.'),('cont','Mantém ou amplia política que já existe.'),
 ('lei','Lei ou emenda aprovada.'),('interp','Avaliação de analistas ou entidades, não fato oficial.'),
 ('inv','Investigação em curso, sem condenação.'),('anul','Anulação, rejeição ou prescrição: não é absolvição de mérito.')]
body += ('<section class="sec howto" id="leitura"><header class="sechead"><span class="eyebrow">Como ler</span><h2>Etiquetas e cuidados</h2></header>'
         '<div class="legend">' + ''.join(f'<div class="lg">{chips([k])}<span>{d}</span></div>' for k, d in legend_items) + '</div>'
         '<ul class="cuidados">'
         '<li><b>Fontes:</b> os números pequenos ao lado do texto abrem a fonte de cada informação. As opiniões são atribuídas a quem as disse; a página não indica qual lado tem razão.</li>'
         f'<li><b>Data:</b> base de dados de 8/10/2026, com disputa, pesquisas, apoios, debates, votação da 6x1 e escândalos atualizados até 26/10/2026, depois do resultado. Esses itens mudam rápido; confira a fonte antes de compartilhar.</li>'
         f'<li><b>Planos:</b> estar registrado no TSE prova que o plano foi apresentado. O TSE não avalia custo, viabilidade nem aprovação das medidas. {R("[[66]]")}</li>'
         f'<li><b>Leis:</b> sanção ou promulgação não é o mesmo que execução, e várias medidas nasceram no Congresso, não no Executivo, como o Auxílio Emergencial e o Marco das Startups. {R("[[12,8]]")}</li>'
         '</ul></section>')

# 3. Propostas por tema (catálogo)
temas = ''.join(f'<a href="#{r["id"]}">{r["t"]}</a>' for r in propostas)
body += (open_sec('propostas', 'Plano 2027–2030', 'Propostas por tema',
         'Tudo o que está nos planos, tema por tema. Os itens marcados com "ver análise" são detalhados na seção seguinte. Segundo as reportagens consultadas, nenhum dos planos trata de aborto ou de política de drogas. [[223,224]]')
         + f'<nav class="temas" aria-label="Temas das propostas">{temas}</nav>'
         + row(P['plano']) + ''.join(row(r) for r in propostas) + '</section>')

# 4. Propostas de maior impacto (efeitos + base legal + Congresso)
imp_rows = ''
for g in IMP:
    L = ''.join(imp_card(c) for c in g['l']); F = ''.join(imp_card(c) for c in g['f'])
    imp_rows += (f'<article class="row" id="{g["id"]}"><h3>{g["t"]}</h3><div class="pair">'
                 f'<div class="cell cell-l"><span class="who who-l">Lula</span>{L}</div>'
                 f'<div class="cell cell-f"><span class="who who-f">Flávio Bolsonaro</span>{F}</div></div></article>')
body += (open_sec('impacto', 'Na prática', 'Propostas de maior impacto',
         'Para cada uma: quem ganha e quem paga, o que precisa ser aprovado, se esbarra na Constituição ou em decisão do STF, e os principais argumentos dos dois lados. '
         'Uma <b>PEC</b> exige 308 dos 513 deputados e 49 dos 81 senadores, em dois turnos; uma <b>lei complementar</b>, 257 deputados e 41 senadores; uma <b>lei ordinária</b>, maioria simples dos presentes. [[204]]')
         + congresso_block() + benef_resumo() + imp_rows + '</section>')

# 5. Quem são
body += (open_sec('quem', 'Perfil', 'Quem são os candidatos')
         + ''.join(row(P[k]) for k in ['candidatura','alianca','vices'])
         + ''.join(row(r) for r in trajetoria)
         + ''.join(row(P[k]) for k in ['bens','arrecadacao'])
         + '</section>')

# 6. Histórico
body += (open_sec('historico', 'Histórico', 'O que os governos de referência entregaram',
         'Compara o governo Lula III (2023–2026) com o de Jair Bolsonaro (2019–2022). <b>Flávio não chefiou esse governo</b>: era senador. Ele aparece aqui porque o plano dele declara continuidade de políticas daquele período (Pix, Gov.br, Liberdade Econômica, Marco do Saneamento). [[80,87]]')
         + ''.join(row(r) for r in governos)
         + '<h3 class="subhead" id="indicadores">Indicadores nacionais</h3>'
         + '<p class="lede sublede">Médias dos anos fechados: 2019–2022 (inclui a pandemia) e 2023–2025 (pós-reabertura). <b>Não medem efeito causal de um presidente</b>: dependem também de juros, commodities, clima, Congresso, estados e municípios.</p>'
         + f'<div class="medias">{medias_html()}</div>'
         + f'<details class="more"><summary>Ver a série completa, ano a ano</summary>{ind_table()}'
         + f'<p class="small"><b>Renda:</b> a renda domiciliar per capita real chegou a R$ 2.264 em 2025, 18,9% acima de 2019. {R("[[51,52]]")} <b>Resultado primário:</b> fluxo do ano (receita menos despesa, sem juros); a dívida bruta é o estoque acumulado. {R("[[64,65]]")}</p>'
         + '<p class="small">* 2026 é parcial. PRODES segue o ano florestal (agosto a julho). MVI soma homicídio doloso, latrocínio, lesão seguida de morte e mortes por intervenção policial. Pobreza não tem estimativa para 2025–2026. D1 = 1ª dose da tríplice viral; meta usual de 95%. ' + R('[[54,61,51,58]]') + '</p></details>'
         + '</section>')

# 7b. Escândalos (depois do Histórico)
body += sec_escandalos()

# 8. Resumo
RES = {
 'l': dict(nome='Lula', intro='Ele continua sendo presidente por mais quatro anos, a partir de 5 de janeiro de 2027, e quer manter quase tudo o que já faz.',
  muda=['As famílias mais pobres continuariam recebendo ajuda em dinheiro, como o Bolsa Família. [[71]]',
        'O salário mínimo continuaria subindo um pouco mais que os preços. [[233]]',
        'Quem ganha até R$ 5 mil por mês continua sem pagar imposto de renda. [[154]]'],
  bom=['Quem ganha pouco e quem é aposentado teria um pouco mais de dinheiro no bolso. [[233,154]]'],
  ruim=['O governo gastaria mais com aposentadorias, que sobem junto com o salário mínimo. [[233]]',
        'O governo gasta mais do que ganha, e o país está devendo cada vez mais dinheiro. [[232]]']),
 'f': dict(nome='Flávio', intro='Ele perdeu a eleição, mas é bom saber o que ele queria mudar no jeito de governar. Ele continua senador até o começo de 2027.',
  muda=['O governo ficaria menor, com pelo menos 10 ministérios a menos. [[81]]',
        'O governo cobraria menos impostos. [[81]]',
        'Ficaria mais barato para as empresas contratarem jovens e pessoas mais velhas. [[83]]',
        'O trabalhador poderia combinar o horário direto com o patrão. [[86]]',
        'Os castigos para crimes ficariam mais duros: adolescentes de 16 anos que cometerem crimes graves poderiam ser julgados como adultos, e criminosos ficariam mais tempo presos. [[81,88]]'],
  bom=['Haveria mais empregos e menos crime. [[83,81]]'],
  ruim=['O trabalhador poderia perder alguns direitos. [[231]]',
        'Algumas comidas e remédios poderiam ficar mais caros. [[235]]',
        'Várias ideias podem ser barradas pelo Supremo Tribunal Federal, que confere se as leis respeitam a Constituição. [[239,242]]'])}
def rcard(k):
    d=RES[k]; ul=lambda xs: '<ul>'+''.join(f'<li>{R(x)}</li>' for x in xs)+'</ul>'
    tit = 'Lula foi reeleito: o que pode acontecer' if k=='l' else 'O que Flávio propunha'
    return (f'<div class="rcard rcard-{k}"><h3>{tit}</h3><p class="rintro">{d["intro"]}</p>'
            f'<h4>O que pode mudar</h4>{ul(d["muda"])}'
            f'<h4 class="r-bom">Quem gosta da ideia acha que</h4>{ul(d["bom"])}'
            f'<h4 class="r-ruim">Quem se preocupa acha que</h4>{ul(d["ruim"])}</div>')
body += ('<section class="sec resumo" id="resumo"><header class="sechead"><span class="eyebrow">Resumo</span><h2>O que pode acontecer</h2>'
         '<p class="lede">Explicado de um jeito simples, para qualquer pessoa entender. Lula venceu: o cartão dele mostra o que pode acontecer agora; o de Flávio, o que ele propunha.</p></header>'
         f'<div class="pair">{rcard("l")}{rcard("f")}</div>'
         '<p class="rnote"><b>Uma mudança já está garantida para todo mundo, ganhe quem ganhar:</b> o fim da escala 6x1 virou lei em 16/10. Até meados de dezembro, quem trabalha com carteira passa a ter duas folgas por semana, sem ganhar menos. ' + R('[[296]]') + '<br><br>O presidente não decide tudo sozinho. Muitas dessas ideias só acontecem se os deputados e senadores votarem a favor. '
         'E ninguém sabe com certeza o que vai acontecer: são planos e previsões, não promessas garantidas.</p></section>')

CFG = json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'config.json')))
contato_html = (f'<p><b>Encontrou um erro?</b> Escreva para <span class="mail">{html.escape(CFG["contato"])}</span> com o trecho e, se possível, uma fonte. Correções entram em "O que mudou".</p>'
                if CFG.get('contato') else '<p><b>Encontrou um erro?</b> Avise quem compartilhou o site com você ou o autor; correções entram em "O que mudou".</p>')
MUDOU = [
 ('26/10/2026', 'Resultado do 2º turno: Lula reeleito com 51,79% dos votos válidos (TSE). Mapa do 2º turno, prorrogação do horário de votação, reação dos dois candidatos e posse em 5/1/2027. Resumo do debate da Globo (23/10) e das pesquisas de véspera. Topo, Resumo e textos de compartilhamento adaptados ao pós-eleição.'),
 ('22/10/2026', 'Resumo do debate da Band (18/10) e confirmação do debate da Globo (23/10, 21h20). Novas pesquisas Datafolha (50% a 50% dos válidos) e Quaest (45% a 44% do total). Anúncio de Flávio sobre o futuro ministro da Saúde incluído em Saúde.'),
 ('17/10/2026', 'Fim da escala 6x1 aprovado no Senado (75 a 1, em 14/10) e promulgado em 16/10 como Emenda Constitucional 141; voto de Flávio a favor. Resumo ajustado: a 6x1 vale ganhe quem ganhar. Novas pesquisas Datafolha, Quaest e PoderData. Debate da Band confirmado pelos dois. Pedido da PF de mais 90 dias no caso Dark Horse.'),
 ('12/10/2026', 'Destaque de "Quem ganha" e "Quem paga" no topo de cada proposta de maior impacto, com um resumo por candidato; Pé-de-Meia, voucher e corte de ministérios ganharam essa análise. Pesquisa AtlasIntel passa a aparecer em votos válidos (47,2% a 52,8%), com o registro no TSE (BR-03663/2026). Links de duas fontes corrigidos. Medidas temporárias do governo Lula III (PEC da Transição e Auxílio Reconstrução) incluídas no Histórico. Nova seção "Sobre e método".'),
 ('11/10/2026', 'Apoio de Augusto Cury a Flávio (8/10); voto crítico de PCB e PSTU e apoio da UP a Lula; cancelamento do debate da Record; pesquisa AtlasIntel; votação da PEC da 6x1 no Senado marcada para 14/10.'),
 ('11/10/2026', 'Auditoria das fontes: 345 afirmações conferidas. Correções nos casos das rachadinhas, Calixto, Adriano da Nóbrega e Dark Horse, e no exemplo de lei que "nasceu no Congresso".'),
 ('9 e 10/10/2026', 'Primeira versão, baseada no relatório comparativo com data de corte em 8/10/2026, e pesquisa complementar: Congresso eleito, apoios, pesquisas, base legal das propostas e escândalos.'),
]
mudou_html = ''.join(f'<li><b>{d}</b> {html.escape(t)}</li>' for d,t in MUDOU)
body += ('<section class="sec" id="sobre"><header class="sechead"><span class="eyebrow">Transparência</span><h2>Sobre e método</h2></header>'
         '<div class="sobre">'
         '<div><h3>O que é</h3><p>Um comparativo dos dois candidatos do 2º turno de 2026, feito de forma independente. Depois da votação, fica como registro da campanha, com o resultado. O site não pede voto, não é material de campanha e trata os dois lados com a mesma estrutura: mesmos temas, mesma ordem, mesmas etiquetas.</p></div>'
         '<div><h3>Como foi feito</h3><p>A base é um relatório comparativo com data de corte em 8/10/2026, conferido e ampliado com fontes oficiais (TSE, Planalto, Câmara, Senado, STF, IBGE) e reportagens. Toda afirmação de fato leva o número da fonte. Opiniões aparecem atribuídas a quem as disse. Anulação ou prescrição de processo é descrita como decisão processual, não como absolvição. Pesquisas aparecem com instituto, período, margem e registro no TSE.</p></div>'
         f'<div><h3>Correções</h3>{contato_html}</div>'
         '</div>'
         f'<h3 class="mudou-t">O que mudou</h3><ul class="mudou">{mudou_html}</ul></section>')

refs_html = ''.join(f'<li value="{n}"><a href="{html.escape(refs[n]["u"])}" target="_blank" rel="noopener">{html.escape(refs[n]["t"])}</a></li>' for n in sorted(used))
body += (f'<section class="sec" id="fontes"><header class="sechead"><span class="eyebrow">Fontes</span><h2>Referências citadas</h2><p class="lede">Números 1 a 154 seguem a pesquisa original; a partir de 201 são fontes adicionadas para atualizar e confirmar informações (reportagens até 26/10/2026).</p></header>'
         f'<details class="more"><summary>Ver as {len(used)} referências</summary><ol class="reflist">{refs_html}</ol></details></section>')

HERE=_os.path.dirname(_os.path.abspath(__file__))
tpl = open(_os.path.join(HERE,'template.html')).read()
_os.makedirs(_os.path.join(HERE,'saida','site-claude'),exist_ok=True)
open(_os.path.join(HERE,'saida','site-claude','index.html'), 'w').write(tpl.replace('<!--BODY-->', body))
print('refs used', len(used))
