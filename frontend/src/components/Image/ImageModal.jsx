import React, { useState } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import * as g from "../../Global";

export const ImageModal = ({ active, handleModal, token }) => {
    //const [name, setName] = useState("");
    const [images, setImages] = useState([]);
    //const [image, setImage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    async function uploadImages(e) {
        if (e.target.files && e.target.files.length > 0) {
            for (let i = 0; i < e.target.files.length; i++) {
                //e.target.files.map(async (file) => {
                var file = e.target.files[i];
                var name = file.name.replace(/\.[^/.]+$/, "");
                var img = await g.fileToDataUri(file);
                const fullImg = { name: name, image: img }
                var imgs = images//.push(fullImg);
                imgs.push(fullImg);
                setImages(imgs)
            }

            //const file = e.target.files;
            //setName(file.name.replace(/\.[^/.]+$/, ""));
            //setImage(await g.fileToDataUri(file));

            //e.target.value = '';
        }
    }

    function cleanFormData() {
        //setName("");
        setImages([]);
        setErrorMessage("");
    }

    function handleClose() {
        cleanFormData();
        handleModal();
    }

    function handleCreateImages(e) {
        e.preventDefault();
        images.map(async (img) => {
            await g.fetchData("POST", "application/json", token, "images", setErrorMessage,
                "Something went wrong when creating image", undefined, undefined, JSON.stringify({ name: img.name, image: img.image, }));
        })
        handleClose();
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
                            <input type="file" placeholder="Image" onChange={uploadImages} className="input" required multiple />
                            {images.map((img) => {
                                <div key={0}>
                                    <img width="150" src={img.image} alt={img.name} />
                                </div>
                            })}
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                </form>
            </section>
            <footer className="modal-card-foot has-background-primary-light">
                <button className="button is-primary" onClick={handleCreateImages}>Add</button>
                <button className="button" onClick={handleClose}>Cancel</button>
            </footer>
        </div>
    </div>
};