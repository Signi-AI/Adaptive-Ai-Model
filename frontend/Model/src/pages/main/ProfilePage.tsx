import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

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

  // =========================
  // STUDENT INFORMATION
  // =========================

  const [student, setStudent] = useState<Student>({
    name: "Comfotha Mwansasule",
    level: "Secondary School",
    className: "Form 3",
    school: "Example Secondary School",
  });

  // =========================
  // PROFILE IMAGE
  // =========================

  const [profileImage, setProfileImage] = useState<string | null>(null);

  const handleProfileImage = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
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

    const imageUrl = URL.createObjectURL(file);

    setProfileImage(imageUrl);
  };

  // =========================
  // SUBJECTS
  // =========================

  const subjects: Subject[] = [
    {
      name: "Mathematics",
      progress: 72,
    },
    {
      name: "English",
      progress: 81,
    },
    {
      name: "Biology",
      progress: 70,
    },
    {
      name: "Chemistry",
      progress: 63,
    },
    {
      name: "Physics",
      progress: 52,
    },
  ];

  // =========================
  // EDIT PROFILE
  // =========================

  const [isEditing, setIsEditing] = useState(false);

  const [formData, setFormData] = useState<Student>(student);

  const handleEdit = () => {
    setFormData(student);
    setIsEditing(true);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSave = () => {
    setStudent(formData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  // =========================
  // START STUDYING
  // =========================

  const handleStudy = () => {
    navigate("/subjects/physics");
  };

  // =========================
  // UI
  // =========================

  return (
    <div className="min-h-screen bg-white px-4 py-8 text-black md:px-8">

      <div className="mx-auto max-w-6xl">

        {/* =====================================
            PAGE HEADER
        ====================================== */}

        <div className="mb-10 text-center">

          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-gray-500">
            Student Dashboard
          </p>

          <h1 className="text-3xl font-bold text-black md:text-4xl">
            My Profile
          </h1>

          <p className="mx-auto mt-2 max-w-xl text-gray-500">
            Manage your profile and track your learning progress.
          </p>

        </div>


        {/* =====================================
            STUDENT PROFILE
        ====================================== */}

        <div className="mb-8 rounded-3xl border border-gray-200 bg-gray-100 shadow-sm">

          <div className="px-6 py-10 md:px-8">

            {/* PROFILE CONTENT */}

            <div className="flex flex-col items-center">

              {/* =================================
                  PROFILE PICTURE
              ================================= */}

              <div className="relative">

                <div className="h-36 w-36 overflow-hidden rounded-full border-4 border-gray-200 bg-gray-100 shadow-md">

                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt="Student profile"
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center text-5xl font-bold text-gray-700">
                      {student.name.charAt(0).toUpperCase()}
                    </div>
                  )}

                </div>


                {/* CAMERA BUTTON */}

                <label
                  htmlFor="profile-picture"
                  className="absolute bottom-1 right-1 flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border-4 border-white bg-gray-200 text-lg shadow-md transition hover:bg-gray-300"
                  title="Change profile picture"
                >
                  📷
                </label>

                <input
                  id="profile-picture"
                  type="file"
                  accept="image/*"
                  onChange={handleProfileImage}
                  className="hidden"
                />

              </div>


              {/* PROFILE IMAGE MESSAGE */}

              <p className="mt-4 text-sm text-gray-500">
                Click the camera to change your profile picture
              </p>


              {/* =================================
                  STUDENT INFORMATION
              ================================= */}

              <div className="mt-7 w-full text-center">

                <p className="text-xs font-semibold uppercase tracking-widest text-gray-500">
                  Student Information
                </p>


                <h2 className="mt-3 text-3xl font-bold text-black">
                  {student.name}
                </h2>


                <p className="mt-2 text-lg text-gray-600">
                  {student.level}
                </p>


                {/* =================================
                    INFORMATION CARDS
                ================================= */}

                <div className="mx-auto mt-7 grid max-w-3xl grid-cols-1 gap-4 sm:grid-cols-3">

                  {/* CLASS */}

                  <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                    <p className="text-xs uppercase tracking-wider text-gray-500">
                      Class
                    </p>

                    <p className="mt-2 font-semibold text-black">
                      {student.className}
                    </p>

                  </div>


                  {/* SCHOOL */}

                  <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                    <p className="text-xs uppercase tracking-wider text-gray-500">
                      School
                    </p>

                    <p className="mt-2 font-semibold text-black">
                      {student.school}
                    </p>

                  </div>


                  {/* LEVEL */}

                  <div className="rounded-2xl border border-gray-200 bg-gray-50 p-5">

                    <p className="text-xs uppercase tracking-wider text-gray-500">
                      Level
                    </p>

                    <p className="mt-2 font-semibold text-black">
                      {student.level}
                    </p>

                  </div>

                </div>


                {/* EDIT PROFILE BUTTON */}

                <button
                  onClick={handleEdit}
                  className="mt-7 rounded-xl bg-black px-7 py-3 font-semibold text-white transition hover:bg-gray-800"
                >
                  ✏️ Edit Profile
                </button>

              </div>

            </div>

          </div>

        </div>


        {/* =====================================
            OVERALL PROGRESS
        ====================================== */}

        <div className="mb-8 rounded-3xl border border-gray-200 bg-white p-6 shadow-sm md:p-8">

          <div className="mb-6 flex flex-col justify-between gap-3 md:flex-row md:items-center">

            <div>

              <p className="text-sm font-medium text-gray-500">
                Learning Progress
              </p>

              <h2 className="text-2xl font-bold text-black">
                Overall Progress
              </h2>

            </div>

            <span className="text-3xl font-bold text-gray-600">
              68%
            </span>

          </div>


          {/* PROGRESS BAR */}

          <div className="h-4 overflow-hidden rounded-full bg-gray-200">

            <div
              className="h-full rounded-full bg-gray-400 transition-all duration-700"
              style={{
                width: "68%",
              }}
            />

          </div>


          <div className="mt-4 flex justify-between text-sm text-gray-500">

            <span>
              68% completed
            </span>

            <span>
              Keep going 🚀
            </span>

          </div>

        </div>


        {/* =====================================
            SUBJECT PROGRESS
        ====================================== */}

        <div className="mb-8 rounded-3xl border border-gray-200 bg-white p-6 shadow-sm md:p-8">

          <div className="mb-7">

            <p className="text-sm font-medium text-gray-500">
              Academic Performance
            </p>

            <h2 className="text-2xl font-bold text-black">
              Subject Progress
            </h2>

          </div>


          <div className="space-y-6">

            {subjects.map((subject) => (

              <div key={subject.name}>

                <div className="mb-2 flex items-center justify-between">

                  <span className="font-medium text-black">
                    {subject.name}
                  </span>

                  <span className="text-sm text-gray-500">
                    {subject.progress}%
                  </span>

                </div>


                <div className="h-3 overflow-hidden rounded-full bg-gray-200">

                  <div
                    className="h-full rounded-full bg-gray-400 transition-all duration-700"
                    style={{
                      width: `${subject.progress}%`,
                    }}
                  />

                </div>

              </div>

            ))}

          </div>

        </div>


        {/* =====================================
            AI RECOMMENDATION
        ====================================== */}

        <div className="mb-8 rounded-3xl border border-gray-200 bg-gray-50 p-6 shadow-sm md:p-8">

          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

            <div className="flex gap-4">

              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-black text-2xl text-white">
                🤖
              </div>


              <div>

                <p className="text-sm font-medium text-gray-500">
                  AI Learning Recommendation
                </p>

                <h2 className="mt-1 text-xl font-bold text-black">
                  Focus on Physics
                </h2>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-500">
                  Your Physics progress is currently lower than
                  your other subjects. We recommend reviewing the
                  current topic and completing a short practice
                  assignment.
                </p>

              </div>

            </div>


            <button
              onClick={handleStudy}
              className="whitespace-nowrap rounded-xl bg-black px-6 py-3 font-semibold text-white transition hover:bg-gray-800"
            >
              Start Studying →
            </button>

          </div>

        </div>


        {/* =====================================
            STATISTICS
        ====================================== */}

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

          {/* TOPICS COMPLETED */}

          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

            <div className="mb-4 text-3xl">
              📚
            </div>

            <p className="text-sm text-gray-500">
              Topics Completed
            </p>

            <h3 className="mt-1 text-3xl font-bold text-black">
              24
            </h3>

          </div>


          {/* ASSIGNMENTS */}

          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

            <div className="mb-4 text-3xl">
              📝
            </div>

            <p className="text-sm text-gray-500">
              Assignments
            </p>

            <h3 className="mt-1 text-3xl font-bold text-black">
              18
            </h3>

          </div>


          {/* AVERAGE SCORE */}

          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

            <div className="mb-4 text-3xl">
              🎯
            </div>

            <p className="text-sm text-gray-500">
              Average Score
            </p>

            <h3 className="mt-1 text-3xl font-bold text-black">
              76%
            </h3>

          </div>


          {/* STUDY STREAK */}

          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

            <div className="mb-4 text-3xl">
              🔥
            </div>

            <p className="text-sm text-gray-500">
              Study Streak
            </p>

            <h3 className="mt-1 text-3xl font-bold text-black">
              7 days
            </h3>

          </div>

        </div>

      </div>


      {/* =====================================
          EDIT PROFILE MODAL
      ====================================== */}

      {isEditing && (

        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4 backdrop-blur-sm">

          <div className="w-full max-w-lg rounded-3xl border border-gray-200 bg-white p-6 text-black shadow-2xl md:p-8">

            {/* MODAL HEADER */}

            <div className="mb-6 flex items-center justify-between">

              <div>

                <p className="text-sm text-gray-500">
                  Account
                </p>

                <h2 className="text-2xl font-bold">
                  Edit Profile
                </h2>

              </div>


              <button
                onClick={handleCancel}
                className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-500 transition hover:bg-gray-200"
              >
                ✕
              </button>

            </div>


            {/* FORM */}

            <div className="space-y-5">

              {/* NAME */}

              <div>

                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Full Name
                </label>

                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-black outline-none transition focus:border-black"
                />

              </div>


              {/* LEVEL */}

              <div>

                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Education Level
                </label>

                <input
                  type="text"
                  name="level"
                  value={formData.level}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-black outline-none transition focus:border-black"
                />

              </div>


              {/* CLASS */}

              <div>

                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Class
                </label>

                <input
                  type="text"
                  name="className"
                  value={formData.className}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-black outline-none transition focus:border-black"
                />

              </div>


              {/* SCHOOL */}

              <div>

                <label className="mb-2 block text-sm font-medium text-gray-700">
                  School
                </label>

                <input
                  type="text"
                  name="school"
                  value={formData.school}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-black outline-none transition focus:border-black"
                />

              </div>

            </div>


            {/* BUTTONS */}

            <div className="mt-8 flex gap-3">

              <button
                onClick={handleCancel}
                className="flex-1 rounded-xl border border-gray-300 bg-white px-5 py-3 font-semibold text-black transition hover:bg-gray-100"
              >
                Cancel
              </button>

              <button
                onClick={handleSave}
                className="flex-1 rounded-xl bg-black px-5 py-3 font-semibold text-white transition hover:bg-gray-800"
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