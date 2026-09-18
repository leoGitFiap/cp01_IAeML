# CheackPoint 1 - IA & ML - FIAP 2026

Este projeto é um pipeline automatizado para leitura, processamento e padronização de currículos em formato PDF. Ele utiliza uma abordagem de processamento em duas camadas (Determinística e Generativa) para garantir alta precisão na extração de dados e análise de perfil dos candidatos.

## Integrantes:
* Leonardo Fernandes Mesquita, RM:559623
* Vitor de Lima Domingues, RM:561008
* Giovanni Romano Provazi, RM:560434
* Caio Berardo de Araújo, RM:560357

## Funcionalidades

* **Leitura de PDFs:** Extração robusta de texto bruto a partir de currículos enviados pelos candidatos.
* **Processamento Híbrido:**
  * *Camada Determinística:* Extração baseada em regras rígidas e expressões regulares (Regex) para dados exatos.
  * *Camada Generativa:* Integração com modelos de Inteligência Artificial (LLMs) simulados para compreensão semântica, sumarização de experiências e extração de soft/hard skills.
* **Gestão de Custos:** Sistema de rastreamento de tokens integrado para monitorar e prever custos.
* **Geração de Relatórios:** Criação automatizada de um novo PDF formatado e padronizado com os dados processados do candidato.

## Estrutura do Projeto

A arquitetura do projeto está organizada da seguinte forma:

```text
cp01_IA&ML/
│
├── data/
│   └── curriculo_candidato.pdf     # Diretório para os currículos de entrada
│
├── src/
│   ├── __init__.py
│   ├── pdf_reader.py               # Módulo responsável por ler e extrair texto do PDF
│   ├── deterministic_layer.py      # Camada de regras (Regex) para dados previsíveis
│   ├── generative_layer.py         # Comunicação com IA Generativa para análise complexa
│   ├── token_tracker.py            # Monitoramento de uso de tokens da LLM
│   └── pdf_generator.py            # Módulo para gerar o PDF final padronizado
│
├── main.py                         # Ponto de entrada (orquestrador) do sistema
└── README.md                       # Documentação do projeto