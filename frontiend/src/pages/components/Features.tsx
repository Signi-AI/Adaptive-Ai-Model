import React from "react";

const Features: React.FC = () => {
  return (
    <section
      id="features"
      className="w-full bg-white px-5 py-20 md:px-8 lg:py-28"
    >
      <div className="mx-auto max-w-7xl">

        {/* Section Header */}
        <div className="mx-auto max-w-3xl text-center">

          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-gray-200 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-600">
            <span className="h-2 w-2 rounded-full bg-black" />
            Powerful Learning Features
          </div>

          <h2 className="text-3xl font-bold tracking-tight text-black sm:text-4xl md:text-5xl">
            Everything you need to
            <br />
            <span className="text-gray-400">
              learn better.
            </span>
          </h2>

          <p className="mt-5 text-base leading-7 text-gray-500 sm:text-lg">
            Our adaptive learning platform combines personalized learning,
            offline access, progress tracking, and AI support to help every
            student learn at their own pace.
          </p>
        </div>

        {/* Features Grid */}
        <div className="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">

          {/* Feature 1 */}
          <div className="group rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-2xl text-white transition duration-300 group-hover:scale-105">
              🧠
            </div>

            <h3 className="mt-6 text-xl font-bold text-black">
              Adaptive Learning
            </h3>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              The system analyzes your performance and adjusts lessons,
              questions, and difficulty based on your learning level.
            </p>

            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-black">
              <span>Personalized for you</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 2 */}
          <div className="group rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gray-100 text-2xl text-black transition duration-300 group-hover:scale-105">
              📶
            </div>

            <h3 className="mt-6 text-xl font-bold text-black">
              Learn Offline
            </h3>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              Continue studying, answering questions, and tracking your
              progress even when you don't have an internet connection.
            </p>

            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-black">
              <span>Learn anywhere</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="group rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gray-100 text-2xl text-black transition duration-300 group-hover:scale-105">
              📊
            </div>

            <h3 className="mt-6 text-xl font-bold text-black">
              Progress Tracking
            </h3>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              Track your topics, assignments, scores, strengths, and areas
              that need more practice from one simple dashboard.
            </p>

            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-black">
              <span>Know your progress</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 4 */}
          <div className="group rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gray-100 text-2xl text-black transition duration-300 group-hover:scale-105">
              🤖
            </div>

            <h3 className="mt-6 text-xl font-bold text-black">
              AI Tutor
            </h3>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              Ask questions, get explanations, and receive learning guidance
              from an AI assistant designed to support your studies.
            </p>

            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-black">
              <span>Get learning support</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 5 */}
          <div className="group rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gray-100 text-2xl text-black transition duration-300 group-hover:scale-105">
              📝
            </div>

            <h3 className="mt-6 text-xl font-bold text-black">
              Smart Assignments
            </h3>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              Receive assignments based on your current understanding and
              automatically identify the topics that need more attention.
            </p>

            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-black">
              <span>Practice smarter</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 6 */}
          <div className="group rounded-3xl border border-gray-200 bg-white p-7 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-xl">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gray-100 text-2xl text-black transition duration-300 group-hover:scale-105">
              🇹🇿
            </div>

            <h3 className="mt-6 text-xl font-bold text-black">
              Tanzanian Curriculum
            </h3>

            <p className="mt-3 text-sm leading-6 text-gray-500">
              Learning content is designed around the Tanzanian education
              system, supporting students from Primary to A-Level.
            </p>

            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-black">
              <span>Built for students</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>
        </div>

        {/* Bottom Highlight */}
        <div className="mt-16 overflow-hidden rounded-3xl bg-black px-6 py-10 text-white sm:px-10 lg:px-14 lg:py-12">
          <div className="flex flex-col items-center justify-between gap-8 text-center lg:flex-row lg:text-left">

            <div className="max-w-2xl">
              <p className="text-sm font-semibold uppercase tracking-widest text-gray-400">
                One platform
              </p>

              <h3 className="mt-3 text-2xl font-bold sm:text-3xl">
                Your learning adapts as you grow.
              </h3>

              <p className="mt-3 text-sm leading-6 text-gray-400 sm:text-base">
                Study at your own pace, practice your weak areas, and move
                forward when you're ready.
              </p>
            </div>

            <div className="flex shrink-0 items-center gap-3">

              <div className="rounded-2xl border border-gray-700 bg-gray-900 px-5 py-4">
                <p className="text-xs text-gray-500">
                  Progress
                </p>

                <p className="mt-1 text-2xl font-bold">
                  68%
                </p>
              </div>

              <div className="rounded-2xl border border-gray-700 bg-gray-900 px-5 py-4">
                <p className="text-xs text-gray-500">
                  Learning
                </p>

                <p className="mt-1 text-2xl font-bold">
                  Adaptive
                </p>
              </div>

            </div>
          </div>
        </div>

      </div>
    </section>
  );
};

export default Features;