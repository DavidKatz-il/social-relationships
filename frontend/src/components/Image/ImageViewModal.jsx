/*import React, { useState } from "react"
import { ErrorMessage } from "../Info/ErrorMessage";
import * as g from "../../Global";

export const ImageViewModal = ({ active, id, token, handleDelete }) => {

    return <div className={`modal ${active && "is-active"}`}>
        <div className="modal-background" onClick={handleClose}></div>
        <div className="modal-card">
            <header className="modal-card-head has-background-primary-light">
                <h1 className="modal-card-title">{"Create Image"}</h1>
            </header>
            <section className="modal-card-body">
                <form>
                    <div className="field">
                        <label className="label">Image</label>
                        <div className="control">
                            <input type="file" placeholder="Image" onChange={uploadImage} className="input" required />
                            {image && <div key={0}>
                                <img width="150" src={image} alt="" />
                            </div>}
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                </form>
            </section>
            <footer className="modal-card-foot has-background-primary-light">
                <button className="button is-primary" onClick={handleCreateImage}>Add</button>
                <button className="button" onClick={handleClose}>Cancel</button>
            </footer>
        </div>
    </div>
};*/