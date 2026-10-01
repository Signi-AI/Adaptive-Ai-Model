import React from "react";
import heroBg from "../../assets/herobg.jpeg";

const HowItWorks: React.FC = () => {
  return (
    <section
      id="how-it-works"
      className="relative overflow-hidden bg-cover bg-center bg-no-repeat px-6 py-20"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      {/* Semi-transparent white overlay to keep text legible */}
      <div className="absolute inset-0 bg-white/85 backdrop-blur-[2px]" />

      <div className="relative z-10 mx-auto max-w-6xl text-center">

        <h2 className="text-4xl font-bold text-gray-900">
          How It Works
        </h2>

        <p className="mx-auto mt-4 max-w-2xl text-gray-600">
          LearnAI makes learning simple by adapting to each
          student's needs and learning progress.
        </p>

        <div className="mt-12 grid gap-8 md:grid-cols-3">

          {/* Step 1 */}
          <div className="rounded-2xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-600 font-bold text-white shadow-md shadow-purple-600/20">
              1
            </div>

            <h3 className="mt-5 text-xl font-semibold text-gray-900">
              Create an Account
            </h3>

            <p className="mt-3 text-gray-600">
              Register and tell LearnAI your education level
              and class so we can understand your learning needs.
            </p>
          </div>

          {/* Step 2 */}
          <div className="rounded-2xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-600 font-bold text-white shadow-md shadow-purple-600/20">
              2
            </div>

            <h3 className="mt-5 text-xl font-semibold text-gray-900">
              Learn With AI
            </h3>

            <p className="mt-3 text-gray-600">
              Ask questions, study lessons, and get learning
              assistance from your AI-powered tutor.
            </p>
          </div>

          {/* Step 3 */}
          <div className="rounded-2xl border border-gray-100 bg-white/90 p-8 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-600 font-bold text-white shadow-md shadow-purple-600/20">
              3
            </div>

            <h3 className="mt-5 text-xl font-semibold text-gray-900">
              Track Your Progress
            </h3>

            <p className="mt-3 text-gray-600">
              Monitor your learning progress and receive
              personalized recommendations.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
};

export default HowItWorks;