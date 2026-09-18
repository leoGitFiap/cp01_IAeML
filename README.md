# CheckPoint 1 - IA & ML - FIAP 2026

## Resume Profiler 

Projeto Python para triagem de currículos de profissionais de tecnologia em PDF.

O programa extrai o texto do currículo, aplica filtros de experiência e pretensão salarial e, para candidatos aprovados, gera um parecer e um resumo executivo por meio de uma simulação local baseada em regras.

Não utiliza API nem executa um modelo de linguagem real. O GPT-4o mini é utilizado como referência para o tokenizador e para as tarifas da estimativa de custo.

## Integrantes:
* Leonardo Fernandes Mesquita, RM:559623
* Vitor de Lima Domingues, RM:561008
* Giovanni Romano Provazi, RM:560434
* Caio Berardo de Araújo, RM:560357

## Funcionalidades

- Extração de texto de PDFs com `pypdf`.
- Validação de experiência mínima, com suporte a valores em anos ou meses.
- Comparação da pretensão salarial com o orçamento da vaga.
- Interrupção da triagem quando o candidato não atende aos filtros.
- Geração simulada de parecer de senioridade e indícios de soft skills.
- Criação de resumo executivo com dados do candidato.
- Identificação de tecnologias mencionadas em um vocabulário predefinido.
- Contagem de tokens do prompt e da resposta com `tiktoken`.
- Exibição dos resultados e da estimativa de custo no terminal.

## Estrutura

```text
projeto/
├── data/
│   └── curriculo_candidato.pdf
├── src/
│   ├── __init__.py
│   ├── deterministic_layer.py
│   ├── generative_layer.py
│   ├── pdf_generator.py
│   ├── pdf_reader.py
│   └── token_tracker.py
├── main.py
└── README.md
```

### Responsabilidade dos arquivos

- `main.py`: coordena a triagem e exibe os resultados.
- `pdf_reader.py`: extrai o texto do PDF.
- `deterministic_layer.py`: aplica os filtros de experiência e salário.
- `generative_layer.py`: monta a resposta simulada e calcula a estimativa de custo.
- `token_tracker.py`: conta os tokens dos textos.
- `pdf_generator.py`: gera o currículo de exemplo em PDF.

## Instalação

Com Python e pip instalados, execute:

```bash
python -m pip install --upgrade pypdf tiktoken reportlab
```

O `reportlab` é utilizado pelo gerador do currículo de exemplo.

## Formato do currículo

O programa espera um PDF com texto extraível e campos identificados por rótulos, como:

```text
Nome: Carlos Eduardo Fontes
Experiência: 28 anos
Pretensão salarial: R$ 32.457
```

Mantenha cada campo em uma linha, com o valor após os dois-pontos.

### Experiência

Exemplos aceitos:

```text
Experiência: 10 anos
Experiência: 120 meses
Experiência: 9,5 anos
Experiência: 28
```

Quando a unidade não é informada, o valor é considerado em anos.

Períodos mistos, como `2 anos e 6 meses`, não são aceitos. Utilize `2,5 anos` ou `30 meses`.

### Pretensão salarial

Informe um único valor no formato brasileiro. Exemplos:

```text
Pretensão salarial: R$ 32.457
Pretensão salarial: R$ 32457
Pretensão salarial: R$ 32.457,50
```

O filtro compara esse valor com o orçamento máximo configurado.

## Configuração e execução

No `main.py`, configure:

```python
budget = 35000
required_experience = 10
```

Esses valores representam o orçamento máximo da vaga e a experiência mínima em anos.

Coloque o currículo em:

```text
data/curriculo_candidato.pdf
```

Execute a partir da pasta raiz do projeto:

```bash
python main.py
```

Para gerar novamente o currículo de exemplo:

```bash
python -m src.pdf_generator
```

Esse comando sobrescreve `data/curriculo_candidato.pdf`.

## Fluxo da triagem

1. O programa lê o PDF e extrai seu texto.
2. Aplica os filtros de experiência e pretensão salarial.
3. Se houver reprovação, exibe os motivos e encerra a execução.
4. Se houver aprovação, gera o parecer e o resumo executivo simulados.
5. Conta os tokens de entrada e saída.
6. Exibe a análise, o total de tokens e a estimativa de custo.

## Simulação da análise

A resposta é construída por regras e modelos de texto preenchidos com informações do currículo.

A senioridade é estimada pelo tempo declarado:

- Menos de 3 anos: Júnior.
- De 3 a menos de 6 anos: Pleno.
- A partir de 6 anos: Sênior.

Essa classificação é didática e não comprova senioridade profissional.

As regras procuram termos relacionados a colaboração, liderança e comunicação. Os trechos encontrados são apresentados como possíveis indícios a confirmar em entrevista.

O vocabulário de tecnologias reconhecidas contém:

- Python
- JavaScript
- TypeScript
- Java
- SQL
- React
- Docker
- AWS

## Tokens e estimativa de custo

O programa utiliza o tokenizador associado a `gpt-4o-mini` para contar os tokens do prompt e da resposta simulada.

As tarifas configuradas são:

| Tipo | US$ por milhão de tokens |
|---|---:|
| Entrada sem cache | 0,15 |
| Saída | 0,60 |

O cálculo utilizado é:

```text
custo = (
    tokens de entrada × tarifa de entrada
    + tokens de saída × tarifa de saída
) / 1.000.000
```

O valor é exibido em dólares, com seis casas decimais.

Não há cobrança real, pois nenhuma API é chamada. A contagem considera os textos da simulação, sem incluir a estrutura adicional de mensagens de uma requisição real.

Na primeira utilização, o `tiktoken` pode precisar de conexão à internet para baixar os dados do tokenizador.

## Limitações

- Não realiza OCR de PDFs digitalizados como imagem.
- Depende dos rótulos e formatos de campos previstos.
- Não calcula experiência a partir de datas do histórico profissional.
- Não interpreta faixas salariais ou valores por extenso.
- A análise utiliza regras simples, sem compreensão semântica por um LLM real.
- A identificação de habilidades depende de palavras-chave e pode omitir ou interpretar inadequadamente informações.
- Os resultados são exibidos no terminal; não são exportados para PDF.
- Não envia o resumo ao recrutador.