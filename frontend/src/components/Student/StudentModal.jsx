import React, { useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage"
import * as g from "../../Global";

export const StudentModal = ({ active, handleModal, token, id }) => {
  const [name, setName] = useState("");
  const [images, setImages] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  async function uploadImage(e) {
    if (e.target.files && e.target.files.length > 0) {
      const newImagesPromises = [];
      for (let i = 0; i < e.target.files.length; i++)
        newImagesPromises.push(g.fileToDataUri(e.target.files[i]));
      const newImages = await Promise.all(newImagesPromises);
      setImages(newImages);
    }
    e.target.value = '';
  };

  function setData(data) {
    if (data) {
      setName(data.name);
      setImages(JSON.parse(data.images));
    }
  }

  async function getStudent() {
    await g.fetchData("GET", "application/json", token, `/api/students/${id}`, setErrorMessage,
      "Could not get the student", setData, undefined, undefined);
  };

  useEffect(() => {
    if (id) getStudent();
  }, [id, token]);

  function cleanFormData() {
    setName("");
    setImages([]);
    setErrorMessage("");
  };

  function handleClose() {
    cleanFormData();
    handleModal();
  }

  async function handleCreateStudent(e) {
    e.preventDefault();
    const body = JSON.stringify({ name: name, images: JSON.stringify(images), });
    await g.fetchData("POST", "application/json", token, "/api/students", setErrorMessage,
      "Something went wrong when creating student", undefined, handleClose, body);
  }

  async function handleUpdateStudent(e) {
    e.preventDefault();
    const body = JSON.stringify({ name: name, images: JSON.stringify(images), });
    await g.fetchData("PUT", "application/json", token, `/api/students/${id}`, setErrorMessage,
      "Something went wrong when updating student", undefined, handleClose, body);
  }

  return <div className={`modal ${active && "is-active"}`}>
    <div className="modal-background" onClick={handleClose}></div>
    <div className="modal-card">
      <header className="modal-card-head has-background-primary-light">
        <h1 className="modal-card-title">{id ? "Update Student" : "Create Student"}</h1>
      </header>
      <section className="modal-card-body">
        <form>
          <div className="field">
            <label className="label">Name</label>
            <div className="control">
              <input type="text" placeholder="Enter name" value={name} required onChange={(e) => setName(e.target.value)} className="input" />
            </div>
          </div>
          <div className="field">
            <label className="label">Images</label>
            <div className="control">
              <input type="file" placeholder="Images" multiple onChange={uploadImage} className="input" required />
              {images && images.map((imageObj, i) => {
                return <div key={i}>
                  <img width="50" src={imageObj} alt="" />
                  <button class="delete" onClick={() => setImages(images.filter(x => x !== imageObj))} />
                </div>
              })}
            </div>
          </div>
          <ErrorMessage message={errorMessage} />
        </form>
      </section>
      <footer className="modal-card-foot has-background-primary-light">
        {id ? <button className="button is-info" onClick={handleUpdateStudent}>Update</button>
          : <button className="button is-primary" onClick={handleCreateStudent}>Add</button>}
        <button className="button" onClick={handleClose}>Cancel</button>
      </footer>
    </div>
  </div>
};