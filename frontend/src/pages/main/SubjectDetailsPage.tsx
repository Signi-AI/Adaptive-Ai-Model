// SubjectDetailsPage.tsx
import React from "react";
import { useParams,  } from "react-router-dom";
import StudentSidebar from "../main/StudentSidebar";

// Subject database object
const SUBJECT_DATA: Record<string, { title: string; form: string; description: string }> = {
  physics: {
    title: "Physics & Mechanics",
    form: "Form 2 Physics",
    description: "Master the fundamental laws of motion, force, energy, and physical mechanics.",
  },
  math: {
    title: "Mathematics & Algebra",
    form: "Form 2 Math",
    description: "Learn algebraic expressions, linear equations, geometry, and calculus concepts.",
  },
  chemistry: {
    title: "Chemistry & Matter",
    form: "Form 2 Chemistry",
    description: "Explore atomic structures, chemical bonding, elements, and periodic table trends.",
  },
};

const SubjectDetailsPage: React.FC = () => {
  // Extract "physics" or "math" from URL (/subjects/:subjectId)
  const { subjectId } = useParams<{ subjectId: string }>();

  // Get current subject data or fallback to generic layout
  const currentSubject = subjectId && SUBJECT_DATA[subjectId] 
    ? SUBJECT_DATA[subjectId] 
    : {
        title: subjectId ? subjectId.toUpperCase() : "Subject Details",
        form: "Form 2",
        description: "Explore subject topics, practice with AI Tutor, and complete lessons.",
      };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <StudentSidebar />

      <main className="ml-60 min-h-screen p-8">
        <div className="mb-6">
          <span className="text-xs font-bold uppercase text-purple-600">
            {currentSubject.form}
          </span>
          <h1 className="text-3xl font-extrabold text-slate-900">
            {currentSubject.title}
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            {currentSubject.description}
          </p>
        </div>

        {/* Dynamic content cards go here */}
      </main>
    </div>
  );
};

export default SubjectDetailsPage;