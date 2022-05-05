import React, { useContext, useState } from "react";
import { UserContext } from "../context/UserContext";
import logo from '../logo.jpeg';


export const HeaderTabs = () => {
  const [token, setToken] = useContext(UserContext);
  const handleLogout = () => { setToken(null); };
    
  return (
    <>
    <nav className="navbar is-info">
        <div className="navbar-brand">
            <a className="navbar-item" href="#">
                <img src={logo} alt="" width="28" height="28"/>
            </a>
        </div>
        <div className="navbar-menu">
            <div className="navbar-start is-link">
                <a className="navbar-item" href="/">
                    Home
                </a>
            </div>
            <div className="navbar-end">
                <div className="navbar-item">
                    <div className="field is-grouped">
                    {token ?
                    <p className="control">
                        <a className="button is-secondary" onClick={handleLogout}>
                            <span className="icon">
                                <i className="fa fa-sign-out"></i>
                            </span>
                            <span>Logout</span>
                        </a>
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
              <li id="1">
                  <a href="/students">
                      <span className="icon is-small"><i className="fa fa-superpowers"></i></span>
                      <span>Students</span>
                  </a>
              </li>
              <li id="2">
                  <a href="/images">
                      <span className="icon is-small"><i className="fa fa-image"></i></span>
                      <span>Images</span>
                  </a>
              </li>
              <li id="3">
                  <a href="/reports">
                      <span className="icon is-small"><i className="fa fa-empire"></i></span>
                      <span>Reports</span>
                  </a>
              </li>
          </ul>
      </div>
    :<></>}
    </section>
    <br></br>
    </>
  );
};
