import React from 'react';

import './css/main.css';
import Table from './table.js';
import ManualAdditionPopUp from './manualAdditionPopUp.js';
import Log from './Model/log.js';


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchLog: [],
            manualAddition: false,
        }
    }

    toggleManualAddition() {
        const manualAddition = this.state.manualAddition;
        this.setState({
            manualAddition: !manualAddition,
        });
    }

    handleChange(event) {
        console.log(event);
    }



    render() {
        const { searchLog, manualAddition } = this.state;
        const entry = {
            date: null,
            employerName: null,
            jobTitle: null,
            contactInfo: null,
        };
        
        return (
            <div id="container">
                <nav>
                    <div id="title-container">
                        <h1>JOB LOGGER</h1> 
                    </div>
                    <div id="contact-info">
                        <a href="https://www.linkedin.com/in/kyuhyunp/">LinkedIn</a>
                        <a href="kyuhyunpark.official@gmail.com">Email</a>
                    </div>
                </nav>

                <div id="content-container">
                    <section id="search-bar">
                        <div className="button-container"> 
                            <button onClick={() => this.toggleManualAddition()}>Manually Add Job</button>
                        </div>
                        <div className="button-container"> 
                            <button>Query Week</button>
                        </div>
                    </section>
                    <section id="job-list">
                        <p>Below is a list of the job search contacts.</p>
                        <h3>Job Search Log</h3>

                        <Table/>
                    </section>
                </div>
                <ManualAdditionPopUp 
                    trigger={manualAddition} 
                    date={entry.date} 
                    employerName={entry.employerName}
                    jobTitle={entry.jobTitle}
                    contactInfo={entry.contactInfo}
                    handleChange={() => this.handleChange()}
                >
                </ManualAdditionPopUp> 
            </div>
        );
    }
}

export default Main;