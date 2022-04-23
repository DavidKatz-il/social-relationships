import React, { useEffect, useState } from "react"
import ErrorMessage from "../ErrorMessage";

const ImageModal = ({ active, handleModal, token }) => {
    const [name, setName] = useState("");
    const [image, setImage] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const fileToDataUri = (image) => {
        return new Promise((res) => {
            const reader = new FileReader();
            reader.addEventListener('load', () => { res(reader.result); });
            reader.readAsDataURL(image);
        });
    };

    const uploadImage = async (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            setName(file.name);
            setImage(await fileToDataUri(file));
        }
        e.target.value = '';
    };

    /*useEffect(() => {
        if (id) getPerson();
    }, [id, token]);*/

    const cleanFormData = () => {
        setName("");
        setImage("");
        setErrorMessage("");
    };

    const handleClose = () => {
        cleanFormData();
        handleModal();
    };

    /*const getImage = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
        };
        const response = await fetch(`/api/images/${id}`, requestOptions);
        if (!response.ok)
            setErrorMessage("Could not get the person");
        else {
            const data = await response.json();
            setName(data.name);
            setImages(JSON.parse(data.images));
        }
    };*/

    const handleCreateImage = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
            body: JSON.stringify({
                name: name,
                image: image,
            }),
        };
        const response = await fetch("/api/images", requestOptions);
        if (!response.ok) setErrorMessage("Something went wrong when creating image");
        else handleClose();
    };

    return <div className={`modal ${active && "is-active"}`}>
        <div className="modal-background" onClick={handleClose}></div>
        <div className="modal-card">
            <header className="modal-card-head has-background-primary-light">
                <h1 className="modal-card-title">{"Create Image"}</h1>
            </header>
            <section className="modal-card-body">
                <form>
                    {/*<div className="field">
                        <label className="label">Name</label>
                        <div className="control">
                            <input type="text" placeholder="Enter name" value={name} required={true}
                                onChange={(e) => setName(e.target.value)} className="input" />
                        </div>
                    </div>*/}
                    <div className="field">
                        <label className="label">Image</label>
                        <div className="control">
                            <input type="file" placeholder="Image" onChange={uploadImage}
                                className="input" required={true} />
                            {image.length > 0 ? 
                                <div key={0}>
                                    <img width="50" src={image} alt="" />
                                </div>
                            : null}
                        </div>
                    </div>
                    <div className="errorMessage"><ErrorMessage message={errorMessage} /></div>
                </form>
            </section>
            <footer className="modal-card-foot has-background-primary-light">
                {//id ? <button className="button is-info" onClick={handleUpdatePerson}>Update</button>:
                    <button className="button is-primary" onClick={handleCreateImage}>Add</button>}
                <button className="button" onClick={handleClose}>Cancel</button>
            </footer>
        </div>
    </div>

    //return <p>ImageModal</p>
};
export default ImageModal;