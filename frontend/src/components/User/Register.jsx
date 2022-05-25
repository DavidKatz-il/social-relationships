import React, { useContext, useState } from "react";
import { UserContext } from "../../context/UserContext";
import { ErrorMessage } from "../Info/ErrorMessage";
import logo from '../../logo.png';
import { NavLink } from "react-router-dom";
import * as g from "../../Global";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [teacherName, setTeacherName] = useState("");
  const [schoolName, setSchoolName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmationPassword, setConfirmationPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  function setData(data) {
    setToken(data.access_token);
  }

  async function submitRegistration() {
    const body = JSON.stringify({ email: email, hashed_password: password, teacher_name: teacherName, school_name: schoolName });
    await g.fetchData("POST", "application/json", undefined, "/api/users", setErrorMessage, "", setData, undefined, body);
    /*const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, hashed_password: password }),
    };
    const response = await fetch("/api/users", requestOptions);
    const data = await response.json();
    if (!response.ok)
      setErrorMessage(data.detail);
    else
      setToken(data.access_token);*/
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password === confirmationPassword && password.length > 5) submitRegistration();
    else setErrorMessage("Ensure that the passwords match and greater than 5 characters");
  };

  return (
    <div className="hero-body">
      <div className="container has-text-centered">
        <div className="column is-4 is-offset-4">
          <hr className="login-hr" />
          <p className="subtitle has-text-black">Please register to proceed.</p>
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
                  <input className="input is-large" type="text" placeholder="Enter your name" autoFocus=""
                    value={teacherName} onChange={(e) => setTeacherName(e.target.value)} required />
                </div>
              </div>
              <div className="field">
                <div className="control">
                  <input className="input is-large" type="text" placeholder="Enter the school name" autoFocus=""
                    value={schoolName} onChange={(e) => setSchoolName(e.target.value)} required />
                </div>
              </div>
              <div className="field">
                <div className="control">
                  <input className="input is-large" type="password" placeholder="Enter your password"
                    value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
              </div>
              <div className="field">
                <div className="control">
                  <input className="input is-large" type="password" placeholder="Enter your password again"
                    value={confirmationPassword} onChange={(e) => setConfirmationPassword(e.target.value)} required />
                </div>
              </div>
              <div className="field">
                <ErrorMessage message={errorMessage} />
                <br />
              </div>
              <button className="button is-block is-info is-large is-fullwidth" type="submit">
                <span>Register </span>
                <i className="fa fa-sign-in" aria-hidden="true" />
              </button>
            </form>
          </div>
          <p className="has-text-grey">
            <NavLink to="/Login">Already have an account?  &nbsp;·&nbsp; Login</NavLink>
          </p>
        </div>
      </div>
    </div>
  );
};