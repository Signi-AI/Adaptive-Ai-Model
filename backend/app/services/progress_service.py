from app.schemas.progress import ProgressResponse
from app.adaptive.performance_analyzer import PerformanceAnalyzer


class ProgressService:
    """
    Service layer between routes and analysis logic.
    Routes call this — this calls PerformanceAnalyzer.
    """

    def __init__(self):
        self.analyzer = PerformanceAnalyzer()

    def get_student_progress(self, student_id: int) -> ProgressResponse:
        # TODO: fetch real topic list for this student
        placeholder_topics = [self.analyzer.analyze_topic(student_id, topic_id=1)]

        return ProgressResponse(
            student_id=student_id,
            topics=placeholder_topics,
        )