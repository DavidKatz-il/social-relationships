import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../ErrorMessage";
import { PersonModal } from "./PersonModal";
import { UserContext } from "../../context/UserContext";

export const PersonsTable = () => {
  const [token] = useContext(UserContext);
  const [persons, setPersons] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);

  const handleUpdate = async (id) => {
    setId(id);
    setActiveModal(true);
  };

  const handleDelete = async (id) => {
    const requestOptions = {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch(`/api/persons/${id}`, requestOptions);
    if (!response.ok) setErrorMessage("Failed to delete person");
    getPersons();
  };

  const getPersons = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    };
    const response = await fetch("/api/persons", requestOptions);
    if (!response.ok) {
      setErrorMessage("Something went wrong. Couldn't load the persons");
    } else {
      const data = await response.json();
      setPersons(data);
      setLoaded(true);
    }
  };

  useEffect(() => { getPersons(); }, []);

  const handleModal = () => {
    setActiveModal(!activeModal);
    getPersons();
    setId(null);
  };

  return <>
      <PersonModal active={activeModal} handleModal={handleModal} token={token} id={id} />
      <section className="container">
        <div className="columns">
            <div className="column">
                <div className="card">
                    <div className="card-content">
                        <div className="content">
                            <div className="control">
                            <button className="button is-fullwidth is-primary"
                            onClick={() => setActiveModal(true)}>Add a new student</button>
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
                                <input className="input is-fullwidth" placeholder="Search students" type="search"/>
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
      {(loaded && persons) ? (
      <section className="container">
        <div className="columns is-multiline">
          {persons.map((person) => (
            <div className="column is-2" key={person.id}>
              <div className="card is-shady">
                <div className="card-image">
                  <figure className="image is-3by2">
                    <img src={JSON.parse(person.images)[0]} alt=""/>
                  </figure>
                </div>
                <div className="card-content">
                  <div className="media-content">
                    <p className="title is-4">{person.name}</p>
                    <p className="subtitle is-6">Number of images: {JSON.parse(person.images).length}</p>
                  </div>
                </div>
                <div className="content">
                  
                </div>
                </div>
                  <footer className="card-footer">
                    <button className="button is-info card-footer-item"
                        onClick={() => handleUpdate(person.id)} >Update
                    </button>
                    <button className="button is-danger card-footer-item"
                        onClick={() => handleDelete(person.id)} >Delete
                    </button>
                  </footer>
                </div>
          ))}
        </div>
      </section>      
      ) : <p style={{ textAlign: "center" }}><br />Loading...</p>}</>
};