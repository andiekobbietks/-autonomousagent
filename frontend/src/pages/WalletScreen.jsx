import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getWallet, getTransactions } from '../services/walletService';

const WalletScreen = () => {
    const [wallet, setWallet] = useState(null);
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const walletData = await getWallet();
                setWallet(walletData);
                const transactionsData = await getTransactions();
                setTransactions(transactionsData);
            } catch (error) {
                console.error('Failed to fetch wallet data', error);
            }
        };

        fetchData();
    }, []);

  return (
    <div className="relative flex min-h-screen w-full flex-col bg-background-dark max-w-[430px] mx-auto overflow-x-hidden pb-24">
      <header className="sticky top-0 z-50 flex items-center bg-background-dark/80 backdrop-blur-md p-4 justify-between border-b border-white/5">
        <Link to="/dashboard" className="text-white flex size-10 shrink-0 items-center justify-center cursor-pointer">
          <span className="material-symbols-outlined">arrow_back</span>
        </Link>
        <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-10">Wallet</h2>
      </header>

      <div className="flex flex-col items-center py-10 px-4">
        <p className="text-[#888888] text-sm font-medium uppercase tracking-widest pb-1">Current Balance</p>
        <h1 className="text-white tracking-tight text-[48px] font-bold leading-tight">${wallet ? wallet.balance : '0.00'}</h1>
        <div className="mt-4 flex gap-2 items-center bg-white/5 px-3 py-1.5 rounded-full">
          <span className="material-symbols-outlined text-green-500 text-sm">check_circle</span>
          <span className="text-sm font-medium text-white/80">All payments cleared</span>
        </div>
      </div>

      <div className="px-4 pb-2 pt-6 flex justify-between items-end border-b border-white/5">
        <h3 className="text-white text-lg font-bold leading-tight tracking-[-0.015em]">Recent Activity</h3>
        <p className="text-primary text-sm font-semibold cursor-pointer">View all</p>
      </div>

      <div className="flex flex-col">
        {transactions.map(tx => (
            <div key={tx.id} className="flex items-center gap-4 hover:bg-white/5 transition-colors px-4 min-h-[80px] py-3 justify-between">
                <div>
                    <p className="text-white">{tx.type}</p>
                    <p className="text-gray-400 text-sm">{new Date(tx.timestamp).toLocaleDateString()}</p>
                </div>
                <p className={`text-lg font-bold ${tx.amount > 0 ? 'text-green-500' : 'text-white'}`}>
                    {tx.amount > 0 ? '+' : ''}${tx.amount}
                </p>
            </div>
        ))}
      </div>

      <div className="fixed bottom-0 left-0 right-0 max-w-[430px] mx-auto bg-background-dark/90 backdrop-blur-xl p-4 pb-8 border-t border-white/5">
        <Link to="/withdraw/destination">
            <button className="w-full bg-primary hover:bg-primary/90 text-background-dark text-lg font-bold py-4 rounded-xl shadow-[0_4px_20px_rgba(249,164,6,0.3)] transition-all active:scale-[0.98]">
                Withdraw Funds
            </button>
        </Link>
      </div>
    </div>
  );
};

export default WalletScreen;