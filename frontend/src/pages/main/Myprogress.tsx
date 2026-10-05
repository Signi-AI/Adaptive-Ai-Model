import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  Award,
  BookOpen,
  Camera,
  CheckCircle2,
  Edit3,
  Flame,
  Sparkles,
  Target,
  TrendingUp,
  X,
} from "lucide-react";
import logo from "../../assets/logo.jpeg";
import StudentSidebar from "./StudentSidebar";

interface Student {
  name: string;
  level: string;
  className: string;
  school: string;
}

interface Subject {
  id: string;
  name: string;
  progress: number;
  category: "Science" | "Mathematics" | "Languages" | "Arts";
  topicsCompleted: number;
  totalTopics: number;
}

interface CircularProgressProps {
  value: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
}

const INITIAL_STUDENT: Student = {
  name: "Comfotha Mwansasule",
  level: "Secondary School",
  className: "Form 3",
  school: "Example Secondary School",
};

const INITIAL_SUBJECTS: Subject[] = [
  {
    id: "math",
    name: "Mathematics",
    progress: 72,
    category: "Mathematics",
    topicsCompleted: 18,
    totalTopics: 25,
  },
  {
    id: "english",
    name: "English",
    progress: 81,
    category: "Languages",
    topicsCompleted: 21,
    totalTopics: 26,
  },
  {
    id: "biology",
    name: "Biology",
    progress: 70,
    category: "Science",
    topicsCompleted: 14,
    totalTopics: 20,
  },
  {
    id: "chemistry",
    name: "Chemistry",
    progress: 63,
    category: "Science",
    topicsCompleted: 12,
    totalTopics: 19,
  },
  {
    id: "physics",
    name: "Physics",
    progress: 52,
    category: "Science",
    topicsCompleted: 11,
    totalTopics: 21,
  },
];

const CircularProgress: React.FC<CircularProgressProps> = ({
  value,
  size = 120,
  strokeWidth = 10,
  label,
}) => {
  const safeValue = Math.min(100, Math.max(0, value));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset =
    circumference - (safeValue / 100) * circumference;

  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="-rotate-90"
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-slate-200"
        />

        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="text-blue-600 transition-all duration-700"
        />
      </svg>

      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-xl font-bold text-slate-800">
          {safeValue}%
        </span>

        {label && (
          <span className="mt-0.5 text-[11px] font-medium text-slate-500">
            {label}
          </span>
        )}
      </div>
    </div>
  );
};

const Profile: React.FC = () => {
  const navigate = useNavigate();

  const [student] = useState<Student>(() => {
    try {
      const saved = localStorage.getItem(
        "student_profile_data"
      );

      return saved ? JSON.parse(saved) : INITIAL_STUDENT;
    } catch {
      return INITIAL_STUDENT;
    }
  });

  const [profileImage] = useState<string>(() => {
    try {
      return (
        localStorage.getItem("student_profile_image") || ""
      );
    } catch {
      return "";
    }
  });

  const [subjects, setSubjects] = useState<Subject[]>(() => {
    try {
      const saved = localStorage.getItem(
        "student_subjects_data"
      );

      return saved ? JSON.parse(saved) : INITIAL_SUBJECTS;
    } catch {
      return INITIAL_SUBJECTS;
    }
  });

  const [selectedSubject, setSelectedSubject] =
    useState<Subject | null>(null);

  const [isUpdatingSubject, setIsUpdatingSubject] =
    useState(false);

  const [editSubjectData, setEditSubjectData] = useState({
    progress: 0,
    topicsCompleted: 0,
  });

  useEffect(() => {
    localStorage.setItem(
      "student_subjects_data",
      JSON.stringify(subjects)
    );
  }, [subjects]);

  const overallProgress = useMemo(() => {
    if (!subjects.length) return 0;

    const total = subjects.reduce(
      (sum, subject) => sum + subject.progress,
      0
    );

    return Math.round(total / subjects.length);
  }, [subjects]);

  const totalTopicsDone = useMemo(() => {
    return subjects.reduce(
      (sum, subject) => sum + subject.topicsCompleted,
      0
    );
  }, [subjects]);

  const totalTopics = useMemo(() => {
    return subjects.reduce(
      (sum, subject) => sum + subject.totalTopics,
      0
    );
  }, [subjects]);

  const lowestSubject = useMemo(() => {
    if (!subjects.length) return null;

    return subjects.reduce((lowest, subject) =>
      subject.progress < lowest.progress
        ? subject
        : lowest
    );
  }, [subjects]);

  const getStatusBadge = (progress: number) => {
    if (progress >= 80) {
      return {
        label: "Mastered",
        className:
          "bg-green-50 text-green-700 border-green-200",
      };
    }

    if (progress >= 60) {
      return {
        label: "On Track",
        className:
          "bg-blue-50 text-blue-700 border-blue-200",
      };
    }

    return {
      label: "Needs Review",
      className:
        "bg-amber-50 text-amber-700 border-amber-200",
    };
  };

  const getCategoryClass = (
    category: Subject["category"]
  ) => {
    switch (category) {
      case "Mathematics":
        return "bg-blue-50 text-blue-700";

      case "Science":
        return "bg-green-50 text-green-700";

      case "Languages":
        return "bg-sky-50 text-sky-700";

      case "Arts":
        return "bg-amber-50 text-amber-700";

      default:
        return "bg-slate-50 text-slate-700";
    }
  };

  const handleOpenSubjectEdit = (subject: Subject) => {
    setSelectedSubject(subject);

    setEditSubjectData({
      progress: subject.progress,
      topicsCompleted: subject.topicsCompleted,
    });

    setIsUpdatingSubject(true);
  };

  const handleSaveSubjectProgress = () => {
    if (!selectedSubject) return;

    const progress = Math.min(
      100,
      Math.max(
        0,
        Number(editSubjectData.progress) || 0
      )
    );

    const topicsCompleted = Math.min(
      selectedSubject.totalTopics,
      Math.max(
        0,
        Number(editSubjectData.topicsCompleted) || 0
      )
    );

    setSubjects((currentSubjects) =>
      currentSubjects.map((subject) =>
        subject.id === selectedSubject.id
          ? {
              ...subject,
              progress,
              topicsCompleted,
            }
          : subject
      )
    );

    setIsUpdatingSubject(false);
    setSelectedSubject(null);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <StudentSidebar />

      <main className="ml-60 min-h-screen">
        <div className="mx-auto max-w-7xl px-6 py-8">

          {/* Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <p className="mb-1 text-sm font-medium text-blue-600">
                Student Learning
              </p>

              <h1 className="text-3xl font-bold text-slate-800">
                My Progress
              </h1>

              <p className="mt-1 text-sm text-slate-500">
                Track your learning progress and academic performance.
              </p>
            </div>

            <button
              onClick={() => navigate("/learn")}
              className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
            >
              Back to Learning
              <ArrowRight size={17} />
            </button>
          </div>

          {/* Student Name + Profile Picture + Overall Progress */}
          <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-7 shadow-sm">
            <div className="flex flex-col items-center">

              {/* Profile Picture */}
              <div className="relative">
                <div className="flex h-24 w-24 items-center justify-center overflow-hidden rounded-full border-4 border-white bg-slate-100 shadow-md ring-1 ring-slate-200">
                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt={student.name}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <img
                      src={logo}
                      alt="Student"
                      className="h-full w-full object-cover"
                    />
                  )}
                </div>

                <div className="absolute bottom-0 right-0 flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-blue-600 text-white">
                  <Camera size={14} />
                </div>
              </div>

              {/* Student Name */}
              <h2 className="mt-4 text-2xl font-bold text-slate-800">
                {student.name}
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {student.className} • {student.level}
              </p>

              {/* Overall Progress */}
              <div className="mt-7 flex flex-col items-center">
                <div className="mb-3 flex items-center gap-2">
                  <TrendingUp
                    size={18}
                    className="text-blue-600"
                  />

                  <h3 className="font-semibold text-slate-800">
                    Overall Progress
                  </h3>
                </div>

                <CircularProgress
                  value={overallProgress}
                  size={175}
                  strokeWidth={13}
                  label="Complete"
                />

                <p className="mt-4 text-sm font-semibold text-slate-700">
                  {overallProgress >= 80
                    ? "Excellent progress!"
                    : overallProgress >= 60
                    ? "You're on the right track!"
                    : "Keep working consistently!"}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  {totalTopicsDone} of {totalTopics} topics completed
                </p>
              </div>
            </div>
          </section>

          {/* Summary */}
          <section className="mb-8">
            <div className="grid gap-5 md:grid-cols-3">

              {/* Topics */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Topics Completed
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Total completed topics
                    </p>
                  </div>

                  <div className="rounded-xl bg-green-50 p-3 text-green-600">
                    <Target size={20} />
                  </div>
                </div>

                <div className="mt-6">
                  <span className="text-4xl font-bold text-slate-800">
                    {totalTopicsDone}
                  </span>

                  <span className="ml-2 text-sm text-slate-500">
                    / {totalTopics}
                  </span>
                </div>

                <div className="mt-5 flex items-center gap-2 rounded-xl bg-slate-50 p-3">
                  <CheckCircle2
                    size={18}
                    className="text-green-600"
                  />

                  <span className="text-xs font-medium text-slate-600">
                    Keep completing topics.
                  </span>
                </div>
              </div>

              {/* Assignments */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Assignments Done
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Completed assignments
                    </p>
                  </div>

                  <div className="rounded-xl bg-blue-50 p-3 text-blue-600">
                    <BookOpen size={20} />
                  </div>
                </div>

                <p className="mt-6 text-4xl font-bold text-slate-800">
                  18
                </p>

                <p className="mt-5 text-xs font-medium text-green-600">
                  Good completion record
                </p>
              </div>

              {/* Study Streak */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Study Streak
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Consecutive learning days
                    </p>
                  </div>

                  <div className="rounded-xl bg-amber-50 p-3 text-amber-600">
                    <Flame size={20} />
                  </div>
                </div>

                <div className="mt-6 flex items-end gap-2">
                  <span className="text-4xl font-bold text-slate-800">
                    7
                  </span>

                  <span className="mb-1 text-sm text-slate-500">
                    days
                  </span>
                </div>

                <div className="mt-5 flex items-center gap-2">
                  <Award
                    size={17}
                    className="text-amber-600"
                  />

                  <span className="text-xs font-medium text-amber-600">
                    Keep it going!
                  </span>
                </div>
              </div>
            </div>
          </section>

          {/* Subject Progress */}
          <section className="mb-8">
            <div className="mb-5">
              <h2 className="text-xl font-bold text-slate-800">
                Subject Progress
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Monitor your progress in each subject.
              </p>
            </div>

            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {subjects.map((subject) => {
                const status = getStatusBadge(
                  subject.progress
                );

                return (
                  <div
                    key={subject.id}
                    className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <div className="rounded-lg bg-slate-100 p-2 text-slate-700">
                            <BookOpen size={17} />
                          </div>

                          <h3 className="font-semibold text-slate-800">
                            {subject.name}
                          </h3>
                        </div>

                        <span
                          className={`mt-3 inline-flex rounded-full px-2.5 py-1 text-[11px] font-semibold ${getCategoryClass(
                            subject.category
                          )}`}
                        >
                          {subject.category}
                        </span>
                      </div>

                      <button
                        onClick={() =>
                          handleOpenSubjectEdit(subject)
                        }
                        className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-blue-600"
                        title="Edit progress"
                      >
                        <Edit3 size={16} />
                      </button>
                    </div>

                    <div className="mt-6 flex justify-center">
                      <CircularProgress
                        value={subject.progress}
                        size={135}
                        strokeWidth={10}
                      />
                    </div>

                    <div className="mt-5 flex items-center justify-between border-t border-slate-100 pt-4">
                      <div>
                        <p className="text-xs text-slate-500">
                          Topics
                        </p>

                        <p className="mt-1 text-sm font-semibold text-slate-800">
                          {subject.topicsCompleted} /{" "}
                          {subject.totalTopics}
                        </p>
                      </div>

                      <span
                        className={`rounded-full border px-2.5 py-1 text-[11px] font-semibold ${status.className}`}
                      >
                        {status.label}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>

          {/* AI Recommendation */}
          {lowestSubject && (
            <section className="mb-8 rounded-2xl border border-blue-100 bg-blue-50 p-6">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white text-blue-600 shadow-sm">
                    <Sparkles size={22} />
                  </div>

                  <div>
                    <p className="text-xs font-bold uppercase tracking-wide text-blue-600">
                      AI Learning Recommendation
                    </p>

                    <h3 className="mt-1 text-lg font-bold text-slate-800">
                      Focus more on {lowestSubject.name}
                    </h3>

                    <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-600">
                      Your current progress in{" "}
                      {lowestSubject.name} is{" "}
                      <strong>
                        {lowestSubject.progress}%
                      </strong>
                      . Spend more time reviewing this subject
                      to improve your overall performance.
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => navigate("/learn")}
                  className="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
                >
                  Start Learning
                  <ArrowRight size={17} />
                </button>
              </div>
            </section>
          )}

          {/* Footer */}
          <div className="rounded-2xl border border-slate-200 bg-white px-6 py-5 text-center shadow-sm">
            <p className="text-sm font-semibold text-slate-700">
              Keep learning, keep improving.
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Your learning progress is saved automatically.
            </p>
          </div>
        </div>
      </main>

      {/* Edit Progress Modal */}
      {isUpdatingSubject && selectedSubject && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-white shadow-2xl">

            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
              <div>
                <h2 className="text-lg font-bold text-slate-800">
                  Update Progress
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  {selectedSubject.name}
                </p>
              </div>

              <button
                onClick={() => {
                  setIsUpdatingSubject(false);
                  setSelectedSubject(null);
                }}
                className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-5 p-6">

              <div className="flex justify-center">
                <CircularProgress
                  value={editSubjectData.progress}
                  size={135}
                  strokeWidth={10}
                  label="Progress"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Progress Percentage
                </label>

                <div className="relative">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={editSubjectData.progress}
                    onChange={(event) =>
                      setEditSubjectData({
                        ...editSubjectData,
                        progress: Number(
                          event.target.value
                        ),
                      })
                    }
                    className="w-full rounded-xl border border-slate-200 px-4 py-3 pr-12 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  />

                  <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-semibold text-slate-400">
                    %
                  </span>
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-semibold text-slate-700">
                  Topics Completed
                </label>

                <input
                  type="number"
                  min="0"
                  max={selectedSubject.totalTopics}
                  value={
                    editSubjectData.topicsCompleted
                  }
                  onChange={(event) =>
                    setEditSubjectData({
                      ...editSubjectData,
                      topicsCompleted: Number(
                        event.target.value
                      ),
                    })
                  }
                  className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />

                <p className="mt-1.5 text-xs text-slate-400">
                  Maximum: {selectedSubject.totalTopics} topics
                </p>
              </div>
            </div>

            <div className="flex justify-end gap-3 border-t border-slate-200 px-6 py-5">
              <button
                onClick={() => {
                  setIsUpdatingSubject(false);
                  setSelectedSubject(null);
                }}
                className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
              >
                Cancel
              </button>

              <button
                onClick={handleSaveSubjectProgress}
                className="rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
              >
                Save Progress
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;