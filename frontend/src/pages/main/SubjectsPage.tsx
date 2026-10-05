import React from "react";
import { Link } from "react-router-dom";
import StudentSidebar from "./StudentSidebar";

interface ProgressCircleProps {
  progress: number;
  size?: number;
}

const ProgressCircle: React.FC<ProgressCircleProps> = ({
  progress,
  size = 72,
}) => {
  const strokeWidth = 7;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div
      className="relative flex shrink-0 items-center justify-center"
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
          className="text-slate-100"
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

      <span className="absolute text-sm font-extrabold text-slate-800">
        {progress}%
      </span>
    </div>
  );
};

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
    <div className="min-h-screen bg-slate-50">
      <StudentSidebar />

      <div className="ml-60">
        {/* HEADER */}
        <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 px-8 py-6 backdrop-blur-xl">
          <h1 className="text-2xl font-bold tracking-tight text-slate-800">
            My Subjects
          </h1>

          <p className="mt-1 text-sm text-slate-500">
            View your subjects and continue your learning
          </p>
        </header>

        <main className="space-y-8 p-8">
          {/* SUMMARY */}
          <section className="rounded-2xl bg-slate-300 p-8 text-slate-900">
            <h2 className="text-2xl font-bold">
              Your Learning Subjects
            </h2>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-700">
              You are currently studying 6 subjects. Continue your
              lessons and improve your progress with personalized
              learning support.
            </p>

            <div className="mt-6 flex flex-wrap gap-4">
              <div className="rounded-xl bg-white/50 px-6 py-4">
                <p className="text-xs font-medium text-slate-600">
                  Total Subjects
                </p>

                <p className="mt-1 text-2xl font-bold text-slate-900">
                  6
                </p>
              </div>

              <div className="rounded-xl bg-white/50 px-6 py-4">
                <p className="text-xs font-medium text-slate-600">
                  Completed Lessons
                </p>

                <p className="mt-1 text-2xl font-bold text-slate-900">
                  24
                </p>
              </div>

              <div className="rounded-xl bg-white/50 px-6 py-4">
                <p className="text-xs font-medium text-slate-600">
                  Overall Progress
                </p>

                <p className="mt-1 text-2xl font-bold text-slate-900">
                  68%
                </p>
              </div>
            </div>
          </section>

          {/* SUBJECTS */}
          <section>
            <div className="mb-5">
              <h2 className="text-xl font-bold text-slate-800">
                Your Subjects
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Select a subject to continue learning.
              </p>
            </div>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
              {subjects.map((subject) => (
                <div
                  key={subject.name}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:border-blue-200 hover:shadow-md"
                >
                  {/* SUBJECT HEADER */}
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <h3 className="text-lg font-bold text-slate-800">
                        {subject.name}
                      </h3>

                      <p className="mt-2 text-sm leading-5 text-slate-500">
                        {subject.description}
                      </p>
                    </div>

                    <span className="whitespace-nowrap rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                      Form 2
                    </span>
                  </div>

                  {/* CIRCULAR PROGRESS */}
                  <div className="mt-6 flex items-center gap-4 rounded-xl bg-slate-50 p-4">
                    <ProgressCircle progress={subject.progress} />

                    <div>
                      <p className="text-xs font-medium text-slate-500">
                        Learning Progress
                      </p>

                      <p className="mt-1 text-sm font-bold text-slate-800">
                        {subject.progress}% completed
                      </p>

                      <p className="mt-1 text-[11px] text-slate-500">
                        Keep going to complete this subject.
                      </p>
                    </div>
                  </div>

                  {/* CURRENT TOPIC */}
                  <div className="mt-5 rounded-xl bg-slate-50 p-4">
                    <p className="text-xs font-medium text-slate-500">
                      Current Topic
                    </p>

                    <p className="mt-1 text-sm font-semibold text-slate-800">
                      {subject.topic}
                    </p>
                  </div>

                  {/* CONTINUE LEARNING -> TUTOR HOME */}
                  <Link
                    to="/learn"
                    className="mt-5 flex w-full items-center justify-center rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 active:scale-[0.98]"
                  >
                    Continue Learning
                  </Link>
                </div>
              ))}
            </div>
          </section>

          {/* RECOMMENDED */}
          <section className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm">
            <div>
              <h2 className="text-xl font-bold text-slate-800">
                Recommended for You
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Continue with topics that need more practice.
              </p>
            </div>

            <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2">
              {/* MATHEMATICS */}
              <div className="rounded-xl border border-slate-200 p-5 transition hover:border-blue-200 hover:bg-blue-50/20">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm font-semibold text-slate-600">
                      Mathematics
                    </p>

                    <h3 className="mt-2 font-bold text-slate-800">
                      Introduction to Equations
                    </h3>
                  </div>

                  <ProgressCircle progress={75} size={64} />
                </div>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                  Continue practicing equations and improve your
                  understanding step by step.
                </p>

                <Link
                  to="/learn"
                  className="mt-4 inline-block text-sm font-semibold text-blue-600 transition hover:text-blue-700"
                >
                  Start Practice →
                </Link>
              </div>

              {/* BIOLOGY */}
              <div className="rounded-xl border border-slate-200 p-5 transition hover:border-blue-200 hover:bg-blue-50/20">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm font-semibold text-slate-600">
                      Biology
                    </p>

                    <h3 className="mt-2 font-bold text-slate-800">
                      Human Body Systems
                    </h3>
                  </div>

                  <ProgressCircle progress={45} size={64} />
                </div>

                <p className="mt-3 text-sm leading-6 text-slate-500">
                  Review the major human body systems and test your
                  understanding with practice questions.
                </p>

                <Link
                  to="/learn"
                  className="mt-4 inline-block text-sm font-semibold text-blue-600 transition hover:text-blue-700"
                >
                  Start Practice →
                </Link>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default MySubjects;