import React from 'react';

const Input = ({ type = 'text', placeholder, className, ...props }) => {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className={`w-full bg-transparent border border-white/20 rounded-lg p-3 focus:ring-1 focus:ring-primary focus:border-primary transition-all ${className}`}
      {...props}
    />
  );
};

export default Input;