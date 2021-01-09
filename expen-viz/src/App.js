import React from "react";
import Plot from "react-plotly.js";
import logo from "./logo.svg";
import "./App.css";
import Data from "./hook/get_data";

function App() {
    // const [graphdata, setgraphdata] = useState(0);
    const [results, errorMessage] = Data();

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
                <Plot data={results.data} layout={results.layout} />
            </header>
        </div>
    );
}

export default App;
