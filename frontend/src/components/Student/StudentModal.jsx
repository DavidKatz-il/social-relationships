import React, { useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage"
import * as g from "../../Global";

export const StudentModal = ({ active, handleModal, token, id }) => {
  const [name, setName] = useState("");
  const [images, setImages] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  /*const fileToDataUri = (image) => {
    return new Promise((res) => {
      const reader = new FileReader();
      reader.addEventListener('load', () => { res(reader.result); });
      reader.readAsDataURL(image);
    });
  };*/

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
    await g.fetchData("GET", "application/json", token, `/api/persons/${id}`, setErrorMessage,
      "Could not get the student", setData, undefined, undefined);
    /*const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/api/persons/${id}`, requestOptions);
    const data = await response.json();
    if (!response.ok) {
      if (data && data.detail) setErrorMessage(data.detail);
      else setErrorMessage("Could not get the student");
    }
    else {
      setName(data.name);
      setImages(JSON.parse(data.images));
    }*/
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
    const body = JSON.stringify({
      name: name,
      images: JSON.stringify(images),
    });
    await g.fetchData("POST", "application/json", token, "/api/persons", setErrorMessage,
      "Something went wrong when creating student", undefined, handleClose, body);
    /*const requestOptions = {
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
    if (!response.ok) {
      const data = await response.json();
      if (data && data.detail) setErrorMessage(data.detail);
      else setErrorMessage("Something went wrong when creating student");
    }
    else handleClose();*/
  }

  async function handleUpdateStudent(e) {
    e.preventDefault();
    const body = JSON.stringify({
      name: name,
      images: JSON.stringify(images),
    });
    await g.fetchData("PUT", "application/json", token, `/api/persons/${id}`, setErrorMessage,
      "Something went wrong when updating student", undefined, handleClose, body);
    /*const requestOptions = {
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
    if (!response.ok) {
      const data = await response.json();
      if (data && data.detail) setErrorMessage(data.detail);
      else setErrorMessage("Something went wrong when updating student");
    }
    else handleClose();*/
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