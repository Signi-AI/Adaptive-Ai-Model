from app.schemas.progress import TopicPerformance


class PerformanceAnalyzer:
    """
    Computes topic-level performance for a student.
    No BKT/AI logic yet — this is a skeleton returning placeholder data,
    per issue scope (API and service contracts only).
    """

    def analyze_topic(self, student_id: int, topic_id: int) -> TopicPerformance:
        # TODO: replace with real calculation once BKT is implemented
        return TopicPerformance(
            topic_id=topic_id,
            topic_name="placeholder_topic",
            mastery_score=0.0,
            attempts_count=0,
            correct_count=0,
        )