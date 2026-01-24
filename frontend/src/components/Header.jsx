import React from 'react';

const Header = ({ title, leftButton, rightButton }) => {
  return (
    <header className="sticky top-0 z-50 flex items-center bg-black/80 backdrop-blur-md p-4 justify-between border-b border-zinc-800/50">
      <div className="w-10">{leftButton}</div>
      <h2 className="text-white text-lg font-bold leading-tight tracking-tight flex-1 text-center">{title}</h2>
      <div className="w-10 flex justify-end">{rightButton}</div>
    </header>
  );
};

export default Header;