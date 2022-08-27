import React, { useContext, useEffect, useState } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import { ImageModal } from "./ImageModal";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";
import { ImageFaceModal } from "./ImageFaceModal";

export const ImagesTable = () => {
    const [token] = useContext(UserContext);
    const [images, setImages] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);
    const [activeFaceModal, setActiveFaceModal] = useState(false);
    const [faceModalID, setFaceModalID] = useState(0);
    const [faceModalName, setFaceModalName] = useState("");

    async function handleDelete(id) {
        await g.fetchData("DELETE", "application/json", token, `images/${id}`, setErrorMessage,
            "Failed to delete image", undefined, getImages);
    }

    async function getImages() {
        await g.fetchData("GET", "application/json", token, "images", setErrorMessage,
            "Something went wrong. Couldn't load the images", setImages, () => setLoaded(true));
    }

    useEffect(() => {
        getImages();
    }, []);// eslint-disable-line react-hooks/exhaustive-deps

    function handleModal() {
        setActiveModal(!activeModal);
        getImages();
    }

    function handleFaceModal() {
        setActiveFaceModal(!activeFaceModal);
        setFaceModalID(0);
        setFaceModalName("");
    }

    return <>
        <ImageModal active={activeModal} handleModal={handleModal} token={token} />
        <ImageFaceModal active={activeFaceModal} handleModal={handleFaceModal} ID={faceModalID} name={faceModalName} />
        <section className="container">
            <div className="columns">
                <div className="column">
                    <button className="button is-fullwidth is-primary" onClick={() => setActiveModal(true)}
                    >Add a new image</button>
                </div>
            </div>
        </section>
        <br /><ErrorMessage message={errorMessage} /><br />
        {(loaded && images) ? (
            <section className="container">
                <div className="columns is-multiline">
                    {images.map((img) => (
                        <div className="column is-4" key={img.id} onClick={() => {
                            setFaceModalID(img.id);
                            setFaceModalName(img.name);
                            setActiveFaceModal(true);
                        }}>
                            <div className="card is-shady">
                                <div className="card-image">
                                    <figure className="image is-3by2">
                                        <img src={img.image} alt="" />
                                    </figure>
                                    <div className="card-content is-overlay is-clipped">
                                        <span className="tag is-info">{img.name}</span>
                                    </div>
                                </div>
                                <footer className="card-footer">
                                    <button className="button is-danger card-footer-item"
                                        onClick={() => handleDelete(img.id)} >Delete</button>
                                </footer>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        ) : <section className="container">
            <div>
                <p style={{ textAlign: "center" }}><br />Loading your images</p>
                <progress className="progress is-small is-primary" max="100">99%</progress>
            </div>
        </section>
        }</>
};