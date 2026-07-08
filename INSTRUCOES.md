# 🧩 Desafio Técnico — Estágio em Análise de Dados | Sefaz Maceió

Bem-vindo(a)! Este repositório contém um **desafio prático** para a vaga de estágio em
Análise de Dados da **Secretaria Municipal da Fazenda de Maceió (Sefaz Maceió)**.

A ideia aqui **não é acertar uma resposta única**. Queremos entender o seu **raciocínio**,
a sua **organização** e a sua **forma de trabalhar com dados** — desde abrir um arquivo
"bagunçado" até transformar números em conclusões que fazem sentido.

> 💡 Não se preocupe se você nunca mexeu com dados de finanças públicas. Este README explica
> tudo o que você precisa saber sobre os dados. O resto é com você.

---

## 🎯 O objetivo do desafio

Você vai trabalhar com os dados de **despesas das 26 capitais brasileiras**, publicados pelo
**Siconfi** (o sistema de contas públicas do Tesouro Nacional), no período de **2020 a 2025**.

Seu objetivo final é **comparar como as capitais gastam o dinheiro público por área (função)**,
olhando principalmente para a diferença entre o que foi **empenhado** (reservado/comprometido)
e o que foi efetivamente **pago**.

Em resumo, você vai:

1. **Descompactar** os arquivos da pasta `dados_compactos/` por meio de código.
2. **Ler e consolidar** tudo em um **único DataFrame** (uma única tabela).
3. **Gerar um formato otimizado** de dados (ex.: Parquet) **ou** usar um banco/biblioteca que
   permita consultar as informações de forma performática (ex.: DuckDB).
4. **Analisar indicadores e fatos relevantes**, comparando as capitais por **função** e,
   se quiser se aprofundar, por **subfunção**.

---

## 📦 Sobre os dados

### Fonte
Os dados vêm do **FINBRA / Siconfi** — mais especificamente do relatório
**"Despesas por Função (Anexo I-E)"**, no escopo **Capitais**. É um dado **público e oficial**
do Tesouro Nacional ([siconfi.tesouro.gov.br](https://siconfi.tesouro.gov.br/)).

> **FINBRA** = *Finanças do Brasil*. É a base que reúne as informações contábeis e fiscais
> declaradas pelos entes públicos (estados e municípios).

### Estrutura das pastas

Os arquivos estão organizados por ano dentro de `dados_compactos/`:

```
dados_compactos/
├── 2020/
│   └── finbra_CAP_DespesasporFuncao(AnexoI-E) (1).zip
├── 2021/
│   └── finbra_CAP_DespesasporFuncao(AnexoI-E).zip
├── 2022/
│   └── finbra_CAP_DespesasporFuncao(AnexoI-E).zip
├── 2023/
│   └── finbra_CAP_DespesasporFuncao(AnexoI-E).zip
├── 2024/
│   └── finbra_CAP_DespesasporFuncao(AnexoI-E).zip
└── 2025/
    └── finbra_CAP_DespesasporFuncao(AnexoI-E).zip
```

Cada `.zip` contém **um arquivo `finbra.csv`** com os dados daquele ano.

### ⚠️ Formato do CSV (leia com atenção — aqui é onde a maioria tropeça!)

O arquivo **não é um CSV "comum"** no padrão internacional. Ele segue o padrão brasileiro do
Siconfi, e tem algumas particularidades que você precisa tratar no código:

| Característica | Valor | Por que importa |
|---|---|---|
| **Encoding** | `ISO-8859-1` (Latin-1) | Se você abrir como UTF-8, acentos viram `�` (ex.: "Saúde" → "Sa�de"). |
| **Separador de colunas** | ponto e vírgula `;` | O separador **não** é a vírgula. |
| **Separador decimal** | vírgula `,` | `874885274,98` é **R$ 874 milhões**, não 874 bilhões. |
| **Linhas de cabeçalho extras** | 3 linhas antes da tabela | As 3 primeiras linhas são **metadados**, não dados. |

As **3 primeiras linhas** de cada arquivo são assim (precisam ser ignoradas na leitura):

```
Exercício: 2020
Escopo: Capitais
Tabela: Despesas por Função (Anexo I-E)
Instituição;Cod.IBGE;UF;População;Coluna;Conta;Identificador da Conta;Valor   ← cabeçalho real
```

### Dicionário de colunas

A partir da 4ª linha, temos a tabela de verdade, com estas colunas:

| Coluna | Descrição | Exemplo |
|---|---|---|
| `Instituição` | Nome da prefeitura (capital) | `Prefeitura Municipal de Maceió - AL` |
| `Cod.IBGE` | Código IBGE do município | `2704302` |
| `UF` | Unidade da Federação | `AL` |
| `População` | População estimada do município | `1025360` |
| `Coluna` | **Estágio da despesa** (ver abaixo) | `Despesas Empenhadas` |
| `Conta` | **Função ou subfunção** orçamentária (ver abaixo) | `10 - Saúde` |
| `Identificador da Conta` | Código técnico interno do Siconfi | `siconfi-cor_TotalDespesas` |
| `Valor` | Valor em reais (R$) | `874885274,98` |

---

## 💰 Conceitos que você precisa entender

### Os estágios da despesa pública (coluna `Coluna`)

No setor público, uma despesa não é simplesmente "paga". Ela passa por **etapas**. No arquivo,
a coluna `Coluna` indica em qual etapa o valor está:

| Valor em `Coluna` | O que significa (em linguagem simples) |
|---|---|
| **Despesas Empenhadas** | O governo **reservou/comprometeu** o dinheiro para uma finalidade. É a "promessa de gasto". |
| **Despesas Liquidadas** | O serviço/produto foi **entregue e conferido** — a dívida foi reconhecida. |
| **Despesas Pagas** | O dinheiro **saiu do caixa** de fato. |
| **Inscrição de Restos a Pagar Não Processados** | Foi empenhado, mas **ainda não foi liquidado** no ano — fica para o ano seguinte. |
| **Inscrição de Restos a Pagar Processados** | Foi liquidado, mas **ainda não foi pago** no ano — fica para o ano seguinte. |

O fluxo normal é: **Empenho → Liquidação → Pagamento**.

👉 **O coração deste desafio** é comparar **Empenhado × Pago**. A diferença entre os dois conta
uma história: quanto a prefeitura prometeu gastar versus quanto realmente saiu do caixa.

### O que é "Função" e "Subfunção"? (coluna `Conta`)

Toda despesa pública é classificada por **função** e **subfunção** — é a forma de dizer
**"em que área"** o dinheiro foi gasto. Isso é padronizado para todo o Brasil pela
**Portaria MOG nº 42/1999**.

- **Função** = a **grande área** de atuação do governo. São códigos de **2 dígitos**.
  - Exemplos: `10 - Saúde`, `12 - Educação`, `04 - Administração`, `15 - Urbanismo`.
- **Subfunção** = um **detalhamento** dentro (ou através) de uma função. Vêm no formato `XX.YYY`.
  - Exemplos dentro de **Saúde**: `10.301 - Atenção Básica`, `10.302 - Assistência Hospitalar e Ambulatorial`.
  - Exemplos dentro de **Educação**: `12.361 - Ensino Fundamental`, `12.365 - Educação Infantil`.

> 🧠 **Sacada importante:** a subfunção é "matricial". Uma mesma subfunção pode aparecer em
> várias funções. Repare que `122 - Administração Geral` aparece como `04.122`, `10.122`,
> `12.122`... ou seja, quase toda função tem um pedaço gasto com administração. Isso é normal.

#### As 27 funções que você vai encontrar nos dados

| Código | Função | Código | Função |
|---|---|---|---|
| 01 | Legislativa | 15 | Urbanismo |
| 02 | Judiciária | 16 | Habitação |
| 03 | Essencial à Justiça | 17 | Saneamento |
| 04 | Administração | 18 | Gestão Ambiental |
| 05 | Defesa Nacional | 19 | Ciência e Tecnologia |
| 06 | Segurança Pública | 20 | Agricultura |
| 07 | Relações Exteriores | 22 | Indústria |
| 08 | Assistência Social | 23 | Comércio e Serviços |
| 09 | Previdência Social | 24 | Comunicações |
| 10 | **Saúde** | 25 | Energia |
| 11 | Trabalho | 26 | Transporte |
| 12 | **Educação** | 27 | Desporto e Lazer |
| 13 | Cultura | 28 | Encargos Especiais |
| 14 | Direitos da Cidadania | | |

*(A função `21` não é usada por municípios.)*

#### Contas "especiais" que aparecem na coluna `Conta`

Além das funções e subfunções, você vai ver algumas linhas agregadas. **Cuidado para não
somá-las junto com as funções** (senão você conta o mesmo valor duas vezes):

- **`Despesas Exceto Intraorçamentárias`** e **`Despesas Intraorçamentárias`** — são totais.
  "Intraorçamentárias" são gastos de um órgão público pagando outro do mesmo município.
- **`FUxx - Demais Subfunções`** (ex.: `FU10 - Demais Subfunções`) — é a soma das subfunções
  "menores" de uma função, agrupadas como resto.

### ⚠️ Atenção: completude dos dados por ano

Nem todo ano está 100% preenchido! Os municípios têm prazos para declarar, e os dados mais
recentes ainda estão sendo consolidados. **No momento, o ano de 2025 está incompleto** — apenas
parte das capitais entregou seus dados.

👉 **Antes de comparar anos**, conte quantas capitais existem em cada ano. Comparar um 2024 com
26 capitais contra um 2025 com 11 capitais levaria a conclusões erradas. Saber identificar isso
**conta pontos** na avaliação. 😉

---

## 🪜 Passo a passo sugerido

A seguir, um roteiro. Você pode adaptar a estrutura como preferir — o importante é que cada
etapa fique **registrada em commits** no seu repositório.

### Passo 1 — Descompactar os arquivos por código

Não vale descompactar na mão! Escreva um script que **percorra** a pasta `dados_compactos/`,
encontre todos os `.zip` e os extraia.

> 💡 Em Python, dê uma olhada em `pathlib` / `glob` (para achar os arquivos) e no módulo
> `zipfile` (para extrair). Pense em **onde** colocar os arquivos extraídos (ex.: uma pasta
> `dados_extraidos/`) e em como **diferenciar o ano** de cada arquivo (a pasta de origem já diz!).

### Passo 2 — Ler e consolidar em um único DataFrame

Leia cada `finbra.csv` e **junte todos em uma única tabela**. Lembre-se das pegadinhas do
formato! Em `pandas`, um ponto de partida seria:

```python
import pandas as pd

df = pd.read_csv(
    caminho_do_csv,
    sep=";",            # separador é ponto e vírgula
    skiprows=3,         # pula as 3 linhas de metadados
    encoding="latin-1", # ISO-8859-1, para os acentos não quebrarem
    decimal=",",        # vírgula é o separador decimal
    thousands=".",      # (se necessário) ponto como separador de milhar
)
```

Sugestões para enriquecer a tabela final:
- Crie uma coluna **`ano`** (você sabe o ano pela pasta de origem do arquivo).
- Crie uma coluna que diferencie **`função` vs `subfunção`** a partir do texto da coluna `Conta`
  (dica: funções começam com 2 dígitos e um espaço, `10 - ...`; subfunções têm um ponto,
  `10.301 - ...`).
- Garanta que `Valor` ficou como **número** (e não como texto), para conseguir somar e comparar.

### Passo 3 — Gerar um formato otimizado / base performática

Ler 6 CSVs toda vez é lento e pesado. Salve sua tabela consolidada em um formato eficiente,
ou use uma ferramenta de consulta rápida. Duas estratégias comuns:

- **Parquet**: `df.to_parquet("finbra_consolidado.parquet")` — arquivo colunar, comprimido e
  rápido de ler.
- **DuckDB**: um banco analítico "de bolso" que roda no seu próprio computador e consulta
  Parquet/CSV com **SQL** muito rápido, sem precisar instalar servidor.

Explique no seu repositório **por que** você escolheu a abordagem que usou.

### Passo 4 — Analisar indicadores e fatos relevantes

Aqui é onde você brilha! 🌟 O foco pedido é:

> **Comparar as despesas por função entre as capitais, olhando o que foi *empenhado* versus o
> que foi *pago*.** Se quiser, detalhe também por subfunção.

Algumas direções (você não precisa fazer todas — escolha as que achar mais interessantes):

- Ranqueie as capitais por gasto em uma função (ex.: Saúde, Educação) e veja quem **paga**
  uma proporção maior do que **empenha**.
- Compare **per capita** (valor ÷ `População`) — comparar São Paulo com Vitória em valor
  absoluto é injusto; por habitante a conversa muda.
- Veja a **evolução ao longo dos anos** (2020 a 2024) de uma função para Maceió e compare com
  a média das capitais.
- Dentro de uma função, descubra **quais subfunções concentram o gasto** (ex.: em Saúde,
  quanto vai para `10.301 - Atenção Básica`?).

---

## 🛠️ Ferramentas e linguagens sugeridas

Você tem **liberdade** para escolher suas ferramentas. Abaixo, algumas sugestões boas para
este tipo de desafio:

### Linguagem
- **Python** *(recomendado)* — é o padrão de mercado em análise de dados e tem todas as
  bibliotecas que você vai precisar.
- **R** — ótima alternativa, especialmente se você já tem familiaridade (`tidyverse`, `data.table`).

### Bibliotecas (Python)

| Para... | Bibliotecas |
|---|---|
| Manipular dados | `pandas` (clássico), `polars` (moderno e rápido) |
| Consultar com SQL / performance | `duckdb` |
| Salvar formato otimizado | `pyarrow` (Parquet) |
| Visualizar (gráficos) | `matplotlib`, `seaborn`, `plotly` |
| Lidar com arquivos/zip | `pathlib`, `glob`, `zipfile` (já vêm no Python) |
| Organizar a análise | `Jupyter Notebook` |

> 💡 Boa prática: use um **ambiente virtual** (`venv`) e deixe um arquivo `requirements.txt`
> com as bibliotecas que você usou, para qualquer pessoa conseguir rodar o seu projeto.

### APPs de DataViz (Caso queira)

- **Power BI**
- **Tableau**
- **Google Data Studio**

---

## 📊 Exemplo de indicador para te inspirar

Um indicador simples e poderoso para este desafio é a **Taxa de Execução Financeira**:

$$\text{Taxa de Execução} = \frac{\text{Despesas Pagas}}{\text{Despesas Empenhadas}} \times 100$$

Ela responde: **de tudo o que a prefeitura comprometeu gastar em uma área, quanto realmente
saiu do caixa dentro do ano?** Uma taxa baixa sugere que sobrou muita coisa em *restos a pagar*
(contas que ficaram para o ano seguinte).

#### Exemplo ilustrativo (valores fictícios, só para entender a leitura)

| Capital | Função | Empenhado (R$) | Pago (R$) | Taxa de Execução |
|---|---|---:|---:|---:|
| Capital A | 10 - Saúde | 500.000.000 | 480.000.000 | **96%** |
| Capital B | 10 - Saúde | 500.000.000 | 350.000.000 | **70%** |
| Capital A | 12 - Educação | 400.000.000 | 360.000.000 | **90%** |

**Leitura:** na Saúde, a *Capital A* pagou 96% do que empenhou (execução alta), enquanto a
*Capital B* pagou só 70% — ou seja, comprometeu o orçamento, mas deixou **30% para restos a
pagar**. Esse tipo de diferença é exatamente o que rende uma boa análise: *por que* isso
acontece? É um padrão que se repete nos anos? Acontece em todas as funções ou só em algumas?

#### Outras perguntas que dariam boas análises
- Qual capital tem a **melhor (e a pior)** taxa de execução média? Isso muda por função?
- Em quais funções as capitais mais "empurram" gasto para *restos a pagar*?
- O gasto **per capita** com Saúde e Educação está crescendo ou caindo de 2020 a 2024?
- Onde Maceió se posiciona em relação às demais capitais? Em que áreas ela se destaca?

> Não existe "a resposta certa". Capriche em **mostrar o raciocínio**, **justificar as escolhas**
> e **traduzir os números em conclusões claras**.

---

## ✅ O que vamos avaliar

| Critério | O que observamos |
|---|---|
| **Tratamento dos dados** | Você lidou corretamente com encoding, decimal, metadados e dados incompletos? |
| **Qualidade do código** | Está organizado, legível e reproduzível (dá para rodar do zero)? |
| **Análise e insights** | As conclusões fazem sentido e estão bem comunicadas? |
| **Organização do repositório** | Estrutura clara, com `README`/comentários explicando as escolhas. |
| **Processo público** | O caminho está visível nos **commits** (não só o resultado final). |

> Não buscamos perfeição — buscamos **clareza de raciocínio** e **honestidade técnica**.
> Documentar uma dificuldade ou limitação também conta a seu favor.

---

## 📤 Como entregar

1. Faça um **fork** deste repositório para a sua conta do GitHub.
2. Desenvolva sua solução no fork, com **commits frequentes** (queremos ver o processo, não só
   o resultado).
3. Deixe tudo **público**: código, resultados e comentários.
4. **Compartilhe o link do seu repositório** com a gente **até 07/07/2026**.

### 💬 Dúvidas?
Entre no nosso grupo do WhatsApp para tirar dúvidas, trocar dicas e fazer networking:
**(https://chat.whatsapp.com/I3dfAfriDRFCCYtGb6LINo?s=cl&p=a&ilr=4)**

---

Boa sorte e bom desafio! 🚀
**José Gonçalves Jr - Head de Dados - Sefaz Maceió**
