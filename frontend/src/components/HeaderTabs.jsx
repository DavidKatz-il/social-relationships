import React, { useContext, useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import * as g from "../Global";
import logo from '../logo.png';

export const HeaderTabs = () => {
    const [token, setToken] = useContext(UserContext);
    const [activeTab, setActiveTab] = useState(window.location.pathname.substring(1, window.location.pathname.length));
    const [userName, setUserName] = useState("");

    const handleLogout = () => {
        setToken(null);
    };

    function getUser(user) {
        if (user && user.teacher_name) setUserName(user.teacher_name);
    }
    const fetchUser = async () => {
        await g.fetchData("GET", "application/json", token, "user", undefined, "", getUser);
    };

    useEffect(() => {
        fetchUser();
    }, [token])

    useEffect(() => {
        fetchUser();
    }, [])

    return (<>
        <nav className="navbar is-fixed-top">
            <div className="navbar-brand">
                <NavLink className="navbar-item" to="/" onClick={() => setActiveTab("home")}>
                    <img src={logo} alt="Logo" width="40" height="50" />
                </NavLink>
            </div>
            <div className="navbar-menu">
                <div className={"navbar-start"}>
                    <div className="tabs is-toggle is-medium" >
                        <ul className="navbar-item">
                            <li className={activeTab === "home" || activeTab === "" ? "is-active" : ""} onClick={() => setActiveTab("home")}>
                                <NavLink to="/home">
                                    <i className="icon is-small fa fa-home" />
                                    <span>Home</span>
                                </NavLink>
                            </li>
                            {token && <>
                                <li className={activeTab === "students" ? "is-active" : ""} onClick={() => setActiveTab("students")}>
                                    <NavLink to="/students">
                                        <i className="icon is-small fa fa-users" />
                                        <span>Students</span>
                                    </NavLink>
                                </li>
                                <li className={activeTab === "images" ? "is-active" : ""} onClick={() => setActiveTab("images")}>
                                    <NavLink to="/images">
                                        <i className="icon is-small fa fa-image" />
                                        <span>Images</span>
                                    </NavLink>
                                </li>
                                <li className={activeTab === "reports" ? "is-active" : ""} onClick={() => setActiveTab("reports")}>
                                    <NavLink to="/reports">
                                        <i className="icon is-small fa fa-file" />
                                        <span>Reports</span>
                                    </NavLink>
                                </li>
                            </>}
                        </ul>
                    </div></div>
                <div className="navbar-end">
                    <div className="navbar-item">
                        <div className="field is-grouped">
                            {token ? <>
                                <p className="control">
                                    <NavLink className="button" to="/User">
                                        <i className="icon fas fa-edit" />
                                        <span>{userName}</span>
                                    </NavLink>
                                </p>
                                <p className="control">
                                    <button className="button is-secondary" onClick={handleLogout}>
                                        <i className="icon fa fa-sign-out" />
                                        <span>Logout</span>
                                    </button>
                                </p>
                            </>
                                : <>
                                    <p className="control">
                                        <NavLink className="button is-primary" to="/Login">
                                            <i className="icon fa fa-sign-in" />
                                            <span>Login</span>
                                        </NavLink>
                                    </p>
                                    <p className="control">
                                        <NavLink className="button is-primary" to="/Register">
                                            <i className="icon fa fa-user-plus" />
                                            <span>Register</span>
                                        </NavLink>
                                    </p>
                                </>
                            }
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        <br />
    </>);
};