// components/ui/card.js
import React from 'react';

export const Card = ({ children }) => (
  <div className="border rounded-md shadow p-4">{children}</div>
);

export const CardContent = ({ children }) => (
  <div className="content">{children}</div>
);

export const CardDescription = ({ children }) => (
  <p className="description">{children}</p>
);

export const CardHeader = ({ children }) => (
  <div className="header">{children}</div>
);

export const CardTitle = ({ children }) => (
  <h2 className="title">{children}</h2>
);
