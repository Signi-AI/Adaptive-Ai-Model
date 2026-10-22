"""Builds the exact messages sent to Gemma. One stable format, used by tests, smoke test and runtime.

The model returns PLAIN TEXT. Do not ask a small local model for JSON: it breaks often.
The service wraps the text into the response contract; authoritative fields stay in the backend.
"""
from __future__ import annotations

from artificial_teacher.retrieval_service import RetrievedChunk
from artificial_teacher.student_context import AssessmentResult, Language, StudentContext, Turn

# A 4B model on a school PC is CPU-bound. Keep the teaching context focused so a
# useful short turn arrives promptly instead of making every reply process a full chapter.
MAX_CHUNK_CHARS = 700
MAX_EXCERPT_CHARS = 2000
MAX_HISTORY_TURNS = 3
MAX_TURN_CHARS = 800

LANGUAGE_RULES: dict[str, str] = {
    "en": "Reply in clear, simple English suitable for a {class_level} learner in Tanzania.",
    "sw": (
        "Jibu kwa Kiswahili sanifu, rahisi na wazi kinachomfaa mwanafunzi wa {class_level}. "
        "Use Kiswahili for all explanations. Keep mathematical/scientific symbols and any English "
        "technical terms exactly as they appear in the curriculum excerpts, and add the Kiswahili "
        "term only when you are certain of it."
    ),
}

BAND_GUIDANCE: dict[str, str] = {
    "unknown": (
        "New student, no history on this topic. Start at the basic level for their class, keep the "
        "first explanation short, and ask an early check question to discover their level."
    ),
    "low": (
        "Low understanding. Use very simple words and short sentences. Use the simplest example from "
        "the excerpts or a familiar everyday Tanzanian context. Break the idea into small steps, give "
        "more guidance and hints, and ask an easy question."
    ),
    "medium": (
        "Medium understanding. Use a moderate example. Give hints one at a time and gradually give "
        "less help. Pay extra attention to the listed weaknesses. Ask a moderately difficult question."
    ),
    "high": (
        "High understanding. Be brief and do not over-explain. Offer a challenging example or "
        "question, give minimal hints, and ask the student to explain their reasoning."
    ),
}

ACTION_GUIDANCE: dict[str, str] = {
    "INTRODUCE": "Introduce the topic from the beginning: one core idea, one example, one check question.",
    "REVISE": (
        "Revisit the idea the student is weak at, using a different and simpler explanation than a "
        "textbook one. Give one worked example, then ask them to try a similar small one."
    ),
    "REMEDIATE": (
        "The student is probably missing a prerequisite. Briefly go back to the prerequisite idea the "
        "weaknesses point to, then connect it back to the current topic."
    ),
    "PRACTICE": "Give ONE practice question at the right difficulty. Do not solve it. Wait for the answer.",
    "CONTINUE": "Continue the lesson from where the conversation stands. Do not restart the topic.",
    "ADVANCE": (
        "The student is ready for more. Confirm the idea briefly, then give a more challenging question, "
        "or introduce the next related idea only if the excerpts support it."
    ),
}

_ALIASES = {"REVIEW": "REVISE", "REMEDIATION": "REMEDIATE", "PROGRESS": "ADVANCE", "NEW": "INTRODUCE"}


def resolve_action(action: str | None, band: str) -> tuple[str, bool]:
    """Map the backend's recommended_action to one of our teaching modes.

    Returns (mode, was_recognised). Unknown/missing actions never crash the teacher.
    """
    raw = (action or "").strip().upper()
    raw = _ALIASES.get(raw, raw)
    if raw in ACTION_GUIDANCE:
        return raw, True
    return ("INTRODUCE" if band == "unknown" else "CONTINUE"), raw == ""


SYSTEM_TEMPLATE = """You are the Artificial Teacher inside TOALM, an offline learning system for Tanzanian students.
You are teaching {subject}, topic "{topic}", to a {class_level} learner.

HOW YOU TEACH
1. Teach in small steps: explain one idea, give one example, then ask the student exactly ONE question to check understanding. Never ask more than one question in a reply.
2. Guide, do not dump answers. When the student is stuck or wrong, use this ladder: a hint, then a guiding question, then a simpler worked example, and only then the full solution. Never state the final answer to the student's current question unless REVEAL ANSWER is YES.
3. Keep replies short: about 100 words at most, plain text, no tables. Use numbered steps for working. Write maths in plain text, for example 2x + 4 = 10 or 3/4.
4. Be encouraging and honest. Praise correct reasoning briefly and specifically. Do not flatter.

WHAT YOU KNOW
5. The CURRICULUM EXCERPTS below are your source for definitions, notation and examples. Prefer them. If they do not cover the question, say so honestly, use only general knowledge you are certain of, and suggest the student check with their teacher or textbook. Never invent syllabus topics, page numbers, book titles or references.
6. LEARNING STATE and ASSESSMENT RESULT come from the system and are authoritative. Never invent or guess marks, mastery, or whether an answer was correct. Never tell the student a mastery number.
7. Stay on the current topic. If the student asks about something else, say briefly that it is outside this lesson and offer to come back to the topic (they can choose another topic from the sidebar).
8. Your students are school learners, some of them children. Keep everything age-appropriate and politely decline anything that is not about learning.

LANGUAGE
{language_rule}

CURRICULUM EXCERPTS
{excerpts}

LEARNING STATE (from the system)
Class: {class_level}
Student: {student_line}
Understanding of this topic: {band}
Recent performance: {recent}
Strengths: {strengths}
Weaknesses: {weaknesses}
Recommended action: {action}

TEACHING PLAN FOR THIS REPLY
{band_guidance}
{action_guidance}
{assessment_block}"""


def _format_excerpts(hits: list[RetrievedChunk]) -> str:
    if not hits:
        return (
            "(No curriculum excerpt was found for this request. If you are unsure, say so and do not "
            "invent curriculum content.)"
        )
    parts: list[str] = []
    budget = MAX_EXCERPT_CHARS
    for i, hit in enumerate(hits, 1):
        c = hit.chunk
        text = c.text[:MAX_CHUNK_CHARS]
        if parts and len(text) > budget:
            break
        budget -= len(text)
        pages = f"p.{c.page_start}" if c.page_start == c.page_end else f"pp.{c.page_start}-{c.page_end}"
        parts.append(f"[{i}] ({c.source}, {pages})\n{text}")
    note = ""
    if any(h.scope == "subject" for h in hits):
        note = "(These excerpts come from elsewhere in the same subject and class, not the selected topic.)\n"
    return note + "\n\n".join(parts)


def _format_assessment(a: AssessmentResult | None) -> str:
    if a is None:
        return ""
    lines = [
        "",
        "ASSESSMENT RESULT (verified by the system, do not re-judge it)",
        f"Question: {a.question}",
        f"Student's answer: {a.student_answer}",
        f"Result: {'CORRECT' if a.is_correct else 'INCORRECT'}",
        f"REVEAL ANSWER: {'YES' if a.reveal_answer else 'NO'}",
    ]
    if a.verified_answer:
        suffix = "" if a.reveal_answer else " (for your reference only, do NOT state it)"
        lines.append(f"Verified answer: {a.verified_answer}{suffix}")
    if a.verified_solution_steps:
        lines.append("Verified solution steps (for your reference):")
        lines += [f"  {n}. {s}" for n, s in enumerate(a.verified_solution_steps, 1)]
    if a.is_correct:
        lines.append("Instruction: confirm briefly why it is right, then give one slightly harder question.")
    else:
        lines.append(
            "Instruction: do not just say it is wrong. Use the verified steps to find the likely step where "
            "the student went wrong, explain that idea simply, and ask them to try again."
        )
    return "\n".join(lines)


def build_system_prompt(
    *,
    subject: str,
    topic: str,
    student: StudentContext,
    language: Language,
    hits: list[RetrievedChunk],
    assessment: AssessmentResult | None,
) -> tuple[str, str, bool]:
    """Returns (system_prompt, resolved_action, action_recognised)."""
    band = student.band
    action, recognised = resolve_action(student.recommended_action, band)
    first_name = (student.display_name or "").split(" ")[0]
    prompt = SYSTEM_TEMPLATE.format(
        subject=subject,
        topic=topic,
        class_level=student.class_level,
        language_rule=LANGUAGE_RULES[language].format(class_level=student.class_level),
        excerpts=_format_excerpts(hits),
        student_line=f"{first_name} (use the first name occasionally)" if first_name else "(name unknown)",
        band=band.upper(),
        recent=student.recent_performance,
        strengths=", ".join(student.strengths) or "none recorded",
        weaknesses=", ".join(student.weaknesses) or "none recorded",
        action=action,
        band_guidance=BAND_GUIDANCE[band],
        action_guidance=ACTION_GUIDANCE[action],
        assessment_block=_format_assessment(assessment),
    )
    return prompt, action, recognised


def build_messages(
    *,
    system_prompt: str,
    history: list[Turn],
    user_message: str,
) -> list[dict[str, str]]:
    """System prompt + recent history + the new student message, with roles merged so they alternate."""
    turns: list[dict[str, str]] = []

    def add(role: str, content: str) -> None:
        if turns and turns[-1]["role"] == role:
            turns[-1]["content"] += "\n\n" + content
        else:
            turns.append({"role": role, "content": content})

    for t in history[-MAX_HISTORY_TURNS:]:
        add("user" if t.role == "student" else "assistant", t.content[:MAX_TURN_CHARS])
    add("user", user_message)
    while turns and turns[0]["role"] == "assistant":
        turns.pop(0)
    return [{"role": "system", "content": system_prompt}, *turns]
