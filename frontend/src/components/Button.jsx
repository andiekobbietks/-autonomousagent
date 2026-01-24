import React from 'react';

const Button = ({ children, onClick, className, ...props }) => {
  return (
    <button
      onClick={onClick}
      className={`font-bold py-2 px-4 rounded transition-all active:scale-[0.98] ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
