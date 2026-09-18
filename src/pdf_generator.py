"""Gera o currículo de entrada usado como exemplo no projeto."""

import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_curriculo_exemplo():
    """Cria o currículo de exemplo e sobrescreve o PDF de mesmo nome."""

    # Encontra a raiz do projeto a partir da localização deste módulo.
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(pasta_atual) == 'src':
        raiz_projeto = os.path.dirname(pasta_atual)
    else:
        raiz_projeto = pasta_atual

    pasta_saida = os.path.join(raiz_projeto, "data")
    nome_arquivo = "curriculo_candidato.pdf"
    
    # Cria a pasta de dados caso ela ainda não exista.
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        
    caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

    # Abre um PDF em tamanho carta e define a área de desenho.
    documento = canvas.Canvas(caminho_arquivo, pagesize=letter)
    largura, altura = letter
    
    # Escreve o título e os campos usados pelos filtros.
    documento.setFont("Helvetica-Bold", 14)
    documento.drawString(50, altura - 50, "CURRÍCULO PROFISSIONAL")
    documento.setFont("Helvetica", 11)
    documento.drawString(50, altura - 70, "-" * 80)
    documento.drawString(50, altura - 100, "Nome: Carlos Eduardo Fontes")
    
    documento.setFont("Helvetica-Bold", 11)
    documento.drawString(50, altura - 140, "Dados Objetivos:")
    documento.setFont("Helvetica", 11)
    documento.drawString(50, altura - 160, "Experiência: 28 anos")
    documento.drawString(50, altura - 180, "Pretensão salarial: R$ 32.457")
    
    documento.drawString(50, altura - 210, "-" * 80)
    
    documento.setFont("Helvetica-Bold", 11)
    documento.drawString(50, altura - 240, "Resumo da Trajetória:")
    
    bloco_texto = documento.beginText(50, altura - 265)
    bloco_texto.setFont("Helvetica", 11)
    bloco_texto.setLeading(15)
    
    # Texto fixo de exemplo para exercitar a análise de perfil.
    resumo_trajetoria = (
        "Busco a consolidação da minha trajetória técnica assumindo a vanguarda de uma\n"
        "iniciativa de alto impacto. Ao longo das últimas décadas, dediquei-me a arquitetar\n"
        "sistemas complexos e, neste momento específico da minha jornada, procuro um projeto\n"
        "desafiador onde eu possa aplicar todo o conhecimento acumulado e deixar um legado\n"
        "tecnológico sólido antes de encerrar meu ciclo no mercado corporativo.\n\n"
        "Sempre acreditei que o sucesso estrutural de um software é o reflexo direto da\n"
        "harmonia e colaboração das equipes que o constroem. Tive o privilégio de guiar\n"
        "arquiteturas que se tornaram referência nos corredores das empresas por onde passei,\n"
        "mas meu maior orgulho é o ambiente de respeito mútuo que ajudei a cultivar,\n"
        "formando parcerias e laços profissionais que perduram até hoje."
    )
    
    # Desenha cada linha do resumo com o espaçamento configurado.
    for linha in resumo_trajetoria.split('\n'):
        bloco_texto.textLine(linha)
        
    documento.drawText(bloco_texto)

    # Finaliza a escrita do arquivo em disco.
    documento.save()
    print(f"Arquivo '{nome_arquivo}' salvo em '{pasta_saida}'.")

if __name__ == "__main__":
    gerar_curriculo_exemplo()
