import React from "react";
import Plot from "react-plotly.js";
import logo from "./logo.svg";
import "./App.css";
import Data from "./hooks/get_data";
function App() {
    // const [graphdata, setgraphdata] = useState(0);
    const [results, errorMessage] = Data();
    console.log("===>", results.data);
    return (
        <div className='App'>
            <header className='App-header'>
                <img src={logo} className='App-logo' alt='logo' />
                <p>
                    Edit <code>src/App.js</code> and save to reload.
                </p>
                <a className='App-link' href='https://reactjs.org' target='_blank' rel='noopener noreferrer'>
                    Learn React
                </a>
                <Plot data={results} />
            </header>
        </div>
    );
}

export default App;
