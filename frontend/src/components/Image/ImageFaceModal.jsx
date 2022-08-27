import React, { useEffect, useState, useContext } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const ImageFaceModal = ({ active, handleModal, ID, name }) => {
    const [token] = useContext(UserContext);
    const [image, setImage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [myID, setMyID] = useState(ID.valueOf().ID);

    function cleanFormData() {
        setImage("");
        setErrorMessage("");
    }

    function handleClose() {
        cleanFormData();
        handleModal();
    }

    async function getImage() {
        await g.fetchData("GET", "application/json", token, "images/" + ID.valueOf().ID, setErrorMessage,
            "Something went wrong when getting image", setImage);
    }

    useEffect(() => {
        setMyID(ID.valueOf().ID);
        if (myID > 0) getImage();
    }, []);// eslint-disable-line react-hooks/exhaustive-deps

    if (ID.valueOf().ID !== myID) {
        setMyID(ID.valueOf().ID);
        if (myID > 0) getImage();
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
                <img src={image} alt="" />
            </section>
            <footer className="modal-card-foot has-background-primary-light">
                <button className="button" onClick={handleClose}>Close</button>
            </footer>
        </div>
    </div>
};