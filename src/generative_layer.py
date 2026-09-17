from token_tracker import count_tokens

def candidate_profiler(file_content, y):

    model = "gpt-4o-mini-sim"

    system_prompt = (
        "Você é um gerente de RH responsável por analisar candidatos para uma das vagas mais disputadas de sua empresa."
        "Sua missão é encontrar o próximo grande membro da equipe de Engenharia de Software."
    )

    user_prompt = (
        f"""
        Com base nos seus profundos conhecimentos, tanto sobre as necessidades específicas da empresa
        quanto as reais virtudes de um trabalhados experiente no mercado corporativo, analise o seguinte
        currículo e retorne um parecer qualitativo e um resumo executivo sobre o candidato:

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
        "• **Senioridade Implícita (Staff / Principal Engineer):** A narrativa aponta para o topo da carreira. O desejo de 'deixar um legado tecnológico' e a menção às 'últimas décadas' revelam um profissional com vasta maturidade, cujo foco transcende o código e alcança a estruturação estratégica da empresa.\n"
        "• **Soft Skills Implícitas:** Demonstra altíssima inteligência emocional e liderança colaborativa. Ao atrelar o sucesso do software à 'harmonia e colaboração' do time, comprova ser um unificador de equipes, focado na construção de ambientes de respeito mútuo e retenção de talentos.\n\n"
        "**Resumo Executivo para o Recrutador**\n"
        "Olá, equipe de atração de talentos,\n\n"
        "Apresento o perfil de Carlos Eduardo Fontes, profissional com 28 anos de experiência e expertise comprovada no desenho de sistemas complexos. O candidato encontra-se em um momento de busca pelo 'projeto de coroação' de sua trajetória, almejando um desafio de alto impacto para a aplicação de todo o seu conhecimento.\n\n"
        "*Parecer do Consultor:* Candidato perfeitamente alinhado para posições estratégicas de liderança técnica. Sua contratação agregará não apenas na arquitetura do software, mas na elevação comportamental e técnica de todo o departamento de tecnologia!"
    )
    response_tokens = count_tokens(response, model)

    tokens_total = prompt_tokens + response_tokens

    tokens_report = {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "tokens_total": tokens_total
    }

    return ""