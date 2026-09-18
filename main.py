from src.pdf_reader import read_file_content
from src.deterministic_layer import apply_filters
from src.generative_layer import candidate_profiler
from pathlib import Path

def run_resume_pipeline():

    print("\n=== RESUME PROFILER ===")

    budget = 35000
    required_experience = 10

    file_path = (
        Path(__file__).resolve().parent
        / "data"
        / "curriculo_candidato.pdf"
    )

    print(f"\nReading file: {file_path}...")

    file_content = read_file_content(file_path)

    print("\nApplying deterministic layer:\n")
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

        print("\n" + "=" * 52)
        print("                  CUSTOM AI GUIDE")
        print("=" * 52)
        print(custom_interview_guide)
        
        print("\n" + "=" * 52)
        print("                TOKEN USAGE REPORT")
        print("=" * 52)
        print(f"• Model Used              :   {token_report['model']}")
        print(f"• Prompt Tokens           :   {token_report['prompt_tokens']}")
        print(f"• Completion Tokens       :   {token_report['completion_tokens']}")
        print(f"• Total Token Usage       :   {token_report['token_total']}")
        print(f"• Total Operation Cost    :   {token_report['cost']}")
        print("=" * 52)

    except Exception as e:
            print(f"[CRITICAL] Generative layer execution failed: {e}")


if __name__ == "__main__":
    run_resume_pipeline()