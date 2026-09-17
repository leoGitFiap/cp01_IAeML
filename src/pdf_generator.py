import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(current_dir) == 'src':
        project_root = os.path.dirname(current_dir)
    else:
        project_root = current_dir

    output_dir = os.path.join(project_root, "data")
    file_name = "curriculo_candidato.pdf" # Changed to match your file tree
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, file_name)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "CURRÍCULO PROFISSIONAL")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 70, "-" * 80)
    c.drawString(50, height - 100, "Nome: Carlos Eduardo Fontes")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 140, "Dados Objetivos:")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 160, "Experiência: 28")
    c.drawString(50, height - 180, "Pretensão salarial: R$ 32.457")
    
    c.drawString(50, height - 210, "-" * 80)
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 240, "Resumo da Trajetória:")
    
    text_object = c.beginText(50, height - 265)
    text_object.setFont("Helvetica", 11)
    text_object.setLeading(15) # Line spacing
    
    narrative = (
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
    
    for line in narrative.split('\n'):
        text_object.textLine(line)
        
    c.drawText(text_object)

    c.save()
    print(f"File '{file_name}' successfully saved to '{output_dir}'.")

if __name__ == "__main__":
    generate_pdf()