import { useEffect, useState } from 'react';
import axios from 'axios';

const Data = () => {
  const [results, setResults] = useState([]);
  const [errorMessage, setErrorMessage] = useState(0);

  const searchApi = async (fromDate, toDate) => {
    console.log('date being passed: ', fromDate, 'and', toDate);
    try {
      const response = await axios.post('http://127.0.0.1:5000/data', {
        head: 'Application/json',
        body: JSON.stringify({ fromDate, toDate }),
      });
      const result = [
        JSON.parse(response.data[0]),
        JSON.parse(response.data[1]),
        JSON.parse(response.data[2]),
        JSON.parse(response.data[3]),
        JSON.parse(response.data[4]),
      ];
      setResults(result);
    } catch (err) {
      setErrorMessage(err);
    }
  };
  useEffect(() => {
    searchApi('2020-01-01', '2020-12-30');
  }, []);
  console.log('this is what is being returned: ', results);
  return [searchApi, results, errorMessage];
};
export default Data;
