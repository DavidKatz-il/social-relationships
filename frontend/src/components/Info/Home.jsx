import React from "react"

export const Home = () => {
    return (
        <div className="container">
            <div className="columns">
                <div className="column">
                    <section className="hero is-info welcome is-small">
                        <div className="hero-body">
                            <div className="container">
                                <h1 className="title"> Hello, TEACHER NAME from SCHOOL NAME. </h1>
                                <h2 className="subtitle"> Some welcome message! </h2>
                            </div>
                        </div>
                    </section>
                    <section className="info-tiles">
                        <div className="tile is-parent has-text-centered">
                            <article className="tile is-child box">
                                <p className="title">4</p>
                                <p className="subtitle">Students</p>
                            </article>
                        </div>
                        <div className="tile is-parent has-text-centered">
                            <article className="tile is-child box">
                                <p className="title">12</p>
                                <p className="subtitle">Images</p>
                            </article>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
};