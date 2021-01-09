import { useEffect, useState } from "react";
import axios from "axios";

const Data = () => {
    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    const searchApi = async () => {
        try {
            const response = await axios.get("/data", {});
            setResults(response.data);
        } catch (err) {
            setErrorMessage("Something Went Wrong");
        }
    };
    useEffect(() => {
        searchApi();
    }, []);

    return [results, errorMessage];
};
export default Data;
