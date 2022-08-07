import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const MostAppearance = (ID) => {
  const [state, setState] = useState(null);
  const [token] = useContext(UserContext);
  const [errorMessage, setErrorMessage] = useState("");
  const [loaded, setLoaded] = useState(false);

  async function GetData() {
    setLoaded(false);
    await g.fetchData("GET", "application/json", token, "report/" + ID.valueOf().ID, setErrorMessage,
      "Something went wrong. Couldn't load the report", setState);
    setLoaded(true);
  }

  useEffect(() => {
    GetData();
  }, []);// eslint-disable-line react-hooks/exhaustive-deps

  return <section className="container">
    <br /><ErrorMessage message={errorMessage} /><br />
    {(loaded && state) ?
      <>
        <h1 className="title" style={{ textAlign: "center" }}>{state.name}</h1>
        <table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth" style={{ textAlign: "center" }}>
          <thead>
            <tr>{Object.values(state.info[0]).map((v) => (
              <th>{v}</th>
            ))}
            </tr>
          </thead>
          <tbody>
            <tr>{Object.values(state.info[1]).map((v) => (
              <td>{v}</td>
            ))}
            </tr>
          </tbody>
        </table>
      </>
      :
      <div>
        <p style={{ textAlign: "center" }}><br />Loading your data</p>
        <progress className="progress is-small is-primary" max="100">99%</progress>
      </div>
    }
  </section >
}