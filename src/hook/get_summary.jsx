import { useEffect, useState } from 'react';
import axios from 'axios';

const SummaryData = () => {
  const [results, setResults] = useState([]);
  const [errorMessage, setErrorMessage] = useState(0);

  const searchApi = async () => {
    try {
      const response = await axios.get('/summary', {});
      const summaryResult = response.data;
      setResults(summaryResult);
    } catch (err) {
      setErrorMessage('Something Went Wrong');
    }
  };
  useEffect(() => {
    searchApi();
  }, []);
  return [results, errorMessage];
};
export default SummaryData;
