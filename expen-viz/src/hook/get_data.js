import { useEffect, useState } from "react";
import axios from "axios";

const Data = () => {
    const [results, setResults] = useState([]);
    const [errorMessage, setErrorMessage] = useState("");

    const searchApi = async () => {
        try {
            const response = await axios.get("/data", {});
            const result = [JSON.parse(response.data[0]), JSON.parse(response.data[1]), JSON.parse(response.data[2]), JSON.parse(response.data[3]), JSON.parse(response.data[4])];
            setResults(result);
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
