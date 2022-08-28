import React, { useState, useContext } from "react";
import { NavLink } from "react-router-dom";
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import logo from '../../logo.png';
import * as g from "../../Global";

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  function setData(data) {
    if (data && data.access_token) setToken(data.access_token);
  }

  async function submitLogin() {
    const body = JSON.stringify(`grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`);
    await g.fetchData("POST", "application/x-www-form-urlencoded", undefined, "token", setErrorMessage,
      "", setData, undefined, body);
  }

  function handleSubmit(e) {
    e.preventDefault();
    submitLogin();
  }

  return (
    <div className="hero-body">
      <div className="container has-text-centered">
        <div className="column is-4 is-offset-4">
          <hr className="login-hr" />
          <p className="subtitle has-text-black">Please login to proceed.</p>
          <div className="box" onSubmit={handleSubmit}>
            <figure className="avatar">
              <img src={logo} alt="Logo" />
            </figure>
            <form>
              <div className="field">
                <div className="control">
                  <input className="input is-large" type="email" placeholder="Enter your email" autoFocus=""
                    value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
              </div>
              <div className="field">
                <div className="control">
                  <input className="input is-large" type="password" placeholder="Enter your password"
                    value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
              </div>
              <div className="field">
                <ErrorMessage message={errorMessage} />
                <br />
              </div>
              <button className="button is-block is-info is-large is-fullwidth" type="submit">
                <span>Login </span>
                <i className="fa fa-sign-in" aria-hidden="true" />
              </button>
            </form>
          </div>
          <p className="has-text-grey">
            <NavLink to="/register">Don't have an account? &nbsp;·&nbsp; Register</NavLink>
          </p>
        </div>
      </div>
    </div>
  );
};