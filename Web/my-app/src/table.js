import React from 'react';


const Rows = (props) => {
    if (props.even) {
        return (
            <tr id="evenRow">
                <td>{props.date}</td>
                <td>{props.employerName}</td>
                <td>{props.jobTitle}</td>
                <td>{props.contactInfo}</td>
                <td>
                    <button onClick={props.editEntry}>Edit</button>
                    <button onClick={props.deleteEntry}>Delete</button>
                </td> 
            </tr>
        );
    }

    return (
        <tr id="oddRow">
            <td>{props.date}</td>
            <td>{props.employerName}</td>
            <td>{props.jobTitle}</td>
            <td>{props.contactInfo}</td>
            <td>
                <button onClick={props.editEntry}>Edit</button>
                <button onClick={props.deleteEntry}>Delete</button>
            </td> 
        </tr>
    );
}

const TableBody = (props) => {
    if (props.searchLogs.length === 0) {
        return "";
    }

    return (<tbody>
        {props.searchLogs.map((row, index) => {
            return <Rows key={index} 
                date={row.date} 
                employerName={row.employerName} 
                jobTitle={row.jobTitle} 
                contactInfo={row.contactInfo} 
                even={index % 2 === 0}
                editEntry={() => props.editEntry(index)}
                deleteEntry={() => props.deleteEntry(index)}
            />;
        })}
    </tbody>);
}

function Table(props) {
    return (
        <table>
            <thead>
                <tr>
                    <td>Contact Date</td>
                    <td>Employer Name</td>
                    <td>Job Title</td>
                    <td>Contact Information</td>
                    <td>Actions</td>
                </tr>
            </thead>
            <TableBody searchLogs={props.searchLogs} 
            editEntry={(index) => props.editEntry(index)}
            deleteEntry={(index) => props.deleteEntry(index)}/>
        </table>
    );
}

export default Table;