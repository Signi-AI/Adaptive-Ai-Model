import { Route, Routes } from "react-router-dom";
import HomePage from "../pages/main/HomePage";
import Profile from "../pages/main/ProfilePage";
import Dashboard from "../pages/main/Dashbord";
import Register from "../pages/main/Register";
import Login from "../pages/main/LoginPage";
import StudentDashboard from "../pages/main/StudentDashboard";
import StudentLayout from "../pages/main/Studentlayout";
import AitutorialPage from "../pages/main/AitutorialPage";
import SubjectsPage from "../pages/main/SubjectsPage";
import Myprogress from "../pages/main/Myprogress";
import AssignmentPage from "../pages/main/AssignmentPage";
import Notifications from "../pages/components/Notification";
import Setting from "../pages/main/Setting";
import SubjectDetailsPage from "../pages/main/SubjectDetailsPage";
import LearningMaterialsPage from "../pages/main/LearningPage";
import TeacherDashboard from "../pages/main/TeacherDashboard";
import TutorHome from "../pages/learn/TutorHome";

const AppRoutes = () => {
  return (
    <div>
        <Routes>
          <Route path="/" element ={<Dashboard/>}/>
          <Route path="/teacher" element={<TeacherDashboard/>}/>

          <Route path="/materials"element={<LearningMaterialsPage/>}/>
          <Route path="/subjects/physics" element ={<SubjectDetailsPage/>}/>
          <Route path="/settings" element={<Setting/>}/>
          <Route path="/student-dashboard" element ={<StudentDashboard/>}/>
          <Route path="/notifications" element={<Notifications/>}/>
          <Route path="/assignments" element={<AssignmentPage/>}/>
          <Route path="progress" element ={<Myprogress/>}/>
          <Route path="/student/ai-tutor" element ={<AitutorialPage/>}/>
          <Route path="/subjects" element ={<SubjectsPage/>}/>
          <Route path="/ studentlayout" element ={<StudentLayout/>}/>
          <Route path="/ai-tutor" element ={<AitutorialPage/>}/>
          <Route path="/learn" element={<TutorHome/>}/>
          <Route path="/login" element = {<Login/>}/>
          <Route path="/register" element={<Register/>}/>
            <Route path="/homepage" element = {<HomePage/>}/>
            <Route path="/profile" element ={<Profile/>}/>
        </Routes>

    </div>
  )
}

export default AppRoutes;