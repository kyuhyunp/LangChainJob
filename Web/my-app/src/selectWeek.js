import React from 'react';
import { QUERY_STATUS } from './queryStatus';
import moment from 'moment';

const WEEKS = 52;
function getFirstDayOfWeek() {
    const today = new Date();
    let day = today.getDay();
    let diff = today.getDate() - day + (day === 0 ? -6 : 1);

    return new Date(today.setDate(diff));
}  

function getPrevWeeks() {
    let currMonday = moment(getFirstDayOfWeek().toLocaleDateString(), "MM/DD/YYYY");
    let ret = [];
    
    for (let week = 0; week < WEEKS; ++week) {
        const start = moment(currMonday).subtract(7, 'days');
        const end = moment(currMonday).subtract(1, 'days');
        ret.push(start.format("MM-DD-YYYY") + ' ~ ' + end.format("MM-DD-YYYY"));
        currMonday = start;
    }

    return ret;
}

const MenuItems = (props) => {
    return (
        getPrevWeeks().map((date, idx) => {
            return <DropDownMenu key={idx} 
            id={idx} 
            date={date}
            selectWeek={(week) => props.selectWeek(week)}
            />
        })
    );
}

const DropDownMenu = (props) => {
    return (
    <li key={props.id}>
        <button id="dropDownButton"
            onClick={() => props.selectWeek(props.date)}>
            { props.date }
        </button>
    </li>
    );
}

function SelectWeek(props) {
      
    return props.status === QUERY_STATUS.SELECT ? (
        <div className="popUpContainer">

            <div className="popUpInner">
                <div className="popUpTitle">
                    <h2> Select Week </h2>
                    <button onClick={() => props.handleClose()}>Exit</button>
                </div>
                <p>Please select the week to query Gmail.</p>
                <div className="selectWeekContainer">
                    <ul className="menu">
                    <MenuItems selectWeek={(week) => props.selectWeek(week)}/>
                    </ul>
                </div>
            </div> 
        </div>
    ): ""; 
}

export default SelectWeek;