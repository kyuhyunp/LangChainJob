import React from 'react';

function ManualAdditionPopUp(props) {
    const INIT = {
        "date": "",
        "employerName": "",
        "jobTitle": "",
        "contactInfo": "",
    };
    
    const [inputs, setInputs] = React.useState(
        INIT
    );

    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}));
    }

    const handleSubmit = (event) => {
        const completed = props.editEntry === null ? 
        props.handleSubmit(event, inputs) : props.handleEditEntry(event, inputs);

        // Only clear the inputs if the submission was successful
        if (completed) {
            setInputs(_ => (INIT));
        }
    }
      
    return props.trigger ? (
        <div className="popUpContainer">
            <div className="popUpInner">
                <div className="popUpTitle">
                    <h2>Job Search Form</h2>
                    <button onClick={() => props.handleClose()}>Exit</button>
                </div>
                <p>Please enter the following entries.</p>
                <div id="manualAdditionFormContainer"> 
                    <form onSubmit={handleSubmit}>
                        <label>
                            <input 
                                type="text" 
                                name="date" 
                                placeholder="Contact Date (MM-DD-YYYY)"
                                autoComplete="off"
                                value={inputs.date}
                                onChange={handleChange}
                            />
                            <input 
                                type="text" 
                                name="employerName" 
                                placeholder="Employer Name"
                                autoComplete="off"
                                value={inputs.employerName}
                                onChange={handleChange}
                            />
                            <input 
                                type="text" 
                                name="jobTitle" 
                                placeholder="Job Title"
                                autoComplete="off"
                                value={inputs.jobTitle}
                                onChange={handleChange}
                            />
                            <input 
                                type="text" 
                                name="contactInfo" 
                                placeholder="Contact Information (URI)"
                                autoComplete="off"
                                value={inputs.contactInfo}
                                onChange={handleChange}
                            />
                        </label>
                        <input type="submit" value="Submit"/>
                    </form>
                </div>
            </div>
        </div>
    ): ""; 
}

export default ManualAdditionPopUp;