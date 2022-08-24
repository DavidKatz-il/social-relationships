import React, { useContext, useEffect, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";

export const ReportModal = (ID) => {
    const [state, setState] = useState(null);
    const [token] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [myID, setMyID] = useState(ID.valueOf().ID);
    const [isImages, setIsImages] = useState(false);
    const [images, setImages] = useState(null);

    async function GetData() {
        setLoaded(false);
        await g.fetchData("GET", "application/json", token, "report/" + ID.valueOf().ID, setErrorMessage,
            "Something went wrong. Couldn't load the report", setState);
        setLoaded(true);
    }

    function getImage() {
        const file = Object.values(state.info);
        setImages(file);
    }

    useEffect(() => {
        setMyID(ID.valueOf().ID);
        if (myID > 0) GetData();
    }, []);// eslint-disable-line react-hooks/exhaustive-deps

    if (ID.valueOf().ID !== myID) {
        setMyID(ID.valueOf().ID);
        if (myID > 0) GetData();
    }
    useEffect(() => {
        if (state) {
            const isimg = Object.keys(state.info).includes("images")
            setIsImages(isimg);
            if (isimg) getImage();
        }
    }, [state]);


    return <section >
        <br /><ErrorMessage message={errorMessage} /><br />
        {(loaded && state) ?
            <>
                <h1 className="title" style={{ textAlign: "center" }}>{state.name}</h1>
                {(isImages) ? (images) && <div style={{ textAlign: "center" }}>{
                    images.map((img) => {
                        return <img src={img} alt={"report " + img} />
                    })
                }</div>
                    :
                    <div>
                        <table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth" style={{ textAlign: "center" }}>
                            <thead><tr>{Object.values(state.info[0]).map((v) => (<th>{v}</th>))}</tr></thead>
                            <tbody>{Object.values(state.info).map((v, i) => {
                                if (i > 0) return <tr>{v.map((c) => (<td>{c}</td>))}</tr>
                            })}</tbody>
                        </table>
                    </div>}
            </>
            :
            <div>
                <p style={{ textAlign: "center" }}><br />Loading your data</p>
                <progress className="progress is-small is-primary" max="100">99%</progress>
            </div>
        }
    </section >
}