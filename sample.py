import React, { useEffect } from 'react';

const DownloadExcel = () => {
    useEffect(() => {
        const downloadFile = async () => {
            const response = await fetch('http://localhost:5000/download'); // Replace with your Flask server URL
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'data.xlsx'; // Set the desired filename
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                console.error('Error downloading file:', response.statusText);
            }
        };

        downloadFile();
    }, []);

    return (
        <div>
            {/* Your component content */}
        </div>
    );
};

export default DownloadExcel;
