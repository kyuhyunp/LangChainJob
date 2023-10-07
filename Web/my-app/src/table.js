import React from 'react';

import './css/main.css';

class Table extends React.Component {
    // Todo: add log
    
    render() {
        return (
            <table>
                <thead>
                    <tr>
                        <td>Contact Date</td>
                        <td>Employer Name</td>
                        <td>Job Title</td>
                        <td>Contact Information</td>
                    </tr>
                </thead>
            </table>
        );
    }
}

export default Table;