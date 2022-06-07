import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const MatchFaces = () => {
    const [state, setState] = useState(null);
    const [token] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);

    async function GetData() {
        setLoaded(false);
        await g.fetchData("GET", "application/json", token, "get_match_faces", setErrorMessage,
            "Something went wrong. Couldn't load the report", setState);
        setLoaded(true);
    }

    useEffect(() => {
        GetData();
    }, []);// eslint-disable-line react-hooks/exhaustive-deps

    return <section className="container">
        <br /><ErrorMessage message={errorMessage} /><br />
        {(loaded && state) ? <>
            <table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth" style={{ textAlign: "center" }}>
                <thead><tr><th>MatchFaces</th></tr></thead>
                <tbody><tr>{Object.keys(state).map((key, i) => (
                    <><table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                        <thead><tr>
                            <th>Image Name</th>
                            <th>Students</th>
                        </tr></thead>
                        <tbody><tr>
                            <td>{key}</td>
                            <td>{Object.keys(state[key]).length}</td>
                        </tr><tr><td></td><td>{Object.keys(state[key]).map((innerkey, i) => (
                            <table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                                <thead><tr>
                                    <th>Student Name</th>
                                    <th>Location</th>
                                </tr></thead>
                                <tbody><tr>
                                    <td>{state[key][innerkey].student_name}</td>
                                    <td><table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                                        <thead><tr>
                                            <th>Top</th>
                                            <th>Right</th>
                                            <th>Bottom</th>
                                            <th>Left</th>
                                        </tr></thead>
                                        <tbody><tr>
                                            <td>{state[key][innerkey].location.top}</td>
                                            <td>{state[key][innerkey].location.right}</td>
                                            <td>{state[key][innerkey].location.bottom}</td>
                                            <td>{state[key][innerkey].location.left}</td>
                                        </tr></tbody>
                                    </table></td>
                                </tr></tbody>
                            </table>
                        ))}
                        </td></tr></tbody>
                    </table></>
                ))}
                </tr></tbody>
            </table>
            <div>{Object.keys(state).map((key, i) => (
                <p key={i}>
                    <span>Image Name:  <b>{key}</b>{" , "}</span>
                    <span>Students ({Object.keys(state[key]).length}): {Object.keys(state[key]).map((innerkey, i) => (
                        <p key={i}>
                            <span>Student Name: <b>{state[key][innerkey].student_name}</b>{" , "}</span>
                            <span>Location: ( Top: <b>{state[key][innerkey].location.top}</b> ,
                                Right: <b>{state[key][innerkey].location.right}</b> ,
                                Bottom: <b>{state[key][innerkey].location.bottom}</b> ,
                                Left: <b>{state[key][innerkey].location.left}</b> ).
                            </span>
                        </p>
                    ))}</span>
                </p>
            ))}</div>
        </>
            :
            <div>
                <p style={{ textAlign: "center" }}><br />Loading your data</p>
                <progress className="progress is-small is-primary" max="100">99%</progress>
            </div>
        }
    </section >
}