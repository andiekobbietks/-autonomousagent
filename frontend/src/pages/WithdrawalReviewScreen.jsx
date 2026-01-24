import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { withdraw } from '../services/walletService';

const WithdrawalReviewScreen = () => {
    const navigate = useNavigate();
    const [amount, setAmount] = useState(1240.50); // Example amount

    const handleWithdraw = async () => {
        try {
            await withdraw({ amount });
            navigate('/withdraw/success');
        } catch (error) {
            console.error('Withdrawal failed', error);
        }
    };

  return (
    <div className="relative flex min-h-screen w-full flex-col bg-background-dark max-w-[430px] mx-auto overflow-x-hidden">
        <header className="sticky top-0 z-50 flex items-center bg-background-dark/80 backdrop-blur-md p-4 justify-between">
            <button onClick={() => navigate(-1)} className="text-white flex size-10 shrink-0 items-center justify-center cursor-pointer">
                <span className="material-symbols-outlined">arrow_back</span>
            </button>
            <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-10">Review Withdrawal</h2>
        </header>

        <div className="flex flex-col items-center pt-12 pb-10 px-6">
            <p className="text-[#888888] text-sm font-medium uppercase tracking-[0.2em] pb-3">You'll Receive</p>
            <h1 className="text-white tracking-tight text-[56px] font-bold leading-none">£{amount.toFixed(2)}</h1>
        </div>

        <div className="px-6 space-y-1">
            {/* Withdrawal details will be added here */}
        </div>

        <div className="mt-auto p-6 space-y-4">
            <button onClick={handleWithdraw} className="w-full bg-primary hover:bg-primary/90 text-background-dark text-lg font-bold py-5 rounded-xl shadow-[0_8px_30px_rgba(249,164,6,0.2)] transition-all active:scale-[0.98]">
                Confirm Withdrawal
            </button>
        </div>
    </div>
  );
};

export default WithdrawalReviewScreen;