import React, { useState } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import * as g from "../../Global";

export const ImageModal = ({ active, handleModal, token }) => {
    const [name, setName] = useState("");
    const [image, setImage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    async function uploadImage(e) {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            setName(file.name.replace(/\.[^/.]+$/, ""));
            setImage(await g.fileToDataUri(file));
        }
        e.target.value = '';
    }

    function cleanFormData() {
        setName("");
        setImage("");
        setErrorMessage("");
    }

    function handleClose() {
        cleanFormData();
        handleModal();
    }

    async function handleCreateImage(e) {
        e.preventDefault();
        await g.fetchData("POST", "application/json", token, "images", setErrorMessage,
            "Something went wrong when creating image", undefined, handleClose, JSON.stringify({ name: name, image: image, }));
    }

    return <div className={`modal ${active && "is-active"}`}>
        <div className="modal-background" onClick={handleClose}></div>
        <div className="modal-card">
            <header className="modal-card-head has-background-primary-light">
                <h1 className="modal-card-title">{"Create Image"}</h1>
                <button class="delete is-large" onClick={handleClose} />
            </header>
            <section className="modal-card-body">
                <form>
                    <div className="field">
                        <label className="label">Image</label>
                        <div className="control">
                            <input type="file" placeholder="Image" onChange={uploadImage} className="input" required />
                            {image && <div key={0}>
                                <img width="150" src={image} alt="" />
                            </div>}
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                </form>
            </section>
            <footer className="modal-card-foot has-background-primary-light">
                <button className="button is-primary" onClick={handleCreateImage}>Add</button>
                <button className="button" onClick={handleClose}>Cancel</button>
            </footer>
        </div>
    </div>
};