"""Live smoke test of the Artificial Teacher against the REAL local model (Ollama + Gemma).

Usage (from the model folder):
    python scripts/smoke_test_model.py
    python scripts/smoke_test_model.py --subject Mathematics --class-level "Form 2" --topic "Linear Equations"
    python scripts/smoke_test_model.py --class-level "Std 5" --topic "Fractions" --language sw

This is the live demo from the model issue (final acceptance test): same request, different
student state, different teaching behaviour. The automatic checks only catch structural
failures. Whether the teaching is GOOD still needs a human to read the output.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from artificial_teacher.settings import load_env  # noqa: E402
from artificial_teacher.gemma_client import GemmaClient, ModelError  # noqa: E402
from artificial_teacher.retrieval_service import RetrievalService  # noqa: E402
from artificial_teacher.student_context import AssessmentResult, StudentContext  # noqa: E402
from artificial_teacher.service import (  # noqa: E402
    ArtificialTeacherService,
    TeachingRequest,
    leaks_answer,
)

MAX_WORDS = 220


def check(label: str, ok: bool, failures: list[str]) -> None:
    print(f"    [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        failures.append(label)


def run_case(service, title, request, failures, *, forbid_answer=None):
    print(f"\n=== {title} ===")
    try:
        result = service.respond(request)
    except ModelError as exc:
        print(f"    MODEL ERROR: {exc}")
        failures.append(f"{title}: model error")
        return None
    print(f"    mode={result.teaching_mode} language={result.language} grounded={result.grounded} "
          f"latency={result.latency_ms}ms sources={len(result.sources)} warnings={result.warnings}")
    print("    ---")
    for line in result.response.splitlines():
        print(f"    {line}")
    print("    ---")
    check("reply is not empty", bool(result.response.strip()), failures)
    check(f"reply is at most {MAX_WORDS} words", len(result.response.split()) <= MAX_WORDS, failures)
    check("reply asks the student something", "?" in result.response, failures)
    if forbid_answer:
        check("reply does not reveal the verified answer", not leaks_answer(result.response, forbid_answer), failures)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="Mathematics")
    ap.add_argument("--class-level", default="Form 2")
    ap.add_argument("--topic", default="Linear Equations")
    ap.add_argument("--language", choices=["en", "sw"], default=None)
    args = ap.parse_args()

    load_env()
    client = GemmaClient()
    health = client.health()
    print(f"Ollama reachable: {health['reachable']}   model '{client.model}' installed: {health['model_installed']}")
    if not health["reachable"]:
        print("\nOllama is not running. Start it (Windows: open the Ollama app; Linux: 'ollama serve'), then re-run.")
        return 2
    if not health["model_installed"]:
        print(f"\nModel not installed. Run:  ollama pull {client.model}\nInstalled now: {health['installed_models']}")
        return 2

    retriever = RetrievalService()
    cov = retriever.coverage(args.subject, args.class_level, args.topic)
    print(f"Curriculum chunks loaded: {retriever.chunk_count}   for this topic: {cov['topic_chunks']}   "
          f"for this subject+class: {cov['subject_chunks']}")
    if cov["topic_chunks"] == 0:
        print("WARNING: no chunks for this topic. The teacher will answer WITHOUT textbook excerpts (ungrounded).")

    service = ArtificialTeacherService(client, retriever)
    failures: list[str] = []
    message = "I do not understand this. Can you help me?"

    weak = StudentContext(display_name="Asha", class_level=args.class_level, mastery=0.30,
                          weaknesses=["basic steps"], recent_performance="poor", recommended_action="REVISE")
    strong = StudentContext(display_name="Juma", class_level=args.class_level, mastery=0.92,
                            strengths=["basic steps"], recent_performance="excellent", recommended_action="ADVANCE")

    a = run_case(service, "A. Weak student, REVISE",
                 TeachingRequest(subject=args.subject, topic=args.topic, student=weak, message=message,
                                 teaching_language=args.language), failures)
    b = run_case(service, "B. Strong student, ADVANCE (same message)",
                 TeachingRequest(subject=args.subject, topic=args.topic, student=strong, message=message,
                                 teaching_language=args.language), failures)
    if a and b:
        check("weak and strong students get different replies", a.response.strip() != b.response.strip(), failures)

    if args.subject.lower() == "mathematics":
        incorrect = AssessmentResult(
            question="Solve 2x + 4 = 10", student_answer="x = 2.5", is_correct=False, verified_answer="x = 3",
            verified_solution_steps=["Subtract 4 from both sides: 2x = 6", "Divide both sides by 2: x = 3"])
        run_case(service, "C. Incorrect answer, answer must stay hidden",
                 TeachingRequest(subject=args.subject, topic=args.topic, student=weak, assessment=incorrect,
                                 teaching_language=args.language), failures, forbid_answer="x = 3")

    print("\n" + ("ALL AUTOMATIC CHECKS PASSED." if not failures else f"{len(failures)} CHECK(S) FAILED: {failures}"))
    print("Now READ the three replies. Automatic checks cannot judge whether the teaching is correct or good.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
