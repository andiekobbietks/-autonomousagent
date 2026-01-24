import React from 'react';
import { Link } from 'react-router-dom';

const WithdrawalSuccessScreen = () => {
  return (
    <div className="relative flex flex-col min-h-screen w-full max-w-[430px] mx-auto bg-background-dark px-6">
      <div className="flex-1 flex flex-col items-center justify-center text-center -mt-20">
        <div className="relative mb-10">
          <div className="size-28 rounded-full border-2 border-green-500 flex items-center justify-center bg-green-500/5">
            <span className="material-symbols-outlined text-[64px] text-green-500">
              check_circle
            </span>
          </div>
        </div>
        <h1 className="text-white text-4xl font-bold tracking-tight mb-4">
          Funds on the Way
        </h1>
        <p className="text-white/60 text-lg leading-relaxed max-w-[300px]">
          Your £1,240.50 will arrive in your bank account shortly.
        </p>
      </div>
      <div className="pb-12 pt-4">
        <Link to="/dashboard">
          <button className="w-full bg-white hover:bg-gray-200 text-black text-lg font-bold py-4 rounded-xl transition-all active:scale-[0.98]">
            Done
          </button>
        </Link>
      </div>
    </div>
  );
};

export default WithdrawalSuccessScreen;