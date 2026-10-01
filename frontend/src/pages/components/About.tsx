import React from "react";
import heroBg from "../../assets/herobg.jpeg";

const About: React.FC = () => {
  return (
    <section
      id="about"
      className="relative min-h-[500px] overflow-hidden bg-cover bg-center bg-no-repeat px-6 py-20"
      style={{ backgroundImage: `url(${heroBg})` }}
    >
      {/* Semi-transparent white overlay to keep content legible */}
      <div className="absolute inset-0 bg-white/85 backdrop-blur-[2px]" />

      <div className="relative z-10 mx-auto max-w-6xl text-center">

        <h2 className="mb-6 text-4xl font-bold text-gray-900">
          About LearnAI
        </h2>

        <p className="mx-auto max-w-3xl text-lg leading-8 text-gray-600">
          LearnAI is an AI-powered learning platform designed to help
          students learn more effectively. It provides personalized
          learning experiences, intelligent assistance, and useful
          learning resources based on each student's needs.
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-3">

          <div className="rounded-2xl border border-gray-100 bg-white/90 p-6 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <h3 className="mb-3 text-xl font-semibold text-purple-600">
              Personalized Learning
            </h3>
            <p className="text-gray-600">
              Learning content can be adapted to the student's
              learning needs and progress.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-100 bg-white/90 p-6 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <h3 className="mb-3 text-xl font-semibold text-purple-600">
              AI Assistance
            </h3>
            <p className="text-gray-600">
              Students can interact with AI to ask questions and
              receive learning support.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-100 bg-white/90 p-6 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-purple-200 hover:shadow-xl">
            <h3 className="mb-3 text-xl font-semibold text-purple-600">
              Student Progress
            </h3>
            <p className="text-gray-600">
              Students can follow their learning activities and
              monitor their progress.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
};

export default About;