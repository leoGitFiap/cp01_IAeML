"""Controla a execução da triagem e exibe os resultados no terminal."""

from pathlib import Path

from src.pdf_reader import extrair_texto_pdf
from src.deterministic_layer import aplicar_filtros
from src.generative_layer import analisar_curriculo


def executar_triagem():
    """Lê o currículo, aplica os filtros e mostra a análise simulada."""

    print("\n=== TRIAGEM DE CURRÍCULOS ===")

    # Define o salário máximo e a experiência mínima da vaga.
    orcamento_vaga = 35000
    experiencia_minima = 10

    # Localiza o PDF a partir da pasta deste arquivo.
    caminho_arquivo = (
        Path(__file__).resolve().parent
        / "data"
        / "curriculo_candidato.pdf"
    )

    print(f"\nLendo arquivo: {caminho_arquivo}...")

    texto_curriculo = extrair_texto_pdf(caminho_arquivo)

    # Um PDF sem texto não deve ser tratado como reprovação do candidato.
    if not texto_curriculo.strip():
        print("-> Processo encerrado: PDF indisponível ou sem texto extraível.")
        return

    print("\nAplicando filtros de experiência e salário:\n")
    atende_requisitos, motivos_reprovacao = aplicar_filtros(
        texto_curriculo,
        experiencia_minima,
        orcamento_vaga
    )

    # Encerra antes da simulação quando algum requisito não é atendido.
    if not atende_requisitos:
        print("-> Situação: REPROVADO nos filtros.")
        print("-> Motivos da reprovação:")
        for motivo in motivos_reprovacao:
            print(f"   - {motivo}")
        print("-> Processo encerrado.")
        return

    print("-> Situação: APROVADO nos filtros. Iniciando análise simulada...")

    print("\nGerando parecer simulado:")
    # A análise só é gerada para candidatos aprovados nos dois filtros.
    try:
        parecer, relatorio_uso = analisar_curriculo(texto_curriculo)

        print("\n" + "=" * 52)
        print("                  ANÁLISE SIMULADA DO PERFIL")
        print("=" * 52)
        print(parecer)
        
        print("\n" + "=" * 52)
        print("                RELATÓRIO DE USO DE TOKENS")
        print("=" * 52)
        print(f"• Modelo de referência    :   {relatorio_uso['modelo']}")
        print(f"• Tokens de entrada       :   {relatorio_uso['tokens_entrada']}")
        print(f"• Tokens de saída         :   {relatorio_uso['tokens_saida']}")
        print(f"• Total de tokens         :   {relatorio_uso['total_tokens']}")
        print(f"• Custo estimado          :   {relatorio_uso['custo_estimado']}")
        print("=" * 52)

    except Exception as erro:
        print(f"[ERRO] Falha na análise simulada: {erro}")


if __name__ == "__main__":
    executar_triagem()
