import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage"
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";
import social_relationships from "../../social_relationships.png";

export const Home = () => {
    const [token] = useContext(UserContext);
    const [teacherName, setTeacherName] = useState("");
    const [schoolName, setSchoolName] = useState("");
    const [studentsCount, setStudentsCount] = useState("");
    const [imagesCount, setImagesCount] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    function setUserData(data) {
        if (data) {
            setTeacherName(data.teacher_name);
            setSchoolName(data.school_name);
        }
    }
    function setUserInfoData(data) {
        if (data) {
            setStudentsCount(data.students_count);
            setImagesCount(data.images_count);
        }
    }

    async function getUserData() {
        if (token !== 'null') {
            await g.fetchData("GET", "application/json", token, 'user', setErrorMessage, "Could not get the user", setUserData);
            await g.fetchData("GET", "application/json", token, 'user_info', setErrorMessage, "Could not get the user", setUserInfoData);
        }
    };

    useEffect(() => {
        getUserData();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    return <>
        <br /><ErrorMessage message={errorMessage} /><br />
        <div style={{ textAlign: "center" }}><img src={social_relationships} height="350" width="350" /></div>
        {(token) ? <>
            <div className="container">
                <div className="columns">
                    <div className="column">
                        <section className="hero is-primary welcome is-small">
                            <div className="hero-body">
                                <div className="container">
                                    <h1 className="title"> Hello, <b>{teacherName}</b> from <b>{schoolName}</b>. </h1>
                                    <h2 className="subtitle"> You are welcome to the platform that helps you track the social relationships of your students. </h2>
                                </div>
                            </div>
                        </section>
                        <section className="info-tiles">
                            <div className="tile is-parent has-text-centered">
                                <article className="tile is-child box">
                                    <p className="title">{studentsCount}</p>
                                    <p className="subtitle">Students</p>
                                </article>
                            </div>
                            <div className="tile is-parent has-text-centered">
                                <article className="tile is-child box">
                                    <p className="title">{imagesCount}</p>
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
                                <h1 className="title"> Please login or register to continue. </h1>
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