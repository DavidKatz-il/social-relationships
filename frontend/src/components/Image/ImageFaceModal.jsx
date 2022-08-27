import React, { useEffect, useState, useContext } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const ImageFaceModal = ({ active, handleModal, ID, name }) => {
    const [token] = useContext(UserContext);
    const [image, setImage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [myID, setMyID] = useState(ID);
    const [activeRefresher, setActiveRefresher] = useState(active);

    function cleanFormData() {
        setImage("");
        setErrorMessage("");
    }

    function handleClose() {
        cleanFormData();
        handleModal();
    }

    function handleSetImage(data) {
        setImage(data.image)
    }

    async function getImage() {
        await g.fetchData("GET", "application/json", token, "images_faces/" + ID, setErrorMessage,
            "Something went wrong when getting image", handleSetImage);
        setActiveRefresher(!activeRefresher);
    }

    useEffect(() => {
        setMyID(ID);
        setActiveRefresher(active);
        if (ID > 0) getImage();
    }, []);// eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        setMyID(ID);
        setActiveRefresher(active);
        if (ID > 0) getImage();
    }, [ID]);


    if (ID !== myID) {
        setMyID(ID);
        if (ID > 0) getImage();
    }

    return <div className={`modal ${active && "is-active"}`}>
        <div className="modal-background" onClick={handleClose}></div>
        <div className="modal-card">
            <header className="modal-card-head has-background-primary-light">
                <h1 className="modal-card-title">{name}</h1>
                <button class="delete is-large" onClick={handleClose} />
            </header>
            <section className="modal-card-body">
                <ErrorMessage message={errorMessage} />
                {(image) ? <img src={image} alt="" />
                : 
                <div>
                    <p style={{ textAlign: "center" }}><br />Loading the image</p>
                    <progress className="progress is-small is-primary" max="100">99%</progress>
                </div>
                }
                
            </section>
            <footer className="modal-card-foot has-background-primary-light">
                <button className="button" onClick={handleClose}>Close</button>
            </footer>
        </div>
    </div>
};