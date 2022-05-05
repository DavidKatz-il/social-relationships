import React, { useContext, useEffect, useState } from "react"
import { ErrorMessage } from "../ErrorMessage";
import { ImageModal } from "./ImageModal";
import { UserContext } from "../../context/UserContext";

export const ImagesTable = () => {
    const [token] = useContext(UserContext);
    const [images, setImages] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);

    const handleDelete = async (id) => {
        const requestOptions = {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
        };
        const response = await fetch(`/api/images/${id}`, requestOptions);
        if (!response.ok) setErrorMessage("Failed to delete image");
        getImages();
    };

    const getImages = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
        };
        const response = await fetch("/api/images", requestOptions);
        if (!response.ok) setErrorMessage("Something went wrong. Couldn't load the images");
        else {
            const data = await response.json();
            setImages(data);
            setLoaded(true);
        }
    };

    useEffect(() => { getImages(); }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getImages();
    };
    
    return <>
        <ImageModal active={activeModal} handleModal={handleModal} token={token} />
        <section className="container">
            <div className="columns">
                <div className="column">
                    <div className="card">
                        <div className="card-content">
                            <div className="content">
                                <div className="control">
                                <button className="button is-fullwidth is-primary"
                                onClick={() => setActiveModal(true)}>Add a new image</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="column">
                    <div className="card">
                        <div className="card-content">
                            <div className="content">
                                <div className="control">
                                    <input className="input is-fullwidth" placeholder="Search images" type="search"/>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <br></br>
        <ErrorMessage message={errorMessage} />
        <br></br>
        {(loaded && images) ? (
        <section className="container">
            <div className="columns is-multiline">
                {images.map((img) => (
                    <div className="column is-4" key={img.id}>
                        <div className="card is-shady">
                            <div className="card-image">
                                <figure className="image is-3by2">
                                    <img src={img.image} alt=""/>
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