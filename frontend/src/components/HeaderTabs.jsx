import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import logo from '../logo.jpeg';

export const HeaderTabs = () => {
    const [token, setToken] = useContext(UserContext);
    const handleLogout = () => { setToken(null); };
    const tabActive = (tab_name) => { return window.location.pathname === "/" + tab_name ? "is-active" : "" };

    return (
        <>
            <nav className="navbar is-info">
                <div className="navbar-brand">
                    <NavLink className="navbar-item" to="/">
                        <img src={logo} alt="" width="28" height="28" />
                    </NavLink>
                </div>
                <div className="navbar-menu">
                    <div className="navbar-start is-link">
                        <NavLink className="navbar-item" to="/">Home</NavLink>
                    </div>
                    <div className="navbar-end">
                        <div className="navbar-item">
                            <div className="field is-grouped">
                                {token ?
                                    <p className="control">
                                        <button className="button is-secondary" onClick={handleLogout}>
                                            <span className="icon">
                                                <i className="fa fa-sign-out"></i>
                                            </span>
                                            <span>Logout</span>
                                        </button>
                                    </p>
                                    : <>
                                        <p className="control">
                                            <a className="button is-primary" href="/login">
                                                <span className="icon">
                                                    <i className="fa fa-sign-in"></i>
                                                </span>
                                                <span>Login</span>
                                            </a>
                                        </p>
                                        <p className="control">
                                            <a className="button is-primary" href="/register">
                                                <span className="icon">
                                                    <i className="fa fa-user-plus"></i>
                                                </span>
                                                <span>Register</span>
                                            </a>
                                        </p>
                                    </>}
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
            <section className="hero is-info">
                <div className="hero-body">
                    <div className="container">
                        <h1 className="title">
                            Social Relationships
                        </h1>
                        <h2 className="subtitle">
                            based on face recognition
                        </h2>
                    </div>
                </div>
                {token ?
                    <div className="tabs is-boxed is-centered main-menu" id="tabs">
                        <ul>
                            <li id="tab-students" className={tabActive("students")}>
                                <a href="/students">
                                    <span className="icon is-small"><i className="fa fa-users"></i></span>
                                    <span>Students</span>
                                </a>
                            </li>
                            <li id="tab-images" className={tabActive("images")}>
                                <a href="/images">
                                    <span className="icon is-small"><i className="fa fa-image"></i></span>
                                    <span>Images</span>
                                </a>
                            </li>
                            <li id="tab-reports" className={tabActive("reports")}>
                                <a href="/reports">
                                    <span className="icon is-small"><i className="fa fa-file"></i></span>
                                    <span>Reports</span>
                                </a>
                            </li>
                        </ul>
                    </div>
                    : <></>}
            </section>
            <br></br>
        </>
    );
};
