import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage"
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const Home = () => {
    const [token] = useContext(UserContext);
    const [id, setId] = useState("");
    const [email, setEmail] = useState("");
    const [teacherName, setTeacherName] = useState("");
    const [schoolName, setSchoolName] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    function setData(data) {
        if (data) {
            setId(data.id);
            setEmail(data.email);
            setTeacherName(data.teacher_name);
            setSchoolName(data.school_name);
        }
    }
    
    async function getUser() {
        await g.fetchData("GET", "application/json", token, 'user', setErrorMessage,
          "Could not get the user", setData, undefined, undefined);
    };
    
    useEffect(() => {
        getUser();
    }, ""); // eslint-disable-line react-hooks/exhaustive-deps
    
    return <>
        {(token) ? <>
            <div className="container">
                <div>
                    <br />
                    <ErrorMessage message={errorMessage} />
                    <br />    
                </div>
                <div className="columns">
                    <div className="column">
                        <section className="hero is-primary welcome is-small">
                            <div className="hero-body">
                                <div className="container">
                                    <h1 className="title"> Hello, {teacherName} from {schoolName}. </h1>
                                    <h2 className="subtitle"> You are welcome to the platform that helps you track the social relationships of your students. </h2>
                                </div>
                            </div>
                        </section>
                        <section className="info-tiles">
                            <div className="tile is-parent has-text-centered">
                                <article className="tile is-child box">
                                    <p className="title">4</p>
                                    <p className="subtitle">Students</p>
                                </article>
                            </div>
                            <div className="tile is-parent has-text-centered">
                                <article className="tile is-child box">
                                    <p className="title">12</p>
                                    <p className="subtitle">Images</p>
                                </article>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </> : <>
            <div className="columns">
                <div className="column">
                    <section className="hero is-primary welcome is-small">
                        <div className="hero-body">
                            <div className="container">
                                <h1 className="title"> Hello, you need to register to continue. </h1>
                                <h2 className="subtitle"> You are welcome to the platform that helps you track the social relationships of your students. </h2>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </>
        }
    </>
};