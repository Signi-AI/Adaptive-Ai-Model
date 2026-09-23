import React from "react";
import { Link } from "react-router-dom";

const MySubjects: React.FC = () => {
  const subjects = [
    {
      name: "Mathematics",
      description: "Algebra, geometry, numbers and equations",
      progress: 75,
      topic: "Introduction to Equations",
    },
    {
      name: "Biology",
      description: "Living things, cells and human body systems",
      progress: 45,
      topic: "Human Body Systems",
    },
    {
      name: "Physics",
      description: "Force, motion, energy and measurements",
      progress: 60,
      topic: "Force and Motion",
    },
    {
      name: "Chemistry",
      description: "Matter, elements and chemical reactions",
      progress: 52,
      topic: "Elements and Compounds",
    },
    {
      name: "English",
      description: "Grammar, comprehension, writing and vocabulary",
      progress: 80,
      topic: "Grammar and Sentence Structure",
    },
    {
      name: "Geography",
      description: "Environment, maps, climate and physical features",
      progress: 35,
      topic: "Map Reading",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-gray-200 bg-white px-8 py-6">
        <h1 className="text-2xl font-bold text-gray-900">
          My Subjects
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          View your subjects and continue your learning
        </p>
      </header>

      {/* Main Content */}
      <div className="space-y-8 p-8">

        {/* Summary */}
        <section className="rounded-2xl bg-slate-400 p-8 text-white">

          <h2 className="text-2xl font-bold">
            Your Learning Subjects
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-gray-300">
            You are currently studying 6 subjects. Continue your
            lessons and improve your progress with personalized
            learning support.
          </p>

          <div className="mt-6 flex flex-wrap gap-4">

            <div className="rounded-xl bg-white/10 px-6 py-4">
              <p className="text-xs text-gray-400">
                Total Subjects
              </p>

              <p className="mt-1 text-2xl font-bold">
                6
              </p>
            </div>
            <div>
            </div>

            <div className="rounded-xl bg-white/10 px-6 py-4">
              <p className="text-xs text-gray-400">
                Completed Lessons
              </p>

              <p className="mt-1 text-2xl font-bold">
                24
              </p>
            </div>

            <div className="rounded-xl bg-white/10 px-6 py-4">
              <p className="text-xs text-gray-400">
                Overall Progress
              </p>

              <p className="mt-1 text-2xl font-bold">
                68%
              </p>
            </div>

          </div>

        </section>

        {/* Subjects */}
        <section>

          <div className="mb-5">
            <h2 className="text-xl font-bold text-gray-900">
              Your Subjects
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Select a subject to continue learning.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">

            {subjects.map((subject) => (
              <div
                key={subject.name}
                className="rounded-2xl border border-gray-200 bg-white p-6 transition hover:-translate-y-1 hover:border-slate-400 hover:shadow-lg"
              >

                {/* Subject Header */}
                <div className="flex items-start justify-between gap-4">

                  <div>
                    <h3 className="text-lg font-bold text-gray-900">
                      {subject.name}
                    </h3>

                    <p className="mt-2 text-sm leading-5 text-gray-500">
                      {subject.description}
                    </p>
                  </div>

                  <span className="whitespace-nowrap rounded-full bg-purple-100 px-3 py-1 text-xs font-semibold text-slate-400">
                    Form 2
                  </span>

                </div>

                {/* Progress */}
                <div className="mt-6">

                  <div className="mb-2 flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      Progress
                    </span>

                    <span className="text-sm font-semibold text-gray-900">
                      {subject.progress}%
                    </span>
                  </div>

                  <div className="h-2.5 overflow-hidden rounded-full bg-gray-200">
                    <div
                      className="h-full rounded-full bg-black"
                      style={{
                        width: `${subject.progress}%`,
                      }}
                    />
                  </div>

                </div>

                {/* Current Topic */}
                <div className="mt-6 rounded-xl bg-gray-50 p-4">

                  <p className="text-xs font-medium text-gray-500">
                    Current Topic
                  </p>

                  <p className="mt-1 text-sm font-semibold text-gray-900">
                    {subject.topic}
                  </p>

                </div>

                {/* Button */}
                <Link
                  to="/student/ai-tutor"
                  className="mt-5 block rounded-xl bg-slate-200 py-3 text-center text-sm font-semibold text-white transition hover:bg-slate-300"
                >
                  Continue Learning
                </Link>

              </div>
            ))}

          </div>

        </section>

        {/* Recommended Learning */}
        <section className="rounded-2xl border border-gray-200 bg-white p-7">

          <div>
            <h2 className="text-xl font-bold text-gray-900">
              Recommended for You
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Continue with topics that need more practice.
            </p>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2">

            {/* Mathematics Recommendation */}
            <div className="rounded-xl border border-gray-200 p-5">

              <p className="text-sm font-semibold text-slate-200">
                Mathematics
              </p>

              <h3 className="mt-2 font-bold text-gray-900">
                Introduction to Equations
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Continue practicing equations and improve your
                understanding step by step.
              </p>

              <Link
                to="/student/ai-tutor"
                className="mt-4 inline-block text-sm font-semibold text-purple-100 hover:text-purple-100"
              >
                Start Practice
              </Link>

            </div>

            {/* Biology Recommendation */}
            <div className="rounded-xl border border-gray-200 p-5">

              <p className="text-sm font-semibold text-slate-300">
                Biology
              </p>

              <h3 className="mt-2 font-bold text-gray-400">
                Human Body Systems
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Review the major human body systems and test your
                understanding with practice questions.
              </p>

              <Link
                to="/student/ai-tutor"
                className="mt-4 inline-block text-sm font-semibold text-blue-200 hover:text-blue-200"
              >
                Start Practice
              </Link>

            </div>

          </div>

        </section>

      </div>
    </div>
  );
};

export default MySubjects;