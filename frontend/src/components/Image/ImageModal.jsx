import React, { useState } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import * as g from "../../Global";

export const ImageModal = ({ active, handleModal, token }) => {
    const [images, setImages] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");
    const [activeRefresher, setActiveRefresher] = useState(active);

    async function uploadImages(e) {
        if (e.target.files && e.target.files.length > 0) {
            for (let i = 0; i < e.target.files.length; i++) {
                var file = e.target.files[i];
                var name = file.name.replace(/\.[^/.]+$/, "");
                var img = await g.fileToDataUri(file);
                const fullImg = { name: name, image: img }
                var imgs = images
                imgs.push(fullImg);
                setImages(imgs)
            }
            setActiveRefresher(!activeRefresher);
        }
    }

    function cleanFormData() {
        setImages([]);
        setErrorMessage("");
    }

    function handleClose() {
        cleanFormData();
        setActiveRefresher(false);
        handleModal();
    }

    function handleCreateImages(e) {
        e.preventDefault();
        images.map(async (img) => {
            await g.fetchData("POST", "application/json", token, "images", setErrorMessage,
                "Something went wrong when creating image", undefined, undefined, JSON.stringify({ name: img.name, image: img.image, }));
        })
        if (errorMessage !== "") handleClose();
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
                            {images.length > 0 && images.map((img, i) => {
                                return <div key={img.name + i}>
                                    <img width="250" src={img.image} alt={img.name} />
                                    <button class="delete" onClick={() => setImages(images.filter(x => x !== img))} />
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