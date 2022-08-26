import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../../context/UserContext";
import { ErrorMessage } from "../Info/ErrorMessage";
import logo from '../../logo.png';
import * as g from "../../Global";

export const EditUser = () => {
    const [email, setEmail] = useState("");
    const [emailChanged, setEmailChanged] = useState(false);
    const [teacherName, setTeacherName] = useState("");
    const [teacherNameChanged, setTeacherNameChanged] = useState(false);
    const [schoolName, setSchoolName] = useState("");
    const [schoolNameChanged, setSchoolNameChanged] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordChanged, setPasswordChanged] = useState(false);
    const [confirmationPassword, setConfirmationPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [token] = useContext(UserContext);

    async function submitUser() {
        const body = JSON.stringify({
            email: (emailChanged && email !== "") ? email : undefined,
            hashed_password: (passwordChanged && password !== "") ? password : undefined,
            teacher_name: (teacherNameChanged && teacherName !== "") ? teacherName : undefined,
            school_name: (schoolNameChanged && schoolName !== "") ? schoolName : undefined
        });
        await g.fetchData("PUT", "application/json", token, "users", setErrorMessage, "", undefined, fetchUser, body);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        if ((password === confirmationPassword && password.length > 5) || (!passwordChanged) || password === "") submitUser();
        else setErrorMessage("Ensure that the passwords match and greater than 5 characters");
    };

    function getUser(user) {
        if (user) {
            setEmail(user.email);
            setTeacherName(user.teacher_name);
            setSchoolName(user.school_name)
        }
    }

    const fetchUser = async () => {
        await g.fetchData("GET", "application/json", token, "user", undefined, "", getUser);
    };

    useEffect(() => {
        fetchUser();
    }, [])

    return (
        <div className="hero-body">
            <div className="container has-text-centered">
                <div className="column is-4 is-offset-4">
                    <div className="box" onSubmit={handleSubmit}>
                        <figure className="avatar">
                            <img src={logo} alt="Logo" />
                        </figure>
                        <form>
                            <div className="field">
                                <div className="control">
                                    <input className="input is-large" type="email" placeholder="Enter your email" autoFocus=""
                                        value={email} onChange={(e) => {
                                            setEmail(e.target.value);
                                            setEmailChanged(true);
                                        }} />
                                </div>
                            </div>
                            <div className="field">
                                <div className="control">
                                    <input className="input is-large" type="text" placeholder="Enter your name" autoFocus=""
                                        value={teacherName} onChange={(e) => {
                                            setTeacherName(e.target.value);
                                            setTeacherNameChanged(true);
                                        }} />
                                </div>
                            </div>
                            <div className="field">
                                <div className="control">
                                    <input className="input is-large" type="text" placeholder="Enter the school name" autoFocus=""
                                        value={schoolName} onChange={(e) => {
                                            setSchoolName(e.target.value);
                                            setSchoolNameChanged(true);
                                        }} />
                                </div>
                            </div>
                            <div className="field">
                                <div className="control">
                                    <input className="input is-large" type="password" placeholder="Enter your password"
                                        value={password} onChange={(e) => {
                                            setPassword(e.target.value);
                                            setPasswordChanged(true);
                                        }} />
                                </div>
                            </div>
                            <div className="field">
                                <div className="control">
                                    <input className="input is-large" type="password" placeholder="Enter your password again"
                                        value={confirmationPassword} onChange={(e) => {
                                            setConfirmationPassword(e.target.value);
                                            setPasswordChanged(true);
                                        }} />
                                </div>
                            </div>
                            <div className="field">
                                <ErrorMessage message={errorMessage} />
                                <br />
                            </div>
                            <button className="button is-block is-info is-large is-fullwidth" type="submit">
                                <span>Save </span>
                                <i className="fa fa-save" aria-hidden="true" />
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};