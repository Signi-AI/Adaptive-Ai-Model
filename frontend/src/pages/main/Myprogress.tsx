import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Edit3,
  Flame,
  Menu,
  Sparkles,
  Target,
  TrendingUp,
  X,
  CheckCircle2,
  Flame,
  Target,
  Sparkles,
  School,
  GraduationCap,
  Bookmark,
  TrendingUp,
  Award,
  AlertCircle,
} from "lucide-react";

import logo from "../../assets/logo.jpeg";
import { useStudentLayout } from "./Studentlayout";

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
  color: string;
}

const INITIAL_SUBJECTS: Subject[] = [
  {
    id: "math",
    name: "Mathematics",
    progress: 72,
    category: "Mathematics",
    topicsCompleted: 18,
    totalTopics: 25,
    color: "from-blue-500 to-indigo-600",
  },
  {
    id: "english",
    name: "English",
    progress: 81,
    category: "Languages",
    topicsCompleted: 21,
    totalTopics: 26,
    color: "from-emerald-500 to-teal-600",
  },
  {
    id: "biology",
    name: "Biology",
    progress: 70,
    category: "Science",
    topicsCompleted: 14,
    totalTopics: 20,
    color: "from-green-500 to-emerald-600",
  },
  {
    id: "chemistry",
    name: "Chemistry",
    progress: 63,
    category: "Science",
    topicsCompleted: 12,
    totalTopics: 19,
    color: "from-amber-500 to-orange-600",
  },
  {
    id: "physics",
    name: "Physics",
    progress: 52,
    category: "Science",
    topicsCompleted: 11,
    totalTopics: 21,
    color: "from-purple-500 to-violet-600",
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
    circumference -
    (safeValue / 100) * circumference;

  return (
    <div
      className="relative flex items-center justify-center"
      style={{
        width: size,
        height: size,
      }}
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

        <div className="relative mx-auto max-w-6xl px-4 py-8 md:px-8">
          {/* HEADER */}
          <header className="mb-8 flex items-center justify-between border-b border-slate-800 pb-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl ring-2 ring-purple-500/30 shadow-lg shadow-purple-500/10">
                <img
                  src={logo}
                  alt="Brand Logo"
                  className="h-full w-full object-cover"
                />
              </div>
              <div>
                <h1 className="text-base font-extrabold tracking-tight text-white">
                  LearnAI Studio
                </h1>
                <p className="text-[11px] font-medium text-slate-400">
                  Student Portal & Analytics
                </p>
              </div>
            </div>

            <button
              onClick={() => navigate("/")}
              className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-800/60 px-4 py-2 text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition-all"
            >
              Back to Chat
            </button>
          </header>

          {/* HERO BANNER CARD WITH BG IMAGE */}
          <div
            className="mb-8 overflow-hidden rounded-3xl border border-purple-500/30 p-6 md:p-8 relative shadow-2xl backdrop-blur-xl bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: `url(${heroBg})` }}
          >
            <div className="absolute inset-0 bg-slate-950/70 backdrop-blur-[2px]" />
            <div className="pointer-events-none absolute -top-24 -left-24 h-72 w-72 rounded-full bg-purple-600/20 blur-3xl" />
            <div className="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-indigo-600/20 blur-3xl" />

            <div className="relative z-10 flex flex-col items-center gap-6 md:flex-row md:items-start md:gap-8">
              {/* AVATAR */}
              <div className="relative shrink-0">
                <div className="h-32 w-32 md:h-36 md:w-36 overflow-hidden rounded-2xl border-2 border-purple-500/40 bg-slate-800 shadow-2xl ring-4 ring-purple-500/20">
                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt="Student profile"
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center bg-gradient-to-br from-purple-600 to-indigo-700 text-4xl font-extrabold text-white">
                      {student.name.charAt(0).toUpperCase()}
                    </div>
                  )}
                </div>

                <label
                  htmlFor="profile-picture"
                  className="absolute -bottom-2 -right-2 flex h-10 w-10 cursor-pointer items-center justify-center rounded-xl border border-slate-700 bg-slate-900 text-purple-400 shadow-lg hover:bg-purple-600 hover:text-white transition-all active:scale-95"
                  title="Change profile picture"
                >
                  <Camera size={18} />
                </label>

                <input
                  id="profile-picture"
                  type="file"
                  accept="image/*"
                  onChange={handleProfileImage}
                  className="hidden"
                />
              </div>

              {/* MAIN INFO SECTION */}
              <div className="flex-1 text-center md:text-left">
                <div className="inline-flex items-center gap-1.5 rounded-full border border-purple-500/30 bg-purple-500/10 px-3 py-1 text-xs font-semibold text-purple-300 mb-3 backdrop-blur-md">
                  <Sparkles size={13} />
                  <span>Active Student Account</span>
                </div>

                <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
                  {student.name}
                </h2>

                <p className="mt-1 text-sm font-medium text-slate-400">
                  {student.level}
                </p>

                <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
                  <div className="flex items-center gap-3 rounded-2xl border border-purple-500/20 bg-slate-900/80 p-3.5 backdrop-blur-sm">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
                      <Bookmark size={18} />
                    </div>
                    <div className="text-left">
                      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Class
                      </p>
                      <p className="text-xs font-bold text-slate-200">
                        {student.className}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 rounded-2xl border border-purple-500/20 bg-slate-900/80 p-3.5 backdrop-blur-sm">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                      <School size={18} />
                    </div>
                    <div className="text-left">
                      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        School
                      </p>
                      <p className="text-xs font-bold text-slate-200 truncate max-w-[120px]">
                        {student.school}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 rounded-2xl border border-purple-500/20 bg-slate-900/80 p-3.5 backdrop-blur-sm">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400">
                      <GraduationCap size={18} />
                    </div>
                    <div className="text-left">
                      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                        Level
                      </p>
                      <p className="text-xs font-bold text-slate-200">
                        {student.level}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex flex-wrap items-center justify-center md:justify-start gap-3">
                  <button
                    onClick={handleEdit}
                    className="inline-flex items-center gap-2 rounded-xl bg-purple-600 px-5 py-2.5 text-xs font-semibold text-white shadow-lg shadow-purple-600/30 hover:bg-purple-500 transition-all active:scale-95"
                  >
                    <Edit3 size={15} />
                    <span>Edit Profile</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* OVERALL PERFORMANCE */}
          <div className="mb-8 rounded-3xl border border-slate-800 bg-slate-800/40 p-6 md:p-8 shadow-xl backdrop-blur-md">
            <div className="mb-4 flex flex-col justify-between gap-2 md:flex-row md:items-center">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-purple-400">
                  Academic Progress
                </p>
                <h3 className="text-xl font-bold text-white">
                  Overall Curriculum Progress
                </h3>
              </div>
              <span className="text-3xl font-extrabold text-purple-400">
                {overallProgress}%
              </span>
            </div>

            <div className="h-3.5 overflow-hidden rounded-full bg-slate-900 border border-slate-800 p-0.5">
              <div
                className="h-full rounded-full bg-gradient-to-r from-purple-600 to-indigo-500 transition-all duration-700 shadow-md shadow-purple-500/30"
                style={{ width: `${overallProgress}%` }}
              />
            </div>

            <div className="mt-3 flex justify-between text-xs font-medium text-slate-400">
              <span>{overallProgress}% Completed Across All Subjects</span>
              <span className="text-purple-300 font-semibold">
                Keep pushing forward 🚀
              </span>
            </div>
          </div>

          {/* DYNAMIC SUBJECT MASTERY BREAKDOWN */}
          <div className="mb-8 rounded-3xl border border-slate-800 bg-slate-800/40 p-6 md:p-8 shadow-xl backdrop-blur-md">
            <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-purple-400">
                  Detailed Subject Mastery
                </p>
                <h3 className="text-xl font-bold text-white">
                  Interactive Subject Breakdown
                </h3>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {subjects.map((subj) => (
                <div
                  key={subj.id}
                  onClick={() => setSelectedSubject(subj)}
                  className={`group relative cursor-pointer rounded-2xl border p-5 transition-all hover:border-purple-500/50 hover:bg-slate-800/80 ${
                    selectedSubject?.id === subj.id
                      ? "border-purple-500 bg-purple-950/20 shadow-lg shadow-purple-500/10"
                      : "border-slate-800 bg-slate-900/60"
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="text-sm font-bold text-white">
                          {subj.name}
                        </h4>
                        {getStatusBadge(subj.progress)}
                      </div>
                      <p className="mt-0.5 text-[11px] text-slate-400">
                        {subj.category} • {subj.topicsCompleted}/{subj.totalTopics} Topics Completed
                      </p>
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setEditSubjectData(subj);
                        setIsUpdatingSubject(true);
                      }}
                      className="opacity-0 group-hover:opacity-100 p-1.5 text-slate-400 hover:text-purple-400 rounded-lg hover:bg-slate-800 transition-all"
                      title="Update score"
                    >
                      <Edit3 size={14} />
                    </button>
                  </div>

                  {/* PROGRESS BAR */}
                  <div className="mt-4">
                    <div className="mb-1 flex justify-between text-[11px]">
                      <span className="text-slate-400 font-medium">Progress</span>
                      <span className="font-extrabold text-white">{subj.progress}%</span>
                    </div>
                    <div className="h-2 overflow-hidden rounded-full bg-slate-950">
                      <div
                        className={`h-full bg-gradient-to-r ${subj.color} transition-all duration-700`}
                        style={{ width: `${subj.progress}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* DYNAMIC AI RECOMMENDATION CARD */}
          {lowestSubject && (
            <div className="mb-8 rounded-3xl border border-purple-500/20 bg-gradient-to-r from-purple-900/30 to-indigo-900/20 p-6 md:p-8 shadow-xl relative overflow-hidden">
              <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center overflow-hidden rounded-2xl bg-white/10 ring-1 ring-white/20">
                    <img
                      src={logo}
                      alt="AI Tutor"
                      className="h-full w-full object-cover"
                    />
                  </div>

                  <div>
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold uppercase tracking-wider text-purple-300">
                      <Sparkles size={12} /> AI Recommended Target
                    </span>
                    <h3 className="mt-1 text-lg font-bold text-white">
                      Focus on {lowestSubject.name} Concepts
                    </h3>
                    <p className="mt-1 max-w-xl text-xs leading-relaxed text-slate-300">
                      Your {lowestSubject.name} score is currently your lowest at {lowestSubject.progress}%. Completing remaining topics will significantly boost your overall score.
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => navigate(`/subjects/${lowestSubject.id}`)}
                  className="whitespace-nowrap flex items-center justify-center gap-2 rounded-xl bg-purple-600 px-5 py-3 text-xs font-bold text-white shadow-lg shadow-purple-600/30 hover:bg-purple-500 transition-all active:scale-95"
                >
                  <span>Start {lowestSubject.name} Session</span>
                  <ArrowRight size={15} />
                </button>
              </div>
            </div>
          )}

          {/* STATS CARDS GRID */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
                <BookOpen size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">
                Topics Completed
              </p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">
                {totalTopicsDone}
              </h4>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                <CheckCircle2 size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">
                Assignments Done
              </p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">18</h4>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400">
                <Target size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">Overall Average</p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">
                {overallProgress}%
              </h4>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400">
                <Flame size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">Study Streak</p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">
                7 Days
              </h4>
            </div>
          </div>
        </div>

        {/* UPDATE SUBJECT PROGRESS MODAL */}
        {isUpdatingSubject && editSubjectData && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-4 backdrop-blur-md">
            <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900 p-6 text-white shadow-2xl">
              <div className="mb-6 flex items-center justify-between border-b border-slate-800 pb-4">
                <h3 className="text-lg font-bold">
                  Update {editSubjectData.name}
                </h3>
                <button
                  onClick={() => setIsUpdatingSubject(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <X size={18} />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="mb-1 block text-xs font-semibold text-slate-300">
                    Progress Percentage (%)
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={editSubjectData.progress}
                    onChange={(e) =>
                      setEditSubjectData({
                        ...editSubjectData,
                        progress: Math.min(100, Math.max(0, Number(e.target.value))),
                      })
                    }
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none focus:border-purple-500"
                  />
                </div>

                <div>
                  <label className="mb-1 block text-xs font-semibold text-slate-300">
                    Topics Completed
                  </label>
                  <input
                    type="number"
                    min="0"
                    max={editSubjectData.totalTopics}
                    value={editSubjectData.topicsCompleted}
                    onChange={(e) =>
                      setEditSubjectData({
                        ...editSubjectData,
                        topicsCompleted: Number(e.target.value),
                      })
                    }
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div className="mt-6 flex gap-3">
                <button
                  onClick={() => setIsUpdatingSubject(false)}
                  className="flex-1 rounded-xl border border-slate-800 bg-slate-800/50 py-2.5 text-xs font-semibold text-slate-300"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSaveSubjectProgress}
                  className="flex-1 rounded-xl bg-purple-600 py-2.5 text-xs font-semibold text-white shadow-md hover:bg-purple-500"
                >
                  Save Progress
                </button>
              </div>
            </div>
          </div>
        )}

        {/* EDIT PROFILE MODAL */}
        {isEditing && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-4 backdrop-blur-md">
            <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900 p-6 text-white shadow-2xl md:p-8">
              <div className="mb-6 flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-purple-400">
                    Account Settings
                  </p>
                  <h3 className="text-xl font-bold text-white">Edit Profile</h3>
                </div>
                <button
                  onClick={() => setIsEditing(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <X size={18} />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="mb-1.5 block text-xs font-semibold text-slate-300">
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none focus:border-purple-500"
                  />
                </div>
                <div>
                  <label className="mb-1.5 block text-xs font-semibold text-slate-300">
                    Education Level
                  </label>
                  <input
                    type="text"
                    name="level"
                    value={formData.level}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none focus:border-purple-500"
                  />
                </div>
                <div>
                  <label className="mb-1.5 block text-xs font-semibold text-slate-300">
                    Class
                  </label>
                  <input
                    type="text"
                    name="className"
                    value={formData.className}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none focus:border-purple-500"
                  />
                </div>
                <div>
                  <label className="mb-1.5 block text-xs font-semibold text-slate-300">
                    School
                  </label>
                  <input
                    type="text"
                    name="school"
                    value={formData.school}
                    onChange={handleChange}
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none focus:border-purple-500"
                  />
                </div>
              </div>

              <div className="mt-6 flex gap-3">
                <button
                  onClick={() => setIsEditing(false)}
                  className="flex-1 rounded-xl border border-slate-800 bg-slate-800/50 py-2.5 text-xs font-semibold text-slate-300 hover:bg-slate-800"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  className="flex-1 rounded-xl bg-purple-600 py-2.5 text-xs font-semibold text-white shadow-md hover:bg-purple-500"
                >
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const Profile: React.FC = () => {
  const navigate = useNavigate();

  const { openMenu } = useStudentLayout();

  const [student] = useState<Student>(() => {
    try {
      const saved = localStorage.getItem(
        "student_profile_data"
      );

      return saved
        ? JSON.parse(saved)
        : INITIAL_STUDENT;
    } catch {
      return INITIAL_STUDENT;
    }
  });

  const [profileImage] = useState<string>(() => {
    try {
      return (
        localStorage.getItem(
          "student_profile_image"
        ) || ""
      );
    } catch {
      return "";
    }
  });

  const [subjects, setSubjects] =
    useState<Subject[]>(() => {
      try {
        const saved =
          localStorage.getItem(
            "student_subjects_data"
          );

        return saved
          ? JSON.parse(saved)
          : INITIAL_SUBJECTS;
      } catch {
        return INITIAL_SUBJECTS;
      }
    });

  const [selectedSubject, setSelectedSubject] =
    useState<Subject | null>(null);

  const [isUpdatingSubject, setIsUpdatingSubject] =
    useState(false);

  const [editSubjectData, setEditSubjectData] =
    useState({
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
      (sum, subject) =>
        sum + subject.progress,
      0
    );

    return Math.round(
      total / subjects.length
    );
  }, [subjects]);

  const totalTopicsDone = useMemo(() => {
    return subjects.reduce(
      (sum, subject) =>
        sum + subject.topicsCompleted,
      0
    );
  }, [subjects]);

  const totalTopics = useMemo(() => {
    return subjects.reduce(
      (sum, subject) =>
        sum + subject.totalTopics,
      0
    );
  }, [subjects]);

  const lowestSubject = useMemo(() => {
    if (!subjects.length) return null;

    return subjects.reduce(
      (lowest, subject) =>
        subject.progress <
        lowest.progress
          ? subject
          : lowest
    );
  }, [subjects]);

  const getStatusBadge = (
    progress: number
  ) => {
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

  const handleOpenSubjectEdit = (
    subject: Subject
  ) => {
    setSelectedSubject(subject);

    setEditSubjectData({
      progress: subject.progress,
      topicsCompleted:
        subject.topicsCompleted,
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
        Number(
          editSubjectData.topicsCompleted
        ) || 0
      )
    );

    setSubjects((currentSubjects) =>
      currentSubjects.map((subject) =>
        subject.id ===
        selectedSubject.id
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

  const closeEditModal = () => {
    setIsUpdatingSubject(false);
    setSelectedSubject(null);
  };

  return (
    <div className="min-h-full bg-slate-50">
      <main className="min-h-full">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">

          {/* Header */}
          <div className="mb-8 flex items-start justify-between gap-4">
            <div className="flex items-start gap-3">
              {/* Mobile Menu */}
              <button
                type="button"
                onClick={openMenu}
                className="mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 shadow-sm transition hover:bg-slate-50 md:hidden"
                aria-label="Open menu"
              >
                <Menu size={20} />
              </button>

              <div>
                <p className="mb-1 text-sm font-medium text-blue-600">
                  Student Learning
                </p>

                <h1 className="text-2xl font-bold text-slate-800 sm:text-3xl">
                  My Progress
                </h1>

                <p className="mt-1 text-sm text-slate-500">
                  Track your learning progress
                  and academic performance.
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={() =>
                navigate("/tutorhome")
              }
              className="hidden shrink-0 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 sm:inline-flex"
            >
              Back to Learning
              <ArrowRight size={17} />
            </button>
          </div>

          {/* Mobile Back Button */}
          <button
            type="button"
            onClick={() =>
              navigate("/tutorhome")
            }
            className="mb-6 inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 sm:hidden"
          >
            Back to Learning
            <ArrowRight size={17} />
          </button>

          {/* Student Name + Profile Picture + Overall Progress */}
          <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
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
              <h2 className="mt-4 text-center text-2xl font-bold text-slate-800">
                {student.name}
              </h2>

              <p className="mt-1 text-center text-sm text-slate-500">
                {student.className} •{" "}
                {student.level}
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

                <p className="mt-4 text-center text-sm font-semibold text-slate-700">
                  {overallProgress >= 80
                    ? "Excellent progress!"
                    : overallProgress >= 60
                    ? "You're on the right track!"
                    : "Keep working consistently!"}
                </p>

                <p className="mt-1 text-center text-xs text-slate-500">
                  {totalTopicsDone} of{" "}
                  {totalTopics} topics
                  completed
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
                Monitor your progress in each
                subject.
              </p>
            </div>

            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {subjects.map((subject) => {
                const status =
                  getStatusBadge(
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
                            <BookOpen
                              size={17}
                            />
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
                        type="button"
                        onClick={() =>
                          handleOpenSubjectEdit(
                            subject
                          )
                        }
                        className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-blue-600"
                        title="Edit progress"
                      >
                        <Edit3 size={16} />
                      </button>
                    </div>

                    <div className="mt-6 flex justify-center">
                      <CircularProgress
                        value={
                          subject.progress
                        }
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
                          {
                            subject.topicsCompleted
                          }{" "}
                          /{" "}
                          {
                            subject.totalTopics
                          }
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
            <section className="mb-8 rounded-2xl border border-blue-100 bg-blue-50 p-5 sm:p-6">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-white text-blue-600 shadow-sm">
                    <Sparkles size={22} />
                  </div>

                  <div>
                    <p className="text-xs font-bold uppercase tracking-wide text-blue-600">
                      AI Learning
                      Recommendation
                    </p>

                    <h3 className="mt-1 text-lg font-bold text-slate-800">
                      Focus more on{" "}
                      {lowestSubject.name}
                    </h3>

                    <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-600">
                      Your current progress in{" "}
                      {lowestSubject.name} is{" "}
                      <strong>
                        {
                          lowestSubject.progress
                        }
                        %
                      </strong>
                      . Spend more time
                      reviewing this subject
                      to improve your overall
                      performance.
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() =>
                    navigate("/tutorhome")
                  }
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
              Your learning progress is saved
              automatically.
            </p>
          </div>
        </div>
      </main>

      {/* Edit Progress Modal */}
      {isUpdatingSubject &&
        selectedSubject && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4 backdrop-blur-sm">
            <div className="w-full max-w-md rounded-2xl bg-white shadow-2xl">

              <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
                <div>
                  <h2 className="text-lg font-bold text-slate-800">
                    Update Progress
                  </h2>

                  <p className="mt-1 text-xs text-slate-500">
                    {
                      selectedSubject.name
                    }
                  </p>
                </div>

                <button
                  type="button"
                  onClick={closeEditModal}
                  className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
                >
                  <X size={20} />
                </button>
              </div>

              <div className="space-y-5 p-6">
                <div className="flex justify-center">
                  <CircularProgress
                    value={
                      editSubjectData.progress
                    }
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
                      value={
                        editSubjectData.progress
                      }
                      onChange={(event) =>
                        setEditSubjectData({
                          ...editSubjectData,
                          progress:
                            Number(
                              event.target
                                .value
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
                    max={
                      selectedSubject.totalTopics
                    }
                    value={
                      editSubjectData.topicsCompleted
                    }
                    onChange={(event) =>
                      setEditSubjectData({
                        ...editSubjectData,
                        topicsCompleted:
                          Number(
                            event.target
                              .value
                          ),
                      })
                    }
                    className="w-full rounded-xl border border-slate-200 px-4 py-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                  />

                  <p className="mt-1.5 text-xs text-slate-400">
                    Maximum:{" "}
                    {
                      selectedSubject.totalTopics
                    }{" "}
                    topics
                  </p>
                </div>
              </div>

              <div className="flex justify-end gap-3 border-t border-slate-200 px-6 py-5">
                <button
                  type="button"
                  onClick={closeEditModal}
                  className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={
                    handleSaveSubjectProgress
                  }
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