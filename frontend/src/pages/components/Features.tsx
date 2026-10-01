import React from "react";
import heroBg from "../../assets/herobg.jpeg";

const Features: React.FC = () => {
  return (
    <section
      id="features"
      className="relative w-full overflow-hidden bg-cover bg-center bg-no-repeat px-5 py-20 md:px-8 lg:py-28"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      {/* Semi-transparent white overlay to keep cards and text crisp */}
      <div className="absolute inset-0 bg-white/85 backdrop-blur-[2px]" />

      <div className="relative z-10 mx-auto max-w-7xl">

        {/* Section Header */}
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white/90 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-gray-700 shadow-sm backdrop-blur-md">
            <span className="h-2 w-2 rounded-full bg-purple-600 animate-pulse" />
            Powerful Learning Features
          </div>

          <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl md:text-5xl">
            Everything you need to
            <br />
            <span className="text-gray-400">
              learn better.
            </span>
          </h2>

          <p className="mt-5 text-base leading-relaxed text-gray-600 sm:text-lg">
            Our adaptive learning platform combines personalized learning,
            offline access, progress tracking, and AI support to help every
            student learn at their own pace.
          </p>
        </div>

        {/* Features Grid */}
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

          {/* Feature 1 */}
          <div className="group flex flex-col justify-between rounded-3xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-purple-600">
                01
              </span>
              <h3 className="mt-4 text-xl font-bold text-gray-900">
                Adaptive Learning
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-600">
                The system analyzes your performance and adjusts lessons,
                questions, and difficulty based on your learning level.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
              <span>Personalized for you</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 2 */}
          <div className="group flex flex-col justify-between rounded-3xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-purple-600">
                02
              </span>
              <h3 className="mt-4 text-xl font-bold text-gray-900">
                Learn Offline
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-600">
                Continue studying, answering questions, and tracking your
                progress even when you don't have an internet connection.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
              <span>Learn anywhere</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 3 */}
          <div className="group flex flex-col justify-between rounded-3xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-purple-600">
                03
              </span>
              <h3 className="mt-4 text-xl font-bold text-gray-900">
                Progress Tracking
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-600">
                Track your topics, assignments, scores, strengths, and areas
                that need more practice from one simple dashboard.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
              <span>Know your progress</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 4 */}
          <div className="group flex flex-col justify-between rounded-3xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-purple-600">
                04
              </span>
              <h3 className="mt-4 text-xl font-bold text-gray-900">
                AI Tutor
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-600">
                Ask questions, get explanations, and receive learning guidance
                from an AI assistant designed to support your studies.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
              <span>Get learning support</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 5 */}
          <div className="group flex flex-col justify-between rounded-3xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-purple-600">
                05
              </span>
              <h3 className="mt-4 text-xl font-bold text-gray-900">
                Smart Assignments
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-600">
                Receive assignments based on your current understanding and
                automatically identify the topics that need more attention.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
              <span>Practice smarter</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

          {/* Feature 6 */}
          <div className="group flex flex-col justify-between rounded-3xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div>
              <span className="text-xs font-bold uppercase tracking-widest text-purple-600">
                06
              </span>
              <h3 className="mt-4 text-xl font-bold text-gray-900">
                Tanzanian Curriculum
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-600">
                Learning content is designed around the Tanzanian education
                system, supporting students from Primary to A-Level.
              </p>
            </div>

            <div className="mt-8 flex items-center gap-2 text-sm font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">
              <span>Built for students</span>
              <span className="transition-transform duration-300 group-hover:translate-x-1">
                →
              </span>
            </div>
          </div>

        </div>

        {/* Bottom Highlight Banner */}
        <div className="mt-16 overflow-hidden rounded-3xl bg-gray-900/95 px-6 py-10 text-white shadow-xl backdrop-blur-md sm:px-10 lg:px-14 lg:py-12">
          <div className="flex flex-col items-center justify-between gap-8 text-center lg:flex-row lg:text-left">

            <div className="max-w-2xl">
              <p className="text-xs font-bold uppercase tracking-widest text-purple-400">
                One platform
              </p>

              <h3 className="mt-3 text-2xl font-bold sm:text-3xl">
                Your learning adapts as you grow.
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-gray-400 sm:text-base">
                Study at your own pace, practice your weak areas, and move
                forward when you're ready.
              </p>
            </div>

            <div className="flex shrink-0 items-center gap-4">

              <div className="rounded-2xl border border-gray-800 bg-gray-950 px-6 py-4 shadow-inner">
                <p className="text-xs font-medium text-gray-500">
                  Progress
                </p>

                <p className="mt-1 text-2xl font-extrabold text-white">
                  68%
                </p>
              </div>

              <div className="rounded-2xl border border-gray-800 bg-gray-950 px-6 py-4 shadow-inner">
                <p className="text-xs font-medium text-gray-500">
                  Learning
                </p>

                <p className="mt-1 text-2xl font-extrabold text-purple-400">
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