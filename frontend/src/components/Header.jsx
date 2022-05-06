import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../context/UserContext";
import logo from '../logo.jpeg';

export const Header = () => {
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => { setToken(null); };

  return (
    <>
      <nav className="navbar" style={{ backgroundColor: "lightblue" }}>
        <div className="navbar-brand">
          <NavLink className="navbar-item" to="/">
            <img src={logo} alt="Social-Relationships" width="40" height="40" />
          </NavLink>
        </div>

        <div className="navbar-menu">
          <div className="navbar-start">
            <NavLink className="navbar-item" to="/students">Students</NavLink>
            <NavLink className="navbar-item" to="/images">Images</NavLink>
            <NavLink className="navbar-item" to="/reports">Reports</NavLink>
          </div>

          <div className="navbar-end">
            <div className="navbar-item">
              <div className="field is-grouped">
                {token ?
                  <p className="control">
                    <button className="button is-secondary" onClick={handleLogout}>Logout</button>
                  </p>
                  : <>
                    <p className="control">
                      <NavLink className="button is-primary" to="/login">Login</NavLink>
                    </p>
                    <p className="control">
                      <NavLink className="button is-secondary" to="/register">Register</NavLink>
                    </p>
                  </>}
              </div>
            </div>
          </div>
        </div>
      </nav>
      <hr />
    </>
  );
};