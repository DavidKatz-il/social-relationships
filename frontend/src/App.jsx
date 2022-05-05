import React, { useContext } from "react";
import { Route, BrowserRouter, Routes } from 'react-router-dom';
import { HeaderTabs } from "./components/HeaderTabs";
import { UserContext } from "./context/UserContext";
import { Register } from "./components/User/Register";
import { Login } from "./components/User/Login";
import { ImagesTable } from "./components/Image/ImagesTable";
import { PersonsTable } from "./components/Person/PersonsTable";
import { ReportsTable } from "./components/Report/ReportsTable";

export const App = () => {
  const [token] = useContext(UserContext);

  return (
    <BrowserRouter>
      <HeaderTabs />
      <Routes>
        <Route path="/" element={token ? <PersonsTable /> : <Login />} />
        <Route path="/login" element={token ? <PersonsTable /> : <Login />} />
        <Route path="/register" element={token ? <PersonsTable /> : <Register />} />
        <Route path="/students" element={token ? <PersonsTable /> : <Login />} />
        <Route path="/images" element={token ? <ImagesTable /> : <Login />} />
        <Route path="/reports" element={token ? <ReportsTable /> : <Login />} />
      </Routes>
    </BrowserRouter>
  );
};