import React from "react";
import { Link } from "react-router-dom";

interface SubjectCardProps {
  id: string;
  name: string;
  description: string;
  progress: number;
  topics: number;
  completedTopics: number;
  icon: string;
}

const SubjectCard: React.FC<SubjectCardProps> = ({
  id,
  name,
  description,
  progress,
  topics,
  completedTopics,
  icon,
}) => {
  return (
    <Link
      to={`/subjects/${id}`}
      className="group block rounded-3xl border border-gray-200 bg-white p-5 shadow-sm transition duration-300 hover:-translate-y-1 hover:border-gray-300 hover:shadow-lg"
    >

      {/* Top */}
      <div className="flex items-start justify-between">

        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-100 text-xl font-bold text-black transition duration-300 group-hover:bg-black group-hover:text-white">
          {icon}
        </div>

        <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-semibold text-gray-600">
          {progress}%
        </span>

      </div>

      {/* Subject */}
      <h3 className="mt-5 text-lg font-bold text-black">
        {name}
      </h3>

      <p className="mt-2 min-h-[48px] text-sm leading-6 text-gray-500">
        {description}
      </p>

      {/* Progress */}
      <div className="mt-5">

        <div className="h-2 overflow-hidden rounded-full bg-gray-100">

          <div
            className="h-full rounded-full bg-black transition-all duration-700"
            style={{
              width: `${progress}%`,
            }}
          />

        </div>

        <div className="mt-3 flex items-center justify-between">

          <span className="text-xs text-gray-400">
            {completedTopics} / {topics} topics
          </span>

          <span className="text-xs font-semibold text-black transition-transform duration-300 group-hover:translate-x-1">
            Open →
          </span>

        </div>

      </div>

    </Link>
  );
};

export default SubjectCard;