import { Outlet } from "react-router-dom";
import StudentSidebar from "../main/StudentSidebar";

const StudentLayout = () => {
  return (
    <div className="min-h-screen bg-gray-100">

      {/* Fixed Sidebar */}
      <StudentSidebar />

      {/* Main Content */}
      <main className="ml-64 min-h-screen">
        <Outlet />
      </main>

    </div>
  );
};

export default StudentLayout