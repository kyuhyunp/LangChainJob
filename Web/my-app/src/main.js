import React from 'react';

import './css/main.css';
import Table from './table.js';
import ManualAdditionPopUp from './popUps/manual_addition_pop_up.js';
import SelectWeek from './popUps/select_week_pop_up.js'
import { QUERY_STATUS } from './query_status.js';
import LoadingScreen from './popUps/loading_screen_pop_up';


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            searchLogs: [],
            manualAddition: false,
            queryStatus: QUERY_STATUS.OFF,
            editEntry: null,
        }
    }

    toggleManualAddition() {
        const manualAddition = this.state.manualAddition;
        this.setState({
            manualAddition: !manualAddition,
        });
    }

    moveQueryStatusToSelect() {
        this.setState({
            queryStatus: QUERY_STATUS.SELECT,
        });
    }

    /**
     * Alerts the user if the input is invalid
     * @param {*} inputs 
     */
    isInvalidInput(inputs) {
        const dateRegEx = /^\d{2}-\d{2}-\d{4}$/;
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

    findUniqueIndex(searchLogs, inputs) {
        const idx = searchLogs.findIndex((log) => {
            return (
                log.date === inputs.date &&
                log.employerName === inputs.employerName &&
                log.jobTitle === inputs.jobTitle &&
                log.contactInfo === inputs.contactInfo
            );
        });

        return idx;
    }

    /**
     * Append inputs to searchLogs if it does not exist in searchLog
     * @param {*} searchLogs
     * @param {*} inputs 
     */
    appendUnique(searchLogs, inputs) {
        const idx = this.findUniqueIndex(searchLogs, inputs);

        if (idx === -1) {
            searchLogs.push(inputs);
        }
    }

    /**
     * Sets new state after the submission of the ManualAdditionPopUp form
     * @param {*} event 
     * @param {*} inputs 
     */
    submitManualAdditionFormAndReturnStatus(event, inputs) {
        event.preventDefault(); // prevents automatic browser refresh

        if (this.isInvalidInput(inputs)) {
            alert("Please enter a valid date in the format MM-DD-YYYY");  
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

    /**
     * Sets new state after the edit request of the ManualAdditionPopUp form
     * @param {*} event 
     * @param {*} inputs 
     */
    submitEditEntryFormAndReturnStatus(event, inputs) {
        event.preventDefault(); // prevents automatic browser refresh

        if (this.isInvalidInput(inputs)) {
            alert("Please enter a valid date in the format MM-DD-YYYY");  
            return false;
        } 

        const editEntry = this.state.editEntry;
        const searchLogs = this.state.searchLogs;

        if (this.findUniqueIndex(searchLogs, inputs) !== -1) {
            alert("This entry already exists in the database");
            return false;
        }

        searchLogs[editEntry] = inputs;
        console.log(searchLogs);

        this.setState ({
            searchLogs: searchLogs,
            manualAddition: false,
            editEntry: null,
        });

        return true;
    }



    /**
     * 
     * 
     * 
     * @param {*} data: json formatted string 
     * (list of dictionary with keys: date, employerName, jobTitle, contactInfo)
     */
    saveLogs(data) {
        const logs = JSON.parse(data);
        console.log(logs);

        const searchLogs = this.state.searchLogs;
        logs.forEach((log) => {
            this.appendUnique(searchLogs, log);
        });

        this.setState ({
            searchLogs: searchLogs,
            queryStatus: QUERY_STATUS.OFF,
        });
    }

    /**
     * https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
     * 
     * set the query status to pending
     * @param {*} week: array of strings in (MM/DD/YYYY - MM/DD/YYYY) format
     */
    queryWeek(week) {
        this.setState ({
            queryStatus: QUERY_STATUS.PENDING,
        });

        const startEndDates = week.split(" ~ ");

        let url = new URL('http://localhost:5000/queryWeek')
        url.searchParams.append('start', startEndDates[0]);
        url.searchParams.append('end', startEndDates[1]);

        const sse = new EventSource(url.toString());
        sse.onmessage = event => {
            console.log(event.data);
            if (event.data.includes("no data")) {
                this.setState ({
                    queryStatus: QUERY_STATUS.OFF,
                });
                sse.close();
                return;
            }
            
            this.saveLogs(event.data);
            sse.close();
        }
        sse.onerror = _ => {
            this.setState ({
                queryStatus: QUERY_STATUS.OFF,
            });
            sse.close();
        }
    }

    editEntry(index) {
        this.setState({
            manualAddition: true,
            editEntry: index,
        });
    }

    deleteEntry(index) {
        this.setState({
            searchLogs: this.state.searchLogs.filter((_, i) => i !== index),
        });
    }

    render() {
        const { searchLogs, manualAddition, queryStatus, editEntry } = this.state;
        
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
                        { this.state.queryStatus === QUERY_STATUS.OFF ? 
                            <button onClick={() => this.toggleManualAddition()}>Manually Add Job</button> :
                            <button disabled>Querying...</button> }
                        </div>
                        <div className="button-container"> 
                            { this.state.queryStatus === QUERY_STATUS.OFF ? 
                            <button onClick={() => this.moveQueryStatusToSelect()}>Query Week</button> :
                            <button disabled>Querying...</button> }
                        </div>
                    </section>
                    <section id="job-list">
                        <p>Below is a list of the job search contacts.</p>
                        <h3>Job Search Logs</h3>

                        <Table searchLogs={searchLogs} 
                        editEntry={(index) => this.editEntry(index)}
                        deleteEntry={(index) => this.deleteEntry(index)}/>
                    </section>
                </div>

                <SelectWeek 
                    status={queryStatus} 
                    selectWeek={(week) => this.queryWeek(week)}
                    handleClose={() => this.setState({queryStatus: QUERY_STATUS.OFF})}
                >
                </SelectWeek> 

                <ManualAdditionPopUp 
                    trigger={manualAddition} 
                    editEntry={editEntry}
                    handleSubmit={(event, inputs) => 
                        this.submitManualAdditionFormAndReturnStatus(event, inputs)}
                    handleEditEntry={(event, inputs) => this.submitEditEntryFormAndReturnStatus(event, inputs)}  
                    handleClose={() => this.toggleManualAddition()}
                >
                </ManualAdditionPopUp> 

                

                { queryStatus === QUERY_STATUS.PENDING && <LoadingScreen/> } 
                
            </div>
        );
    }
}

export default Main;