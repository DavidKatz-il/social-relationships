import React, { useContext, useState } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import logo from '../logo.png';
import logo_social_relationships from '../social_relationships.png';

export const HeaderTabs = () => {
    const [token, setToken] = useContext(UserContext);
    const [activeTab, setActiveTab] = useState(window.location.pathname.substring(1, window.location.pathname.length));

    const handleLogout = () => {
        setToken(null);
    };

    return (<>
        <nav className="navbar">{/* className="navbar-menu is-info" set background color for the tabs pane also*/}
            <div className="navbar-brand">
                <NavLink className="navbar-item" to="/" onClick={() => setActiveTab("home")}>
                    <img src={logo} alt="Logo" width="28" height="28" />
                </NavLink>
            </div>
            <div className="navbar-menu">
                <div className={"navbar-start"}>
                    <div className="tabs is-boxed" >
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
                                {/*<li style={{ paddingRight: 70, paddingLeft: 70 }} />*/}
                            </>}
                            {/*
                            <li className={activeTab === "about" ? "is-active" : ""} onClick={() => setActiveTab("about")}>
                                <NavLink to="/about">
                                    <i className="icon is-small fa fa-info-circle" />
                                    <span>About</span>
                                </NavLink>
                            </li>
                            <li className={activeTab === "contact" ? "is-active" : ""} onClick={() => setActiveTab("contact")}>
                                <NavLink to="/contact">
                                    <i className="icon is-small fa fa-phone-alt" />
                                    <span>Contact us</span>
                                </NavLink>
                            </li>
                            */}
                        </ul>
                    </div></div>
                <div className="navbar-end">
                    <div className="navbar-item">
                        <div className="field is-grouped">
                            {token ?
                                <p className="control">
                                    <button className="button is-secondary" onClick={handleLogout}>
                                        <i className="icon fa fa-sign-out" />
                                        <span>Logout</span>
                                    </button>
                                </p>
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
        <section className="hero is-primary">
            <div style={{ padding: 20 }}>
                <div className="container">
                    <div className="columns">
                        <div className="column">
                            <img src={logo_social_relationships} alt="social_relationships" width="200" height="100" />
                        </div>
                        <div className="column">
                            <h1 className="title">Page</h1>
                        </div>
                        <div className="column">
                            <h2 className="subtitle">some info about the page</h2>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br />
    </>);
};