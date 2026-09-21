import { Route, Routes } from "react-router-dom";
import HomePage from "../pages/main/HomePage";
import Profile from "../pages/main/ProfilePage";
import Dashboard from "../pages/main/Dashbord";
import Register from "../pages/main/Register";
import Login from "../pages/main/LoginPage";
import StudentDashboard from "../pages/main/StudentDashboard";

const AppRoutes = () => {
  return (
    <div>
        <Routes>
          <Route path="/" element ={<Dashboard/>}/>
          <Route path="/login" element = {<Login/>}/>
          <Route path="/studentdashboard" element={<StudentDashboard/>}/>
          <Route path="/register" element={<Register/>}/>
            <Route path="/homepage" element = {<HomePage/>}/>
            <Route path="/profile" element ={<Profile/>}/>
        </Routes>

    </div>
  )
}

export default AppRoutes;