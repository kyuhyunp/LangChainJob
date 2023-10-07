import React from 'react';

function ManualAdditionPopUp(props) {
    return props.trigger ? (
        <div id="manualAddition">
            <p>Please enter the following entries.</p>
            <form>
                <label>
                    <input 
                        type="text" 
                        name="date" 
                        placeholder="Contact Date (MM/DD/YYYY)"
                        value={props.date}
                        onChange={() => props.handleChange()}
                    />
                    <input type="text" name="employerName" placeholder="Employer Name"/>
                    <input type="text" name="jobTitle" placeholder="Job Title"/>
                    <input type="text" name="contactInfo" placeholder="Contact Information (URI)"/>
                </label>
                <input type="submit" value="Submit"/>
            </form>
        </div>
    ): ""; 
}

export default ManualAdditionPopUp;