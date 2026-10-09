from fastapi import APIRouter

from app.api.routes import (
    academic_levels,
    adaptive,
    Admin,
    auth,
    curriculum,
    health,
    learning,
    learning_objectives,
    lesson,
    mastery,
    progress,
    recommendations,
    sessions,
    student_curriculum,
    students,
    subjects,
    teacher,
    topics,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(students.router)
api_router.include_router(learning.router)
api_router.include_router(teacher.router)
api_router.include_router(Admin.router)
api_router.include_router(health.router)
api_router.include_router(sessions.router)
api_router.include_router(academic_levels.router)
api_router.include_router(subjects.router)
api_router.include_router(topics.router)
api_router.include_router(lesson.router)
api_router.include_router(learning_objectives.router)
api_router.include_router(curriculum.router)
api_router.include_router(student_curriculum.router)
api_router.include_router(adaptive.router)
api_router.include_router(mastery.router)
api_router.include_router(progress.router)
api_router.include_router(recommendations.router)
