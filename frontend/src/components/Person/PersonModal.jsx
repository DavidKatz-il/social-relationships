import React, { useEffect, useState } from "react";
import { ErrorMessage } from "../ErrorMessage"

export const PersonModal = ({ active, handleModal, token, id }) => {
  const [name, setName] = useState("");
  const [images, setImages] = useState([]);
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
      const newImagesPromises = [];
      for (let i = 0; i < e.target.files.length; i++)
        newImagesPromises.push(fileToDataUri(e.target.files[i]));
      const newImages = await Promise.all(newImagesPromises);
      setImages(newImages);
    }
    e.target.value = '';
  };

  const getPerson = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/api/persons/${id}`, requestOptions);
    if (!response.ok)
      setErrorMessage("Could not get the person");
    else {
      const data = await response.json();
      setName(data.name);
      setImages(JSON.parse(data.images));
    }
  };

  useEffect(() => {
    if (id) getPerson();
  }, [id, token]);

  const cleanFormData = () => {
    setName("");
    setImages([]);
    setErrorMessage("");
  };

  const handleClose = () => {
    cleanFormData();
    handleModal();
  }

  const handleCreatePerson = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        name: name,
        images: JSON.stringify(images),
      }),
    };
    console.log(requestOptions);
    const response = await fetch("/api/persons", requestOptions);
    if (!response.ok) setErrorMessage("Something went wrong when creating person");
    else handleClose();
  };

  const handleUpdatePerson = async (e) => {
    e.preventDefault();
    const requestOptions = {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify({
        name: name,
        images: JSON.stringify(images),
      }),
    };
    const response = await fetch(`/api/persons/${id}`, requestOptions);
    if (!response.ok) setErrorMessage("Something went wrong when updating person");
    else handleClose();
  };

  return <div className={`modal ${active && "is-active"}`}>
    <div className="modal-background" onClick={handleClose}></div>
    <div className="modal-card">
      <header className="modal-card-head has-background-primary-light">
        <h1 className="modal-card-title">{id ? "Update Person" : "Create Person"}</h1>
      </header>
      <section className="modal-card-body">
        <form>
          <div className="field">
            <label className="label">Name</label>
            <div className="control">
              <input type="text" placeholder="Enter name" value={name} required={true}
                onChange={(e) => setName(e.target.value)} className="input" />
            </div>
          </div>
          <div className="field">
            <label className="label">Images</label>
            <div className="control">
              <input type="file" placeholder="Images" multiple onChange={uploadImage}
                className="input" required={true} />
              {images.length > 0 ? images.map((imageObj, i) => {
                return <div key={i}>
                  <img width="50" src={imageObj} alt="" />
                </div>
              }) : null}
            </div>
          </div>
          <ErrorMessage message={errorMessage} />
        </form>
      </section>
      <footer className="modal-card-foot has-background-primary-light">
        {id ? <button className="button is-info" onClick={handleUpdatePerson}>Update</button>
          : <button className="button is-primary" onClick={handleCreatePerson}>Add</button>}
        <button className="button" onClick={handleClose}>Cancel</button>
      </footer>
    </div>
  </div>
};