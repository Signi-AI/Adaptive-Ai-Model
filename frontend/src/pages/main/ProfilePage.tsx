import React, {
  useEffect,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router-dom";

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
} from "lucide-react";
<<<<<<< HEAD
import logo from "../../assets/logo.jpeg";
import heroBg from "../../assets/herobg.jpeg";
import StudentSidebar from "./StudentSidebar";
=======
>>>>>>> 6d22643 (student frontend development)

interface Student {
  name: string;
  level: string;
  className: string;
  school: string;
}

interface Subject {
  name: string;
  progress: number;
}

const Profile: React.FC = () => {
  const navigate = useNavigate();

<<<<<<< HEAD
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
=======
  const [student, setStudent] =
    useState<Student>(() => {
      try {
        const saved =
          localStorage.getItem(
            "student_profile_data"
          );

        if (saved) {
          return JSON.parse(saved);
        }
      } catch {
        // Ignore invalid localStorage data
      }

      return {
        name: "Comfotha Mwansasule",
        level: "Secondary School",
        className: "Form 3",
        school:
          "Example Secondary School",
      };
    });
>>>>>>> 6d22643 (student frontend development)

  // Save student profile data locally
  useEffect(() => {
    localStorage.setItem("student_profile_data", JSON.stringify(student));
  }, [student]);

<<<<<<< HEAD
  // =========================
  // PROFILE IMAGE
  // =========================
  const [profileImage, setProfileImage] = useState<string | null>(() => {
    return localStorage.getItem("student_profile_image") || null;
  });

  const handleProfileImage = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
=======
  const [profileImage, setProfileImage] =
    useState<string | null>(() => {
      return (
        localStorage.getItem(
          "student_profile_image"
        ) || null
      );
    });

  const [isEditing, setIsEditing] =
    useState(false);

  const [formData, setFormData] =
    useState<Student>(student);

  const handleProfileImage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file =
      event.target.files?.[0];

>>>>>>> 6d22643 (student frontend development)
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert(
        "Please select an image file."
      );
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert(
        "Image size should not exceed 5MB."
      );
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
<<<<<<< HEAD
      const result = reader.result as string;
=======
      const result =
        reader.result as string;

>>>>>>> 6d22643 (student frontend development)
      setProfileImage(result);

      localStorage.setItem(
        "student_profile_image",
        result
      );
    };
    reader.readAsDataURL(file);
  };

  // =========================
  // SUBJECTS
  // =========================
  const subjects: Subject[] = [
    { name: "Mathematics", progress: 72 },
    { name: "English", progress: 81 },
    { name: "Biology", progress: 70 },
    { name: "Chemistry", progress: 63 },
    { name: "Physics", progress: 52 },
  ];

  // Calculate overall average
  const overallProgress = Math.round(
    subjects.reduce((acc, curr) => acc + curr.progress, 0) / subjects.length
  );

  // =========================
  // EDIT PROFILE MODAL
  // =========================
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<Student>(student);

  const handleEdit = () => {
    setFormData(student);
    setIsEditing(true);
  };

<<<<<<< HEAD
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
=======
  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const {
      name,
      value,
    } = event.target;

    setFormData(
      (previous) => ({
        ...previous,
        [name]: value,
      })
    );
>>>>>>> 6d22643 (student frontend development)
  };

  const handleSave = () => {
    setStudent(formData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  // =========================
  // NAVIGATION
  // =========================
  const handleStudy = () => {
    navigate("/subjects/physics");
  };

  return (
<<<<<<< HEAD
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
          {/* TOP HEADER WITH BRAND LOGO */}
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

          {/* HERO BANNER CARD WITH ENHANCED STYLED HERO BG */}
          <div
            className="mb-8 overflow-hidden rounded-3xl border border-purple-500/30 p-6 md:p-8 relative shadow-2xl backdrop-blur-xl bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: `url(${heroBg})` }}
          >
            {/* OVERLAY TO MAINTAIN CONTRAST & READABILITY */}
            <div className="absolute inset-0 bg-slate-950/70 backdrop-blur-[2px]" />

            {/* AMBIENT HERO BACKGROUND ELEMENTS */}
            <div className="pointer-events-none absolute -top-24 -left-24 h-72 w-72 rounded-full bg-purple-600/20 blur-3xl" />
            <div className="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-indigo-600/20 blur-3xl" />

            {/* SUBTLE GRID OVERLAY */}
            <div
              className="pointer-events-none absolute inset-0 opacity-10"
              style={{
                backgroundImage: `radial-gradient(#a855f7 1px, transparent 1px)`,
                backgroundSize: "24px 24px",
              }}
            />

            <div className="relative z-10 flex flex-col items-center gap-6 md:flex-row md:items-start md:gap-8">
              {/* AVATAR UPLOAD CONTAINER */}
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

                {/* CAMERA BUTTON */}
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

                {/* DETAILS GRID CARDS */}
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

                {/* ACTION BUTTONS */}
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

          {/* OVERALL PROGRESS BANNER */}
          <div className="mb-8 rounded-3xl border border-slate-800 bg-slate-800/40 p-6 md:p-8 shadow-xl backdrop-blur-md">
            <div className="mb-4 flex flex-col justify-between gap-2 md:flex-row md:items-center">
              <div>
                <p className="text-xs font-bold uppercase tracking-wider text-purple-400">
                  Academic Progress
                </p>
                <h3 className="text-xl font-bold text-white">
                  Overall Performance
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
              <span>{overallProgress}% Curriculum Completed</span>
              <span className="text-purple-300 font-semibold">
                Keep learning 🚀
              </span>
            </div>
          </div>

          {/* SUBJECT PROGRESS SECTION */}
          <div className="mb-8 rounded-3xl border border-slate-800 bg-slate-800/40 p-6 md:p-8 shadow-xl backdrop-blur-md">
            <div className="mb-6">
              <p className="text-xs font-bold uppercase tracking-wider text-purple-400">
                Subject Mastery
              </p>
              <h3 className="text-xl font-bold text-white">
                Academic Breakdown
              </h3>
            </div>

            <div className="space-y-5">
              {subjects.map((subject) => (
                <div key={subject.name}>
                  <div className="mb-2 flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-200">
                      {subject.name}
                    </span>
                    <span className="font-bold text-slate-400">
                      {subject.progress}%
                    </span>
                  </div>

                  <div className="h-2.5 overflow-hidden rounded-full bg-slate-900 border border-slate-800">
                    <div
                      className="h-full rounded-full bg-purple-500 transition-all duration-700"
                      style={{ width: `${subject.progress}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI RECOMMENDATION CARD */}
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
                    <Sparkles size={12} /> AI Personalized Recommendation
                  </span>
                  <h3 className="mt-1 text-lg font-bold text-white">
                    Focus on Physics Concepts
                  </h3>
                  <p className="mt-1 max-w-xl text-xs leading-relaxed text-slate-300">
                    Your Physics progress is currently behind other subjects (52%).
                    Reviewing current topics with practice exercises will quickly
                    bring you back on track.
                  </p>
                </div>
              </div>

              <button
                onClick={handleStudy}
                className="whitespace-nowrap flex items-center justify-center gap-2 rounded-xl bg-purple-600 px-5 py-3 text-xs font-bold text-white shadow-lg shadow-purple-600/30 hover:bg-purple-500 transition-all active:scale-95"
              >
                <span>Start Physics Session</span>
                <ArrowRight size={15} />
              </button>
            </div>
          </div>

          {/* STATS CARDS GRID */}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
                <BookOpen size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">
                Topics Completed
              </p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">24</h4>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                <CheckCircle2 size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">
                Assignments Completed
              </p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">18</h4>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-800/40 p-5 shadow-lg">
              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400">
                <Target size={20} />
              </div>
              <p className="text-xs font-medium text-slate-400">Average Score</p>
              <h4 className="mt-1 text-2xl font-extrabold text-white">76%</h4>
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

        {/* EDIT PROFILE MODAL */}
        {isEditing && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-4 backdrop-blur-md">
            <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900 p-6 text-white shadow-2xl md:p-8 animate-in fade-in zoom-in-95 duration-150">
              {/* MODAL HEADER */}
              <div className="mb-6 flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-purple-400">
                    Account Settings
                  </p>
                  <h3 className="text-xl font-bold text-white">Edit Profile</h3>
                </div>

                <button
                  onClick={handleCancel}
                  className="flex h-8 w-8 items-center justify-center rounded-xl border border-slate-800 bg-slate-800/50 text-slate-400 hover:text-white transition-all"
                >
                  <X size={18} />
                </button>
              </div>

              {/* FORM */}
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
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
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
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
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
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
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
                    className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-2.5 text-xs text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                  />
=======
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 antialiased">

      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 px-8 py-4 backdrop-blur-xl">
        <div className="mx-auto flex max-w-5xl items-center justify-between">

          <div>
            <h1 className="text-lg font-extrabold text-slate-800">
              My Profile
            </h1>

            <p className="text-xs text-slate-400">
              Student Account
            </p>
          </div>

          <button
            onClick={() =>
              navigate("/tutorhome")
            }
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-semibold text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600"
          >
            Back to Learning
            <ArrowRight size={15} />
          </button>

        </div>
      </header>

      {/* Main */}
      <main className="mx-auto max-w-5xl p-6 md:p-8">

        <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">

          {/* Profile Section */}
          <div className="px-6 py-10 md:px-10">

            <div className="flex flex-col items-center text-center">

              {/* Profile Picture */}
              <div className="relative">

                <div className="flex h-36 w-36 items-center justify-center overflow-hidden rounded-full border-4 border-white bg-slate-100 shadow-lg ring-1 ring-slate-200">

                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt="Student profile"
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center bg-blue-600 text-5xl font-extrabold text-white">
                      {student.name
                        .charAt(0)
                        .toUpperCase()}
                    </div>
                  )}

                </div>

                {/* Camera Button */}
                <label
                  htmlFor="profile-picture"
                  className="absolute bottom-1 right-1 flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border-4 border-white bg-blue-600 text-white shadow-md transition hover:bg-blue-700 active:scale-95"
                  title="Change profile picture"
                >
                  <Camera size={18} />
                </label>

                <input
                  id="profile-picture"
                  type="file"
                  accept="image/*"
                  onChange={
                    handleProfileImage
                  }
                  className="hidden"
                />

              </div>

              {/* Name */}
              <div className="mt-6">

                <h2 className="text-3xl font-extrabold tracking-tight text-slate-800">
                  {student.name}
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                  {student.level}
                </p>

              </div>

              {/* Edit Button */}
              <button
                onClick={handleEdit}
                className="mt-5 inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 active:scale-[0.98]"
              >
                <Edit3 size={16} />
                Edit Profile
              </button>

            </div>

            {/* Personal Information */}
            <div className="mt-12">

              <div className="mb-5">

                <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                  Personal Information
                </p>

                <h3 className="mt-1 text-xl font-bold text-slate-800">
                  Student Details
                </h3>

              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">

                {/* Class */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5 transition hover:border-blue-200 hover:bg-blue-50/40">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                    <Bookmark size={21} />
                  </div>

                  <div className="min-w-0">

                    <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      Class
                    </p>

                    <p className="mt-1 text-base font-bold text-slate-800">
                      {student.className}
                    </p>

                  </div>

                </div>

                {/* School */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5 transition hover:border-blue-200 hover:bg-blue-50/40">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-slate-200 text-slate-700">
                    <School size={21} />
                  </div>

                  <div className="min-w-0">

                    <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      School
                    </p>

                    <p className="mt-1 truncate text-base font-bold text-slate-800">
                      {student.school}
                    </p>

                  </div>

>>>>>>> 6d22643 (student frontend development)
                </div>

<<<<<<< HEAD
              {/* MODAL ACTIONS */}
              <div className="mt-6 flex gap-3">
                <button
                  onClick={handleCancel}
                  className="flex-1 rounded-xl border border-slate-800 bg-slate-800/50 py-2.5 text-xs font-semibold text-slate-300 hover:bg-slate-800 transition-all"
                >
                  Cancel
                </button>

                <button
                  onClick={handleSave}
                  className="flex-1 rounded-xl bg-purple-600 py-2.5 text-xs font-semibold text-white shadow-md shadow-purple-600/20 hover:bg-purple-500 transition-all"
                >
                  Save Changes
                </button>
=======
                {/* Education Level */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5 transition hover:border-blue-200 hover:bg-blue-50/40">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-green-50 text-green-600">
                    <GraduationCap size={21} />
                  </div>

                  <div className="min-w-0">

                    <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      Education Level
                    </p>

                    <p className="mt-1 text-base font-bold text-slate-800">
                      {student.level}
                    </p>

                  </div>

                </div>

                {/* Account Type */}
                <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5 transition hover:border-blue-200 hover:bg-blue-50/40">

                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
                    <User size={21} />
                  </div>

                  <div className="min-w-0">

                    <p className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                      Account Type
                    </p>

                    <p className="mt-1 text-base font-bold text-slate-800">
                      Student
                    </p>

                  </div>

                </div>

>>>>>>> 6d22643 (student frontend development)
              </div>
            </div>

            {/* Update Profile */}
            <div className="mt-8 rounded-2xl border border-blue-100 bg-blue-50 p-5">

              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                <div>

                  <p className="text-sm font-bold text-slate-800">
                    Keep your profile updated
                  </p>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    Make sure your student
                    information is correct and
                    up to date.
                  </p>

                </div>

                <button
                  onClick={handleEdit}
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-xs font-semibold text-blue-600 shadow-sm ring-1 ring-blue-100 transition hover:bg-blue-600 hover:text-white"
                >
                  <Edit3 size={14} />
                  Update Details
                </button>

              </div>

            </div>

          </div>
        </div>
      </main>

      {/* Edit Profile Modal */}
      {isEditing && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 px-4 py-6 backdrop-blur-sm">

          <div className="w-full max-w-md overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">

            {/* Modal Header */}
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">

              <div>

                <p className="text-xs font-bold uppercase tracking-wider text-blue-600">
                  Account Settings
                </p>

                <h3 className="mt-1 text-xl font-bold text-slate-800">
                  Edit Profile
                </h3>

              </div>

              <button
                onClick={() =>
                  setIsEditing(false)
                }
                className="flex h-9 w-9 items-center justify-center rounded-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
              >
                <X size={18} />
              </button>

            </div>

            {/* Modal Body */}
            <div className="space-y-5 p-6">

              {/* Profile Image */}
              <div className="flex justify-center">

                <div className="flex h-20 w-20 items-center justify-center overflow-hidden rounded-full bg-blue-50 text-blue-600 ring-1 ring-slate-200">

                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt="Profile"
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <User size={30} />
                  )}

                </div>

              </div>

              {/* Full Name */}
              <div>

                <label className="mb-2 block text-xs font-semibold text-slate-600">
                  Full Name
                </label>

                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                />

              </div>

              {/* Education Level */}
              <div>

                <label className="mb-2 block text-xs font-semibold text-slate-600">
                  Education Level
                </label>

                <input
                  type="text"
                  name="level"
                  value={formData.level}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                />

              </div>

              {/* Class */}
              <div>

                <label className="mb-2 block text-xs font-semibold text-slate-600">
                  Class
                </label>

                <input
                  type="text"
                  name="className"
                  value={formData.className}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                />

              </div>

              {/* School */}
              <div>

                <label className="mb-2 block text-xs font-semibold text-slate-600">
                  School
                </label>

                <input
                  type="text"
                  name="school"
                  value={formData.school}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
                />

              </div>

            </div>

            {/* Modal Footer */}
            <div className="flex gap-3 border-t border-slate-200 bg-slate-50 px-6 py-4">

              <button
                onClick={() =>
                  setIsEditing(false)
                }
                className="flex-1 rounded-xl border border-slate-200 bg-white py-3 text-sm font-semibold text-slate-600 transition hover:bg-slate-100"
              >
                Cancel
              </button>

              <button
                onClick={handleSave}
                className="flex-1 rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
              >
                Save Changes
              </button>

            </div>

          </div>
        </div>
      )}

    </div>
  );
};

export default Profile;