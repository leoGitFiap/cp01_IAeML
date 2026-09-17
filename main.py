from src.pdf_reader import read_file_content
from src.deterministic_layer import apply_filters
from src.generative_layer import candidate_profiler

def run_resume_pipeline():

    print("=== CURRICULUM VITAE PROFILER ===")

    budget = 35000
    required_experience = 10

    file_path = "cp01\entrega\cp01_IA&ML\data\curriculo_candidato.pdf"

    print(f"\nReading file: {file_path}...")

    file_content = read_file_content(file_path)

    print("\nApplying deterministic layer:")
    meets_criteria, feedback = apply_filters(
        file_content,
        required_experience,
        budget
    )

    if not meets_criteria:
        print("-> Status: REJECTED by deterministic screening.")
        print("-> Reason(s) for rejection:")
        for reason in feedback:
            print(f"   - {reason}")
        print("-> Process terminated.")
        return

    print("-> Status: PASSED deterministic screening! Proceeding to AI script generation...")

    print("\nApplying generative layer:")
    try:
        custom_interview_guide, token_report = candidate_profiler(file_content)

        # Exibe os resultados da análise generativa
        print("\n==================================================")
        print("       ROTEIRO PERSONALIZADO GERADO PELA IA       ")
        print("==================================================")
        print(custom_interview_guide)
        
        # Exibe o relatório de consumo computacional
        print("\n==================================================")
        print("         RELATÓRIO DE CONSUMO E TOKENS            ")
        print("==================================================")
        print(f"• Model Used                : {token_report['model']}")
        print(f"• Prompt Tokens             : {token_report['prompt_tokens']}")
        print(f"• Response Tokens           : {token_report['response_tokens']}")
        print(f"• Total Token Usage         : {token_report['token_total']}")
        print("==================================================")

    except Exception as e:
            print(f"[CRITICAL] Generative layer execution failed: {e}")


if __name__ == "__main__":
    run_resume_pipeline()