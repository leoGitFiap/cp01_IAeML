"""Valida experiência mínima e pretensão salarial antes da análise simulada."""

import re

from decimal import Decimal

def aplicar_filtros(texto_curriculo, experiencia_minima_anos, orcamento_vaga):
    """Retorna a aprovação e os motivos encontrados nos dois filtros."""

    # Ignora diferenças entre letras maiúsculas e minúsculas.
    texto_minusculo = texto_curriculo.lower()

    aprovado = True

    motivos_reprovacao = []

    # Procura a experiência no campo identificado do currículo.

    campo_experiencia = re.search(
        r"^[ \t]*experi[eê]ncia(?: profissional)?[ \t]*:"
        r"[ \t]*([^\r\n]+)",
        texto_minusculo,
        flags=re.MULTILINE,
    )

    if campo_experiencia is None:
        aprovado = False
        motivos_reprovacao.append(
            "Informação de experiência não encontrada no currículo.\n"
        )

    else:
        experiencia_informada = campo_experiencia.group(1).strip()

        # Aceita um número, uma unidade opcional e o texto "de experiência".
        padrao_experiencia = (
            r"(\d+(?:[.,]\d+)?)"
            r"\s*"
            r"(anos?|meses|mês|mes)?"
            r"(?:\s+de\s+experiência)?"
            r"\.?"
        )

        # Valida o campo inteiro para evitar a leitura de valores incompletos.
        correspondencia_experiencia = re.fullmatch(
            padrao_experiencia,
            experiencia_informada,
            flags=re.IGNORECASE,
        )

        if correspondencia_experiencia is None:
            aprovado = False
            motivos_reprovacao.append(
                f"Formato de experiência inválido: "
                f"{experiencia_informada!r}. "
                "Use, por exemplo, '28 anos' ou '18 meses'.\n"
            )

        else:
            valor_experiencia = float(
                correspondencia_experiencia.group(1).replace(",", ".")
            )

            # Valores sem unidade são considerados em anos.
            unidade = (correspondencia_experiencia.group(2) or "anos").lower()

            # Converte meses para a mesma unidade do requisito da vaga.
            if unidade in ("meses", "mês", "mes"):
                experiencia_anos = valor_experiencia / 12
            else:
                experiencia_anos = valor_experiencia

            if experiencia_anos < experiencia_minima_anos:
                aprovado = False
                motivos_reprovacao.append(
                    f"Experiência insuficiente: "
                    f"{experiencia_anos:g} anos. "
                    f"Mínimo exigido: "
                    f"{experiencia_minima_anos:g} anos.\n"
                )

    # Procura a pretensão salarial no formato brasileiro.

    rotulo_salario = "pretensão salarial:"

    padrao_salario = (
        re.escape(rotulo_salario)
        + r"\s*(?:r\$|\$)?\s*"
        + r"(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d{2}))?(?![\d.,])"
    )

    correspondencia_salario = re.search(padrao_salario, texto_minusculo)

    if correspondencia_salario:
        # Remove os pontos de milhar e separa os centavos.
        parte_inteira = correspondencia_salario.group(1).replace(".", "")
        centavos = correspondencia_salario.group(2) or "00"

        # Decimal mantém a precisão dos valores monetários.
        salario_pretendido = Decimal(
            f"{parte_inteira}.{centavos}"
        )
        valor_orcamento = Decimal(str(orcamento_vaga))

        if salario_pretendido > valor_orcamento:
            aprovado = False
            motivos_reprovacao.append(
                f"Pretensão salarial ({salario_pretendido}) "
                f"acima do orçamento ({valor_orcamento}).\n"
            )
    else:
        aprovado = False
        motivos_reprovacao.append(
            "Pretensão salarial ausente ou em formato inválido no currículo.\n"
        )

    # A reprovação de um filtro não impede a verificação do outro.
    return aprovado, motivos_reprovacao