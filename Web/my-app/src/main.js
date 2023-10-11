import React from 'react';

import './css/main.css';
import Table from './table.js';
import ManualAdditionPopUp from './manualAdditionPopUp.js';


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchLogs: [],
            manualAddition: false,
        }
    }

    componentDidUpdate(_, prevState) {
        
        if (prevState.searchLogs !== this.state.searchLogs) {
            
        }
    }

    toggleManualAddition() {
        const manualAddition = this.state.manualAddition;
        this.setState({
            manualAddition: !manualAddition,
        });
    }

    /**
     * Alerts the user if the input is invalid
     * @param {*} inputs 
     */
    isInvalidInput(inputs) {
        const dateRegEx = /^\d{2}\/\d{2}\/\d{4}$/;
        if (!dateRegEx.test(inputs.date)) {
            return true;
        }

        // Parse the date parts to integers
        let parts = inputs.date.split("/");
        let day = parseInt(parts[1], 10);
        let month = parseInt(parts[0], 10);
        let year = parseInt(parts[2], 10);

        // Check the ranges of month and year
        if (year < 1000 || year > 3000) {
            return true;
        } 
        if (month === 0 || month > 12) {
            return true;
        }
            
        var monthLengthInDays = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

        // Adjust for leap years
        if (year % 400 === 0 || (year % 100 !== 0 && year % 4 === 0)) {
            monthLengthInDays[1] = 29;
        }

        // Check the range of the day
        if (day <= 0 || day > monthLengthInDays[month - 1]) {
            return true;
        }

        return false;
    }


    /**
     * Append inputs to searchLogs if it does not exist in searchLog
     * @param {*} searchLogs
     * @param {*} inputs 
     */
    appendUnique(searchLogs, inputs) {
        const idx = searchLogs.findIndex((log) => {
            return (
                log.date === inputs.date &&
                log.employerName === inputs.employerName &&
                log.jobTitle === inputs.jobTitle &&
                log.contactInfo === inputs.contactInfo
            );
        });

        if (idx === -1) {
            searchLogs.push(inputs);
        }
    }


    /**
     * Sets new state after the submission of the ManualAdditionPopUp form
     * @param {*} event 
     * @param {*} inputs 
     * @param {*} completed
     */
    submitManualAdditionFormAndReturnStatus(event, inputs) {
        event.preventDefault();

        if (this.isInvalidInput(inputs)) {
            alert("Please enter a valid date in the format MM/DD/YYYY");  
            return false;
        } 

        const searchLogs = this.state.searchLogs;
        this.appendUnique(searchLogs, inputs);
        console.log(searchLogs);

        this.setState ({
            searchLogs: searchLogs,
            manualAddition: false,
        });

        return true;
    }

    render() {
        const { searchLogs, manualAddition } = this.state;
        
        return (
            <div id="container">
                <nav>
                    <div id="title-container">
                        <h1>JOB LOGGER</h1> 
                    </div>
                    <div id="contact-info">
                        <a href="https://www.linkedin.com/in/kyuhyunp/" target="_blank" rel="noreferrer">LinkedIn</a>
                        <a href="https://github.com/kyuhyunp" target="_blank" rel="noreferrer">GitHub</a>
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
                        <h3>Job Search Logs</h3>

                        <Table searchLogs={searchLogs}/>
                    </section>
                </div>
                <ManualAdditionPopUp 
                    trigger={manualAddition} 
                    handleSubmit={(event, inputs) => 
                        this.submitManualAdditionFormAndReturnStatus(event, inputs)}
                    handleClose={() => this.toggleManualAddition()}
                >
                </ManualAdditionPopUp> 
            </div>
        );
    }
}

export default Main;