"""Performance analyzer: turns attempts + mastery into strengths and weaknesses.

Analysis only: no database, no API, no framework imports, nothing is saved.
Inputs are plain records, so the rules can be tested without a database.
"""
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class AttemptRecord:
    """One answered question (built from the Attempt model by the service)."""

    topic_id: int
    is_correct: bool
    created_at: datetime
    question_id: Optional[int] = None
    response_time: Optional[float] = None  # seconds


@dataclass(frozen=True)
class MasteryRecord:
    """Current mastery of one topic (produced by the BKT engine)."""

    topic_id: int
    mastery: float  # 0-1


@dataclass(frozen=True)
class AnalyzerConfig:
    """All thresholds in one place so they are easy to review and change."""

    weak_threshold: float = 0.4    # mastery below this = weak
    strong_threshold: float = 0.8  # mastery at or above this = strong
    min_attempts: int = 3          # attempts needed before judging a topic
    repeated_mistake_count: int = 3  # wrong answers in a row / on one question
    slow_seconds: float = 30.0     # average time above this = slow

    def __post_init__(self):
        if not 0.0 <= self.weak_threshold < self.strong_threshold <= 1.0:
            raise ValueError("need 0 <= weak_threshold < strong_threshold <= 1")
        if self.min_attempts < 1:
            raise ValueError("min_attempts must be at least 1")
        if self.repeated_mistake_count < 1:
            raise ValueError("repeated_mistake_count must be at least 1")
        if self.slow_seconds <= 0:
            raise ValueError("slow_seconds must be greater than 0")


DEFAULT_CONFIG = AnalyzerConfig()


@dataclass(frozen=True)
class RepeatedMistakes:
    topic_ids: List[int]     # topics where the latest answers are all wrong
    question_ids: List[int]  # questions answered wrongly again and again


@dataclass(frozen=True)
class PerformanceSummary:
    total_attempts: int
    correct_attempts: int
    accuracy: float  # 0-1, 0.0 when there are no attempts
    average_response_time: Optional[float]  # seconds, None if no timing data
    weak_topics: List[int]
    strong_topics: List[int]
    repeated_mistake_topics: List[int]
    repeated_mistake_questions: List[int]
    slow_topics: List[int]


def _group_by_topic(attempts: Iterable[AttemptRecord]) -> Dict[int, List[AttemptRecord]]:
    grouped: Dict[int, List[AttemptRecord]] = defaultdict(list)
    for attempt in attempts:
        grouped[attempt.topic_id].append(attempt)
    return grouped


def find_weak_topics(
    mastery: Iterable[MasteryRecord],
    attempts: Iterable[AttemptRecord],
    config: AnalyzerConfig = DEFAULT_CONFIG,
) -> List[int]:
    """Topic ids with low mastery, weakest first."""
    counts = {t: len(a) for t, a in _group_by_topic(attempts).items()}
    # min_attempts stops brand-new topics (starting mastery) from looking weak
    weak = [
        m
        for m in mastery
        if m.mastery < config.weak_threshold
        and counts.get(m.topic_id, 0) >= config.min_attempts
    ]
    weak.sort(key=lambda m: m.mastery)
    return [m.topic_id for m in weak]


def find_strong_topics(
    mastery: Iterable[MasteryRecord],
    attempts: Iterable[AttemptRecord],
    config: AnalyzerConfig = DEFAULT_CONFIG,
) -> List[int]:
    """Topic ids with high mastery, strongest first."""
    counts = {t: len(a) for t, a in _group_by_topic(attempts).items()}
    strong = [
        m
        for m in mastery
        if m.mastery >= config.strong_threshold
        and counts.get(m.topic_id, 0) >= config.min_attempts
    ]
    strong.sort(key=lambda m: m.mastery, reverse=True)
    return [m.topic_id for m in strong]


def _trailing_wrong_streak(attempts: List[AttemptRecord]) -> int:
    """How many of the most recent answers in a row are wrong."""
    streak = 0
    for attempt in sorted(attempts, key=lambda a: a.created_at, reverse=True):
        if attempt.is_correct:
            break
        streak += 1
    return streak


def detect_repeated_mistakes(
    attempts: Iterable[AttemptRecord],
    config: AnalyzerConfig = DEFAULT_CONFIG,
) -> RepeatedMistakes:
    """Find topics the student is currently stuck on, and questions missed often."""
    attempts = list(attempts)

    # Topic: latest N answers in a row are wrong (a later correct answer resets it)
    topic_ids = [
        topic_id
        for topic_id, topic_attempts in _group_by_topic(attempts).items()
        if _trailing_wrong_streak(topic_attempts) >= config.repeated_mistake_count
    ]

    # Question: total wrong answers on the same question (attempts without a question id are skipped)
    misses: Dict[int, int] = defaultdict(int)
    for attempt in attempts:
        if attempt.question_id is not None and not attempt.is_correct:
            misses[attempt.question_id] += 1
    question_ids = [
        q for q, count in misses.items() if count >= config.repeated_mistake_count
    ]

    return RepeatedMistakes(sorted(topic_ids), sorted(question_ids))


def average_response_time(attempts: Iterable[AttemptRecord]) -> Optional[float]:
    """Average seconds per answer, or None when no attempt has timing data."""
    times = [a.response_time for a in attempts if a.response_time is not None]
    return sum(times) / len(times) if times else None


def find_slow_topics(
    attempts: Iterable[AttemptRecord],
    config: AnalyzerConfig = DEFAULT_CONFIG,
) -> List[int]:
    """Topic ids where answers take long on average, slowest first."""
    slow = []
    for topic_id, topic_attempts in _group_by_topic(attempts).items():
        timed = [a for a in topic_attempts if a.response_time is not None]
        if len(timed) < config.min_attempts:
            continue
        average = average_response_time(timed)
        if average is not None and average > config.slow_seconds:
            slow.append((topic_id, average))
    slow.sort(key=lambda item: item[1], reverse=True)
    return [topic_id for topic_id, _ in slow]


def build_summary(
    attempts: Iterable[AttemptRecord],
    mastery: Iterable[MasteryRecord],
    config: AnalyzerConfig = DEFAULT_CONFIG,
) -> PerformanceSummary:
    """Combine every analysis into one performance summary for a student."""
    attempts = list(attempts)
    mastery = list(mastery)

    total = len(attempts)
    correct = sum(1 for a in attempts if a.is_correct)
    repeated = detect_repeated_mistakes(attempts, config)

    return PerformanceSummary(
        total_attempts=total,
        correct_attempts=correct,
        accuracy=correct / total if total else 0.0,
        average_response_time=average_response_time(attempts),
        weak_topics=find_weak_topics(mastery, attempts, config),
        strong_topics=find_strong_topics(mastery, attempts, config),
        repeated_mistake_topics=repeated.topic_ids,
        repeated_mistake_questions=repeated.question_ids,
        slow_topics=find_slow_topics(attempts, config),
    )