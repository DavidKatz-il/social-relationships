import React, { useContext } from "react";
import { Route, BrowserRouter, Routes } from 'react-router-dom';
import { HeaderTabs } from "./components/HeaderTabs";
import { UserContext } from "./context/UserContext";
import { Register } from "./components/User/Register";
import { Login } from "./components/User/Login";
import { ImagesTable } from "./components/Image/ImagesTable";
import { StudentsTable } from "./components/Student/StudentsTable";
import { ReportsTable } from "./components/Report/ReportsTable";
import { Home } from "./components/Info/Home";

export const App = () => {
  const [token] = useContext(UserContext);

  return (
    <BrowserRouter>
      <HeaderTabs />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={token ? <Home /> : <Login />} />
        <Route path="/register" element={token ? <Home /> : <Register />} />
        <Route path="/students" element={token ? <StudentsTable /> : <Home />} />
        <Route path="/images" element={token ? <ImagesTable /> : <Home />} />
        <Route path="/reports" element={token ? <ReportsTable /> : <Home />} />
      </Routes>
    </BrowserRouter>
  );
};