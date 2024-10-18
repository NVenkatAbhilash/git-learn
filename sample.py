import React from 'react';
import axios from 'axios';

function App() {
  const handleDownload = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/download', {
        responseType: 'blob', // Important for file downloads
      });

      // Create a link element
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'sample_data.xlsx'); // File name to download

      // Append to the body and click to trigger download
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error('Error downloading the file:', error);
    }
  };

  return (
    <div>
      <h1>Download Excel File</h1>
      <button onClick={handleDownload}>Download XLSX</button>
    </div>
  );
}

export default App;
