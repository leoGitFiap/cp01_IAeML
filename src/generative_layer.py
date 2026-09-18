from src.token_tracker import count_tokens

def candidate_profiler(file_content):

    model = "gpt-4o-mini-sim"

    system_prompt = (
        "Você é um gerente de RH responsável por analisar candidatos para uma das vagas mais disputadas de sua empresa."
        "Sua missão é encontrar o próximo grande membro da equipe de Engenharia de Software."
        "Com base nos seus profundos conhecimentos, tanto sobre as necessidades específicas da empresa"
        "quanto as reais virtudes de um trabalhados experiente no mercado corporativo, analise o seguinte"
        "currículo e retorne um parecer qualitativo e um resumo executivo sobre o candidato:"
    )

    user_prompt = (
        f"""
        --- CURRÍCULO ---
        {file_content}
        """
    )

    prompt = system_prompt + user_prompt
    prompt_tokens = count_tokens(prompt, model)

    response = (
        "--- PARECER QUALITATIVO E RESUMO EXECUTIVO (SIMULAÇÃO DIDÁTICA) ---\n\n"
        "**Candidato:** Carlos Eduardo Fontes | **Pretensão Salarial:** R$ 32.457\n\n"
        "**Parecer Qualitativo: Análise de Perfil**\n"
        "• **Senioridade Implícita (Staff / Principal Engineer):** A narrativa aponta para o topo da carreira. \nO desejo de 'deixar um legado tecnológico' e a menção às 'últimas décadas' revelam um profissional com vasta maturidade, \ncujo foco transcende o código e alcança a estruturação estratégica da empresa.\n"
        "• **Soft Skills Implícitas:** Demonstra altíssima inteligência emocional e liderança colaborativa. \nAo atrelar o sucesso do software à 'harmonia e colaboração' do time, comprova ser um unificador de equipes, \nfocado na construção de ambientes de respeito mútuo e retenção de talentos.\n\n"
        "**Resumo Executivo para o Recrutador**\n"
        "Olá, equipe de atração de talentos,\n\n"
        "Apresento o perfil de Carlos Eduardo Fontes, profissional com 28 anos de experiência e expertise comprovada no desenho de sistemas complexos. \nO candidato encontra-se em um momento de busca pelo 'projeto de coroação' de sua trajetória, \nalmejando um desafio de alto impacto para a aplicação de todo o seu conhecimento.\n\n"
        "*Parecer do Consultor:* Candidato perfeitamente alinhado para posições estratégicas de liderança técnica. \nSua contratação agregará não apenas na arquitetura do software, \nmas na elevação comportamental e técnica de todo o departamento de tecnologia!"
    )
    completion_tokens = count_tokens(response, model)

    token_total = prompt_tokens + completion_tokens

    prompt_token_rate = 0.15
    completion_token_rate = 0.60

    cost = ((prompt_tokens * prompt_token_rate) + (completion_tokens * completion_token_rate) / 1000000)
    clean_cost = f"US$ {cost:.2f}"

    token_report = {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "token_total": token_total,
        "cost": clean_cost
    }

    return response, token_report