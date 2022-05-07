import React, { useContext, useEffect, useState } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import { ImageModal } from "./ImageModal";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const ImagesTable = () => {
    const [token] = useContext(UserContext);
    const [images, setImages] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);
    const [search, setSearch] = useState("");

    async function handleDelete(id) {
        await g.fetchData("DELETE", "application/json", token, `/api/images/${id}`, setErrorMessage,
            "Failed to delete image", undefined, getImages);
    }

    async function getImages() {
        await g.fetchData("GET", "application/json", token, "/api/images", setErrorMessage,
            "Something went wrong. Couldn't load the images", setImages, () => setLoaded(true));
    }

    useEffect(() => {
        getImages();
    }, []);

    useEffect(() => {
        console.log("search: " + search);
        //search for images....
    }, [search]);

    function handleModal() {
        setActiveModal(!activeModal);
        getImages();
    }

    return <>
        <ImageModal active={activeModal} handleModal={handleModal} token={token} />
        <section className="container">
            <div className="columns">
                <div className="column">
                    <button className="button is-fullwidth is-primary" onClick={() => setActiveModal(true)}
                    >Add a new image</button>
                </div>
                <div className="column">
                    <input className="input is-fullwidth" placeholder="Search images" type="search"
                        value={search} onChange={e => setSearch(e.target.value)} />
                </div>
            </div>
        </section>
        <br /><ErrorMessage message={errorMessage} /><br />
        {(loaded && images) ? (
            <section className="container">
                <div className="columns is-multiline">
                    {images.map((img) => (
                        <div className="column is-4" key={img.id}>
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
                                        onClick={() => handleDelete(img.id)} >Delete
                                    </button>
                                </footer>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
        ) : <p style={{ textAlign: "center" }}><br />Loading...</p>}</>
};