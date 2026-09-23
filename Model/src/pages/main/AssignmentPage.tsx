import React from "react";
import { Link } from "react-router-dom";

const MyProgress: React.FC = () => {
  const subjects = [
    {
      name: "Mathematics",
      progress: 75,
      lessons: 10,
      completed: 8,
    },
    {
      name: "Biology",
      progress: 45,
      lessons: 10,
      completed: 5,
    },
    {
      name: "Physics",
      progress: 60,
      lessons: 10,
      completed: 6,
    },
    {
      name: "Chemistry",
      progress: 52,
      lessons: 10,
      completed: 5,
    },
    {
      name: "English",
      progress: 80,
      lessons: 10,
      completed: 8,
    },
    {
      name: "Geography",
      progress: 35,
      lessons: 10,
      completed: 4,
    },
  ];

  const weeklyProgress = [
    { day: "Monday", value: 70 },
    { day: "Tuesday", value: 85 },
    { day: "Wednesday", value: 55 },
    { day: "Thursday", value: 90 },
    { day: "Friday", value: 65 },
    { day: "Saturday", value: 75 },
    { day: "Sunday", value: 40 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-gray-200 bg-white px-8 py-6">
        <h1 className="text-2xl font-bold text-black">
          My Progress
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Track your learning progress and performance
        </p>
      </header>

      {/* Main Content */}
      <div className="space-y-8 p-8">

        {/* Overview */}
        <section className="rounded-2xl bg-black p-8 text-white">

          <h2 className="text-2xl font-bold">
            Your Learning Progress
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-300">
            Keep learning and practicing to improve your performance
            across all your subjects.
          </p>

          <div className="mt-7">

            <div className="mb-2 flex items-center justify-between">
              <span className="text-sm text-gray-300">
                Overall Progress
              </span>

              <span className="text-lg font-bold">
                68%
              </span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-gray-700">
              <div
                className="h-full rounded-full bg-slate-300"
                style={{ width: "68%" }}
              />
            </div>

          </div>

        </section>

        {/* Statistics */}
        <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">

          <div className="rounded-2xl border border-gray-200 bg-white p-6">
            <p className="text-sm text-gray-500">
              Overall Progress
            </p>

            <h3 className="mt-2 text-3xl font-bold text-black">
              68%
            </h3>

            <p className="mt-2 text-xs text-black">
              Learning progress
            </p>
          </div>

          <div className="rounded-2xl border border-gray-200 bg-white p-6">
            <p className="text-sm text-gray-500">
              Lessons Completed
            </p>

            <h3 className="mt-2 text-3xl font-bold text-black">
              24
            </h3>

            <p className="mt-2 text-xs text-gray-500">
              Out of 60 lessons
            </p>
          </div>

          <div className="rounded-2xl border border-gray-200 bg-white p-6">
            <p className="text-sm text-gray-500">
              Learning Streak
            </p>

            <h3 className="mt-2 text-3xl font-bold text-black">
              7 Days
            </h3>

            <p className="mt-2 text-xs text-gray-500">
              Keep going
            </p>
          </div>

          <div className="rounded-2xl border border-gray-200 bg-white p-6">
            <p className="text-sm text-gray-500">
              Study Time
            </p>

            <h3 className="mt-2 text-3xl font-bold text-black">
              18h
            </h3>

            <p className="mt-2 text-xs text-gray-500">
              Total learning time
            </p>
          </div>

        </section>

        {/* Subject Progress */}
        <section className="rounded-2xl border border-gray-200 bg-white p-7">

          <div>
            <h2 className="text-xl font-bold text-black">
              Subject Progress
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              See how you are progressing in each subject.
            </p>
          </div>

          <div className="mt-6 space-y-6">

            {subjects.map((subject) => (
              <div key={subject.name}>

                <div className="mb-2 flex items-center justify-between">

                  <div>
                    <h3 className="text-sm font-semibold text-black">
                      {subject.name}
                    </h3>

                    <p className="mt-1 text-xs text-gray-500">
                      {subject.completed} of {subject.lessons} lessons
                      completed
                    </p>
                  </div>

                  <span className="text-sm font-bold text-black">
                    {subject.progress}%
                  </span>

                </div>

                <div className="h-3 overflow-hidden rounded-full bg-gray-200">
                  <div
                    className="h-full rounded-full bg-slate-300"
                    style={{
                      width: `${subject.progress}%`,
                    }}
                  />
                </div>

              </div>
            ))}

          </div>

        </section>

        {/* Learning Activity */}
        <section className="grid grid-cols-1 gap-6 lg:grid-cols-2">

          {/* Recent Activity */}
          <div className="rounded-2xl border border-gray-200 bg-white p-7">

            <h2 className="text-xl font-bold text-black">
              Recent Learning Activity
            </h2>

            <div className="mt-6 space-y-5">

              <div className="border-b border-gray-100 pb-5">
                <p className="text-sm font-semibold text-black">
                  Completed Algebra Lesson
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  Mathematics
                </p>

                <p className="mt-2 text-xs text-gray-400">
                  2 hours ago
                </p>
              </div>

              <div className="border-b border-gray-100 pb-5">
                <p className="text-sm font-semibold text-black">
                  Completed Science Quiz
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  Biology
                </p>

                <p className="mt-2 text-xs text-gray-400">
                  Yesterday
                </p>
              </div>

              <div>
                <p className="text-sm font-semibold text-black">
                  Completed Force and Motion Topic
                </p>

                <p className="mt-1 text-xs text-gray-500">
                  Physics
                </p>

                <p className="mt-2 text-xs text-gray-400">
                  2 days ago
                </p>
              </div>

            </div>

          </div>

          {/* Weekly Progress */}
          <div className="rounded-2xl border border-gray-200 bg-white p-7">

            <h2 className="text-xl font-bold text-black">
              Weekly Progress
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Your learning activity this week.
            </p>

            <div className="mt-7 space-y-5">

              {weeklyProgress.map((item) => (
                <div key={item.day}>

                  <div className="mb-2 flex justify-between">
                    <span className="text-xs font-medium text-gray-600">
                      {item.day}
                    </span>

                    <span className="text-xs text-gray-500">
                      {item.value}%
                    </span>
                  </div>

                  <div className="h-2 rounded-full bg-gray-200">
                    <div
                      className="h-full rounded-full bg-slate-300"
                      style={{
                        width: `${item.value}%`,
                      }}
                    />
                  </div>

                </div>
              ))}

            </div>

          </div>

        </section>

        {/* Improvement Section */}
        <section className="rounded-2xl border border-slate-300 bg-slate-300 p-7">

          <h2 className="text-xl font-bold text-black">
            Continue Improving
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-black">
            Focus on the subjects with lower progress and use the
            AI Tutor to get explanations and practice questions.
          </p>

          <Link
            to="/student/ai-tutor"
            className="mt-5 inline-block rounded-xl bg-black px-6 py-3 text-sm font-semibold text-white transition hover:bg-gray-800"
          >
            Practice with AI Tutor
          </Link>

        </section>

      </div>
    </div>
  );
};

export default MyProgress;

