import React, { useContext, useEffect, useState } from "react"
import moment from "moment";
import ErrorMessage from "../ErrorMessage";
import ImageModal from "./ImageModal";
import { UserContext } from "../../context/UserContext";

export const ImagesTable = () => {
    const [token] = useContext(UserContext);
    const [images, setImages] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);
    //const [id, setId] = useState(null);

    /*const handleUpdate = async (id) => {
        setId(id);
        setActiveModal(true);
        //getPersons(); why wasnt this here ?? doesitworks ??
    };*/

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
        if (!response.ok) {
            setErrorMessage("Something went wrong. Couldn't load the images");
        } else {
            const data = await response.json();
            setImages(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getImages();
    }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getImages();
        //setId(null);
    };

    return <>
        <ImageModal
            active={activeModal}
            handleModal={handleModal}
            token={token}
        //id={id}
        />
        <button className="button is-fullwidth mb-5 is-primary"
            onClick={() => setActiveModal(true)}>Add a new Image</button>
        <ErrorMessage message={errorMessage} />
        {loaded && images ? (
            <table className="table is-fullwidth">
                <thead>
                    <tr>
                        {/*<th>Name</th>*/}
                        <th>Images</th>
                        <th>Last Updated</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {images.map((img) => (
                        <tr key={img.id}>
                            {/*<td>{img.name}</td>*/}
                            <td>{JSON.parse(img.image).length > 0 ? JSON.parse(img.image).map((imageObj, i) => {
                                return (
                                    <div key={i}>
                                        <img width="50" src={imageObj} alt="" />
                                    </div>
                                );
                            })
                                : null}</td>
                            <td>{moment(img.date_last_updated).format("MMM Do YY")}</td>
                            <td>
                                {/*<button className="button mr-2 is-info is-light"
                                    onClick={() => handleUpdate(img.id)} >Update</button>*/}
                                <button className="button mr-2 is-danger is-light"
                                    onClick={() => handleDelete(img.id)} >Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        ) : <p style={{ textAlign: "center" }}><br />Loading...</p>}</>
};
//export default ImagesTable;