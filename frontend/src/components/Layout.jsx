import React from 'react';
import Navigation from './Navigation';

const Layout = ({ children }) => {
  return (
    <div className="relative h-screen">
      <main>{children}</main>
      <Navigation />
    </div>
  );
};

export default Layout;