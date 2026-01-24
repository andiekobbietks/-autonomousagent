import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <nav className="absolute bottom-0 left-0 w-full z-30 bg-[#000000] pt-4 pb-10 border-t border-white/10">
      <div className="flex justify-around items-center px-6">
        <Link to="/dashboard" className="flex flex-col items-center gap-1.5 text-white">
          <span className="material-symbols-outlined font-normal fill-1 text-[26px]">explore</span>
          <span className="text-[10px] font-bold tracking-wide">Radar</span>
        </Link>
        <Link to="/pools" className="flex flex-col items-center gap-1.5 text-white">
          <span className="material-symbols-outlined font-normal text-[26px]">group</span>
          <span className="text-[10px] font-bold tracking-wide">Pools</span>
        </Link>
        <div className="relative -top-2">
          <button className="flex size-14 items-center justify-center rounded-full bg-white text-black shadow-xl active:scale-95 transition-transform">
            <span className="material-symbols-outlined text-3xl font-bold">add</span>
          </button>
        </div>
        <Link to="/wallet" className="flex flex-col items-center gap-1.5 text-white">
          <span className="material-symbols-outlined font-normal text-[26px]">account_balance_wallet</span>
          <span className="text-[10px] font-bold tracking-wide">Wallet</span>
        </Link>
        <Link to="/settings" className="flex flex-col items-center gap-1.5 text-white">
          <span className="material-symbols-outlined font-normal text-[26px]">settings</span>
          <span className="text-[10px] font-bold tracking-wide">Settings</span>
        </Link>
      </div>
    </nav>
  );
};

export default Navigation;