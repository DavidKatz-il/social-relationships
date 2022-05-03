import React, { useContext, useEffect, useState } from "react";
import moment from "moment";
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

  return (
    <>
      <PersonModal active={activeModal} handleModal={handleModal} token={token} id={id} />
      <div className="columns">
        <div className="column"></div>
        <button className="column button is-fullwidth mb-5 is-primary"
          onClick={() => setActiveModal(true)}>Add a new Person</button>
        <div className="column"></div>
      </div>
      <ErrorMessage message={errorMessage} />
      {(loaded && persons) ? (
        <table className="table is-fullwidth is-bordered is-hoverable is-striped" style={{ textAlign: "center" }}>
          <thead>
            <tr>
              <th width="25%">Name</th>
              <th >Images</th>
              <th width="15%">Last Updated</th>
              <th width="15%">Actions</th>
            </tr>
          </thead>
          <tbody>
            {persons.map((person) => (
              <tr key={person.id}>
                <td>{person.name}</td>
                <td>{JSON.parse(person.images).length > 0 ? JSON.parse(person.images).map((imageObj, i) => {
                  return (<img key={i} width="100" height="100" style={{ padding: 5 }} src={imageObj} />);
                })
                  : null}</td>
                <td>{moment(person.date_last_updated).format("MMM Do YY")}</td>
                <td>
                  <button
                    className="button mr-2 is-info is-light"
                    onClick={() => handleUpdate(person.id)}
                  >Update</button>
                  <button
                    className="button mr-2 is-danger is-light"
                    onClick={() => handleDelete(person.id)}
                  >Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : <p style={{ textAlign: "center" }}><br />Loading...</p>
      }</>
  );
};