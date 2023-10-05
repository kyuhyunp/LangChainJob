import React from 'react';

import './css/main.css';
import Table from './table.js';

class Main extends React.Component {
    render() {
        return (
            <div id="container">
                <nav>
                    <div id="title-container">
                        <h1>JOB LOGGER</h1> 
                    </div>
                    <div id="contact-info">
                        <a href="kyuhyunpark.official@gmail.com">Email</a>
                        <a href="https://www.linkedin.com/in/kyuhyunp/">LinkedIn</a>
                    </div>
                </nav>

                <div id="content-container">
                    <section id="search-bar">
                        <div class="button-container"> 
                            <button>Manually Add Job</button>
                        </div>
                        <div class="button-container"> 
                            <button>Query Week</button>
                        </div>
                    </section>
                    <section id="job-list">
                        <p>Below is a list of the job search contacts.</p>
                        <h3>Job Search Log</h3>

                        <Table/>
                    </section>
                </div>

            </div>
        );
    }
}

export default Main;