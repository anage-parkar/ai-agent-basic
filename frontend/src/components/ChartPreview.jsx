import React from 'react';

const ChartPreview = ({ images }) => {
  if (!images || images.length === 0) {
    return null;
  }
  
  return (
    <div className="chart-preview">
      {images.map((image, index) => (
        <div key={index} className="chart-item">
          <img 
            src={`data:image/png;base64,${image}`} 
            alt={`Chart ${index + 1}`}
            className="chart-image"
          />
        </div>
      ))}
    </div>
  );
};

export default ChartPreview;
