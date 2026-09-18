"""Lê PDFs com texto extraível. Não realiza reconhecimento de imagens (OCR)."""

from pypdf import PdfReader

def extrair_texto_pdf(caminho_arquivo):
    """Extrai o texto das páginas; retorna texto vazio se a leitura falhar."""

    try:
        leitor = PdfReader(caminho_arquivo)

        texto_curriculo = ""

        # Percorre as páginas na ordem e separa seus textos por uma quebra de linha.
        for pagina in leitor.pages:
            texto_pagina = pagina.extract_text()

            # Páginas sem texto extraível não acrescentam conteúdo.
            if texto_pagina:
                texto_curriculo += texto_pagina + "\n"

        return texto_curriculo

    except Exception as erro:
        # Informa a falha para que o fluxo principal encerre a triagem.
        print(f"Erro ao ler o PDF: {erro}.")
        return ""
