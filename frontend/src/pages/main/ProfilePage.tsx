import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Edit3,
  Camera,
  ArrowRight,
  X,
  School,
  GraduationCap,
  Bookmark,
  User,
} from "lucide-react";
import StudentSidebar from "./StudentSidebar";

interface Student {
  name: string;
  level: string;
  className: string;
  school: string;
}

const Profile: React.FC = () => {
  const navigate = useNavigate();

  const [student, setStudent] = useState<Student>(() => {
    try {
      const saved = localStorage.getItem("student_profile_data");

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
      school: "Example Secondary School",
    };
  });

  useEffect(() => {
    localStorage.setItem(
      "student_profile_data",
      JSON.stringify(student)
    );
  }, [student]);

  const [profileImage, setProfileImage] = useState<string | null>(() => {
    return localStorage.getItem("student_profile_image") || null;
  });

  const [isEditing, setIsEditing] = useState(false);

  const [formData, setFormData] =
    useState<Student>(student);

  const handleProfileImage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

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

  const handleEdit = () => {
    setFormData(student);
    setIsEditing(true);
  };

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSave = () => {
    setStudent(formData);
    setIsEditing(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 antialiased">
      <StudentSidebar />

      <div className="ml-60">
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
              onClick={() => navigate("/learn")}
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
                    onChange={handleProfileImage}
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
                  </div>

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
                      Make sure your student information is
                      correct and up to date.
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
                  onClick={() => setIsEditing(false)}
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
                  onClick={() => setIsEditing(false)}
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
    </div>
  );
};

export default Profile;