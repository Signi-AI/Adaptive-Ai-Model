import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Edit3,
  Camera,
  ArrowRight,
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
import heroBg from "../../assets/herobg.jpeg";
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

const Profile: React.FC = () => {
  const navigate = useNavigate();

  // =========================
  // STUDENT INFORMATION
  // =========================
  const [student, setStudent] = useState<Student>(() => {
    const saved = localStorage.getItem("student_profile_data");
    return saved
      ? JSON.parse(saved)
      : {
          name: "Comfotha Mwansasule",
          level: "Secondary School",
          className: "Form 3",
          school: "Example Secondary School",
        };
  });

  useEffect(() => {
    localStorage.setItem("student_profile_data", JSON.stringify(student));
  }, [student]);

  // =========================
  // PROFILE IMAGE
  // =========================
  const [profileImage, setProfileImage] = useState<string | null>(() => {
    return localStorage.getItem("student_profile_image") || null;
  });

  const handleProfileImage = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please select an image file.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("Image size should not exceed 5MB.");
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      setProfileImage(result);
      localStorage.setItem("student_profile_image", result);
    };
    reader.readAsDataURL(file);
  };

  // =========================
  // SUBJECTS & PROGRESS STATE
  // =========================
  const [subjects, setSubjects] = useState<Subject[]>(() => {
    const saved = localStorage.getItem("student_subjects_data");
    return saved ? JSON.parse(saved) : INITIAL_SUBJECTS;
  });

  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(
    null
  );
  const [isUpdatingSubject, setIsUpdatingSubject] = useState<boolean>(false);
  const [editSubjectData, setEditSubjectData] = useState<Subject | null>(null);

  useEffect(() => {
    localStorage.setItem("student_subjects_data", JSON.stringify(subjects));
  }, [subjects]);

  // Overall calculations
  const overallProgress = Math.round(
    subjects.reduce((acc, curr) => acc + curr.progress, 0) / subjects.length
  );

  const totalTopicsDone = subjects.reduce(
    (acc, curr) => acc + curr.topicsCompleted,
    0
  );

  // Lowest progress subject recommendation
  const lowestSubject = [...subjects].sort(
    (a, b) => a.progress - b.progress
  )[0];

  // Update subject progress handler
  const handleSaveSubjectProgress = () => {
    if (!editSubjectData) return;
    setSubjects((prev) =>
      prev.map((s) => (s.id === editSubjectData.id ? editSubjectData : s))
    );
    setIsUpdatingSubject(false);
  };

  // Status Badge Helper
  const getStatusBadge = (progress: number) => {
    if (progress >= 80) {
      return (
        <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-[10px] font-bold text-emerald-400 border border-emerald-500/20">
          <Award size={10} /> Mastered
        </span>
      );
    }
    if (progress >= 60) {
      return (
        <span className="inline-flex items-center gap-1 rounded-full bg-blue-500/10 px-2.5 py-0.5 text-[10px] font-bold text-blue-400 border border-blue-500/20">
          <TrendingUp size={10} /> On Track
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-amber-500/10 px-2.5 py-0.5 text-[10px] font-bold text-amber-400 border border-amber-500/20">
        <AlertCircle size={10} /> Needs Review
      </span>
    );
  };

  // =========================
  // EDIT PROFILE MODAL
  // =========================
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<Student>(student);

  const handleEdit = () => {
    setFormData(student);
    setIsEditing(true);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((previous) => ({ ...previous, [name]: value }));
  };

  const handleSave = () => {
    setStudent(formData);
    setIsEditing(false);
  };

  return (
    <div className="min-h-screen bg-white font-sans text-slate-100 antialiased">
      <div>
        <StudentSidebar />
      </div>
      <div className="ml-60">
        <div className="fixed inset-0 pointer-events-none overflow-hidden">
          <div className="absolute -left-40 -top-40 h-96 w-96 rounded-full bg-purple-600/15 blur-3xl" />
          <div className="absolute right-0 top-1/3 h-96 w-96 rounded-full bg-blue-600/10 blur-3xl" />
        </div>

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

export default Profile;