// components/ui/card.js
import React from 'react';

const Card = ({ children }) => {
  return (
    <div className="border rounded-lg p-4 shadow-md">
      {children}
    </div>
  );
};

export const CardContent = ({ children }) => (
  <div className="p-4">{children}</div>
);

export const CardDescription = ({ children }) => (
  <p className="text-sm text-gray-500">{children}</p>
);

export const CardHeader = ({ children }) => (
  <div className="border-b pb-2 mb-2">{children}</div>
);

export const CardTitle = ({ children }) => (
  <h3 className="text-lg font-semibold">{children}</h3>
);

export default Card;
