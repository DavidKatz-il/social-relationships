import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage";
import { StudentModal } from "./StudentModal";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const StudentsTable = () => {
  const [token] = useContext(UserContext);
  const [students, setStudents] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);
  const [activeModal, setActiveModal] = useState(false);
  const [id, setId] = useState(null);
  const [search, setSearch] = useState("");

  async function handleUpdate(id) {
    setId(id);
    setActiveModal(true);
  }

  async function handleDelete(id) {
    await g.fetchData("DELETE", "application/json", token, `students/${id}`,
      setErrorMessage, "Failed to delete student", undefined, getStudents);
  }

  async function getStudents() {
    await g.fetchData("GET", "application/json", token, "students", setErrorMessage,
      "Something went wrong. Couldn't load the students", setStudents, () => setLoaded(true));
  }

  useEffect(() => {
    getStudents();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    console.log("search: " + search);
    //search for students....
  }, [search]);

  function handleModal() {
    setActiveModal(!activeModal);
    getStudents();
    setId(null);
  }

  return <>
    <StudentModal active={activeModal} handleModal={handleModal} token={token} id={id} />
    <section className="container">
      <div className="columns">
        <div className="column">
          <button className="button is-fullwidth is-primary" onClick={() => setActiveModal(true)}>Add a new student</button>
        </div>
        <div className="column">
          <input className="input is-fullwidth" placeholder="Search students" type="search"
            value={search} onChange={e => setSearch(e.target.value)} />
        </div>
      </div>
    </section>
    <br />
    <ErrorMessage message={errorMessage} />
    <br />
    {(loaded && students) ? (
      <section className="container">
        <div className="columns is-multiline">
          {students.map((student) => (
            <div className="column is-2" key={student.id}>
              <div className="card is-shady">
                <div className="card-image">
                  <figure className="image is-3by2">
                    <img src={JSON.parse(student.images)[0]} alt={student.name} />
                  </figure>
                </div>
                <div className="card-content">
                  <div className="media-content">
                    <p className="title is-4">{student.name}</p>
                    <p className="subtitle is-6">Number of images: {JSON.parse(student.images).length}</p>
                  </div>
                </div>
              </div>
              <footer className="card-footer">
                <button className="button is-info card-footer-item" onClick={() => handleUpdate(student.id)} >Update</button>
                <button className="button is-danger card-footer-item" onClick={() => handleDelete(student.id)} >Delete</button>
              </footer>
            </div>
          ))}
        </div>
      </section>
    ) : <section className="container">
          <div>
            <p style={{ textAlign: "center" }}><br />Loading your students</p>
            <progress className="progress is-small is-primary" max="100">99%</progress>
          </div>
        </section>
    }</>
};