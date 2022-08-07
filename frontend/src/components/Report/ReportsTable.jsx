import React, { useContext, useState } from "react";
import { ErrorMessage } from "../Info/ErrorMessage";
import { UserContext } from "../../context/UserContext";
import * as g from "../../Global";
import { ReportModal } from "./ReportModal";
import { TotalAppearance } from "./TotalAppearance";
import { MostAppearance } from "./MostAppearance";

export const ReportsTable = () => {
    const [reports, setReports] = useState(null);
    const [activeTab, setActiveTab] = useState("", 0);
    const [token] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);

    async function handleCreate() {
        setLoaded(false);
        await g.fetchData("POST", "application/json", token, "reports", setErrorMessage,
            "Something went wrong. Couldn't create reports");
        handleGet();
    }

    async function handleGet() {
        setLoaded(false);
        await g.fetchData("GET", "application/json", token, "reports", setErrorMessage,
            "Something went wrong. Couldn't get reports", setReports);
        setLoaded(true);
    }

    return <>
        <aside className="menu" style={{ padding: 25, float: "right" }}>
            <ul className="menu-list">
                <li>
                    <button className="button is-fullwidth is-primary" onClick={handleCreate}>
                        <b>{(reports && reports.length) ? "Renew " : "Create "}Reports</b>
                    </button>
                </li>
            </ul>
            <p className="menu-label"><b>Reports</b></p>
            <ul className="menu-list">
                {reports && reports.map(r => {
                    return <li><a className={activeTab === r.name ? "is-active" : ""} onClick={() => setActiveTab(r.name,)} >{r.name}</a></li>
                })}
            </ul>
        </aside>
        <section className="container">
            <br /><ErrorMessage message={errorMessage} /><br />
            {(loaded && reports.length) ? <>{{
                "Total appear": <TotalAppearance />,
                "Most appearance": <MostAppearance ID={2} />,
                "Besties": <ReportModal />
            }[activeTab]}</>
                :
                <div>
                    <p style={{ textAlign: "center" }}><br />Loading your reports</p>
                    <progress className="progress is-small is-primary" max="100">99%</progress>
                </div>
            }
        </section>
    </>
}