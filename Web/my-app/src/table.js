import React from 'react';

import './css/main.css';

class Table extends React.Component {
    // Todo: add log
    
    render() {
        return (
            <table class="tg">
                <thead>
                    <tr>
                        <td class="tg-0lax">Contact Date</td>
                        <td class="tg-0lax">Employer Name</td>
                        <td class="tg-0lax">Job Title</td>
                        <td class="tg-0lax">Contact Information</td>
                    </tr>
                </thead>
            </table>
        );
    }
}

export default Table;