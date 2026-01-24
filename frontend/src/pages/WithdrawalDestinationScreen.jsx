import React from 'react';
import { Link } from 'react-router-dom';

const WithdrawalDestinationScreen = () => {
  return (
    <div className="relative flex min-h-screen w-full flex-col bg-background-dark max-w-[430px] mx-auto overflow-x-hidden pb-32">
        <header className="sticky top-0 z-50 flex items-center bg-background-dark/80 backdrop-blur-md p-4 justify-between border-b border-white/5">
            <Link to="/wallet" className="text-white flex size-10 shrink-0 items-center justify-center cursor-pointer">
            <span className="material-symbols-outlined">arrow_back</span>
            </Link>
            <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-10">Choose destination</h2>
        </header>

        <div className="w-full h-1 bg-white/10">
            <div className="h-full bg-primary w-1/3"></div>
        </div>

        <div className="flex flex-col px-5 pt-8">
            <h1 className="text-2xl font-bold mb-2">Where should we send your funds?</h1>
            <p className="text-[#888888] text-sm mb-8">Available balance: $1,240.50</p>
            {/* Destination options will be added here */}
        </div>

        <div className="fixed bottom-0 left-0 right-0 max-w-[430px] mx-auto bg-background-dark/95 backdrop-blur-xl p-5 pb-10 border-t border-white/10">
            <Link to="/withdraw/review">
                <button className="w-full bg-primary hover:bg-primary/90 text-background-dark text-lg font-bold py-4 rounded-xl shadow-[0_8px_30px_rgba(249,164,6,0.2)] transition-all active:scale-[0.98]">
                    Continue
                </button>
            </Link>
        </div>
    </div>
  );
};

export default WithdrawalDestinationScreen;