import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import { getUser } from '../services/userService';

const Dashboard = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getUser();
                setUser(userData);
            } catch (error) {
                console.error('Failed to fetch user', error);
            }
        };

        fetchUser();
    }, []);
  return (
    <div className="relative flex h-screen w-full flex-col bg-black">
      <div className="absolute inset-0 z-0">
        <div
          className="w-full h-full bg-cover bg-center grayscale contrast-[1.2] brightness-[0.15]"
          style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuCAZOE85wOhVPpw9iL-T-CJdR9tIxnVsSVxtFqtIHkrjYuG0w-QLxTO7YiM2MlkaHZmc9OzQZ0cUshFo9q6qzL2ZNs8gSmcnxZbV9NEnVVi7ugeAY5hUHhaj7CtlSV1KcsyyKraE0DnLW7KXZOBSv1rToITl3wkiOL3cxAmdUE0GXnv9S8yKHC4IU9AM4T6mU8b46Gz9mUmPS5ZejvMF4SiAi66qeGaQ9DirpmpJFqD-kRYDoyNRAfSvmCGvfwZ47a8DcSHma05d77W')"}}
        ></div>
        <div className="absolute top-[30%] left-[25%] w-2.5 h-2.5 bg-[var(--alert-orange)] rounded-full glow-dot"></div>
        <div className="absolute top-[55%] left-[60%] w-3 h-3 bg-[var(--alert-orange)] rounded-full glow-dot"></div>
        <div className="absolute top-[40%] right-[20%] w-2.5 h-2.5 bg-[var(--alert-orange)] rounded-full glow-dot"></div>
        <div className="absolute bottom-[45%] left-[40%] w-3 h-3 bg-[var(--alert-orange)] rounded-full glow-dot"></div>
        <div className="absolute top-[15%] right-[45%] w-2 h-2 bg-[var(--alert-orange)]/80 rounded-full glow-dot"></div>
      </div>
      <div className="relative z-20 px-6 pt-14 pb-4 bg-gradient-to-b from-black/80 to-transparent">
        <div className="flex items-center justify-between relative mb-6">
          <div className="w-10"></div>
          <h1 className="text-white text-xl font-bold tracking-tight">Radar</h1>
          <div className="w-10 flex justify-end items-center">
            {user && <span className="text-white mr-2">{user.username}</span>}
            <span className="material-symbols-outlined text-white text-2xl cursor-pointer">account_circle</span>
          </div>
        </div>
        <div className="max-w-md mx-auto">
          <div className="flex items-center w-full h-12 px-5 rounded-full border border-white/40 bg-black/40 backdrop-blur-md">
            <span className="material-symbols-outlined text-white text-xl mr-3">search</span>
            <input className="bg-transparent border-none focus:ring-0 text-white placeholder-white/80 text-base font-medium w-full p-0" placeholder="Where to next?" type="text"/>
          </div>
        </div>
      </div>
      <div className="absolute right-4 top-1/2 -translate-y-1/2 z-20 flex flex-col gap-4">
        <button className="flex size-11 items-center justify-center rounded-full glass-tile border-white/20 text-white shadow-lg">
          <span className="material-symbols-outlined text-2xl">layers</span>
        </button>
        <button className="flex size-11 items-center justify-center rounded-full glass-tile border-white/20 text-white shadow-lg">
          <span className="material-symbols-outlined text-2xl">near_me</span>
        </button>
      </div>
      <div className="mt-auto relative z-20 pb-32">
        <div className="flex gap-4 px-6 overflow-x-auto no-scrollbar">
          <Card className="min-w-[280px] glass-tile rounded-3xl p-6 flex flex-col justify-between shadow-2xl">
            <div>
              <p className="text-white/80 text-[11px] uppercase tracking-[0.1em] font-bold mb-1">Active Rotations</p>
              <h3 className="text-white text-2xl font-bold tracking-tight">8 Pools Local</h3>
            </div>
            <div className="mt-5 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-[var(--alert-orange)] animate-pulse"></span>
              <span className="text-[var(--alert-orange)] text-xs font-black uppercase tracking-wider">Live Activity</span>
            </div>
          </Card>
          <Card className="min-w-[280px] glass-tile rounded-3xl p-6 flex flex-col justify-between shadow-2xl">
            <div>
              <p className="text-white/80 text-[11px] uppercase tracking-[0.1em] font-bold mb-1">Growth Forecast</p>
              <h3 className="text-white text-2xl font-bold tracking-tight">+$1,240.00</h3>
            </div>
            <div className="mt-5 flex items-center gap-1.5">
              <span className="material-symbols-outlined text-green-500 text-lg">trending_up</span>
              <span className="text-green-500 text-xs font-black uppercase tracking-wider">12.4% vs last week</span>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;