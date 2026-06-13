import { useState, useEffect } from 'react';
import api from '../api';

const DebugTimetable = () => {
  const [debugInfo, setDebugInfo] = useState([]);
  const [loading, setLoading] = useState(false);

  const addDebugInfo = (message) => {
    setDebugInfo(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testTimetableAPI = async () => {
    setLoading(true);
    setDebugInfo([]);
    
    try {
      addDebugInfo('Starting timetable API test...');
      
      // Check if user is authenticated
      const token = localStorage.getItem('access_token');
      const userInfo = localStorage.getItem('user_info');
      
      addDebugInfo(`Token exists: ${!!token}`);
      addDebugInfo(`User info: ${userInfo}`);
      
      if (!token) {
        addDebugInfo('ERROR: No access token found');
        return;
      }
      
      // Test the API call
      addDebugInfo('Making API request to /api/academics/timetables/pdfs/');
      
      const response = await api.get('/api/academics/timetables/pdfs/');
      
      addDebugInfo(`Response status: ${response.status}`);
      addDebugInfo(`Response data type: ${typeof response.data}`);
      addDebugInfo(`Response data length: ${Array.isArray(response.data) ? response.data.length : 'Not an array'}`);
      addDebugInfo(`Response data: ${JSON.stringify(response.data, null, 2)}`);
      
    } catch (error) {
      addDebugInfo(`ERROR: ${error.message}`);
      addDebugInfo(`Error response: ${error.response?.status} - ${error.response?.statusText}`);
      addDebugInfo(`Error data: ${JSON.stringify(error.response?.data, null, 2)}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testTimetableAPI();
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>Timetable API Debug</h1>
      <button onClick={testTimetableAPI} disabled={loading}>
        {loading ? 'Testing...' : 'Test API Again'}
      </button>
      
      <div style={{ marginTop: '20px', backgroundColor: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
        <h3>Debug Log:</h3>
        {debugInfo.map((info, index) => (
          <div key={index} style={{ marginBottom: '5px', fontSize: '12px' }}>
            {info}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DebugTimetable;