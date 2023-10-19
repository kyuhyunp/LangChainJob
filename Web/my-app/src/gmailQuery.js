import React from 'react'

function GmailQuery(props) {
    const [data, setData] = React.useState("");

    React.useEffect(() => {
        const sse = new EventSource('http://localhost:5000/stream')
        
        function handleStream(data) {
            console.log(data);
            setData(data);
        }

        sse.onmessage = event => {
            return handleStream(event.data);
        }
        sse.onerror = _ => {
            sse.close();
        }

        return () => {;
            sse.close()
        }
    }, [])
    return (
        <div>streamed : { data }</div>
    );
}

export default GmailQuery;