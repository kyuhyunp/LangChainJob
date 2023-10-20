import React from 'react'

function LoadingScreen() {
  return (
    <div className="popUpContainer">
        <div className="popUpInner">
            <div id="loading">
                <h1>Loading...</h1>
            </div>
        </div>
    </div>
  );
}

export default LoadingScreen;