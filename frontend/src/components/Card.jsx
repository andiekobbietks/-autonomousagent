import React from 'react';

const Card = ({ children, className, ...props }) => {
  return (
    <div
      className={`bg-black/60 backdrop-blur-2xl border border-white/10 rounded-2xl p-4 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;