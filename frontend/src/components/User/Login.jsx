import React, { useState, useContext } from "react";
import { ErrorMessage } from "../ErrorMessage";
import { UserContext } from "../../context/UserContext";
import logo from '../../logo.jpeg';

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [, setToken] = useContext(UserContext);

  const submitLogin = async () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: JSON.stringify(`grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`),
    };
    const response = await fetch("/api/token", requestOptions);
    const data = await response.json();
    if (!response.ok) setErrorMessage(data.detail);
    else setToken(data.access_token);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitLogin();
  };

  return (
    <div className="hero-body">
        <div className="container has-text-centered">
            <div className="column is-4 is-offset-4">
                <hr className="login-hr"/>
                <p className="subtitle has-text-black">Please login to proceed.</p>
                <div className="box" onSubmit={handleSubmit}>
                    <figure className="avatar"> <img src={logo} alt=""/> </figure>
                    <form>
                        <div className="field">
                            <div className="control">
                                <input className="input is-large" type="email" placeholder="Enter your email" autoFocus=""
                                value={email} onChange={(e) => setEmail(e.target.value)} required/>
                            </div>
                        </div>
                        <div className="field">
                            <div className="control">
                                <input className="input is-large" type="password" placeholder="Enter your password"
                                value={password} onChange={(e) => setPassword(e.target.value)} required/>
                            </div>
                        </div>
                        <div className="field"> <ErrorMessage message={errorMessage} /><br /></div>
                        <button className="button is-block is-info is-large is-fullwidth" type="submit">Login <i className="fa fa-sign-in" aria-hidden="true"></i></button>
                    </form>
                </div>
                <p className="has-text-grey">
                    <a href="./register">Don't have an account? &nbsp;·&nbsp; Register</a>
                </p>
            </div>
        </div>
    </div>
  );
};