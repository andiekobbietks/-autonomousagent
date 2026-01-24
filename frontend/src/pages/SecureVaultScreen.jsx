import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';

const SecureVaultScreen = () => {
  return (
    <div className="relative flex h-screen w-full flex-col bg-background-dark overflow-hidden">
      <div className="flex items-center justify-between p-6 pt-12">
        <div className="text-white flex size-10 shrink-0 items-center justify-center cursor-pointer hover:bg-white/10 rounded-full transition-colors">
          <span className="material-symbols-outlined text-2xl">arrow_back_ios_new</span>
        </div>
        <div className="flex-1"></div>
      </div>
      <div className="flex flex-col flex-1 items-center justify-center px-8">
        <h1 className="text-white tracking-tight text-[32px] font-extrabold leading-tight text-center pb-12">
          Secure Your Vault
        </h1>
        <div className="flex items-center justify-center mb-16">
          <div className="relative flex items-center justify-center">
            <div className="absolute w-40 h-40 bg-white/5 rounded-full blur-3xl"></div>
            <div className="flex items-center justify-center text-white">
              <span className="material-symbols-outlined text-[120px] font-light">face</span>
            </div>
          </div>
        </div>
        <div className="max-w-[280px]">
          <p className="text-white/70 text-base font-normal leading-relaxed text-center">
            Use biometrics for instant, secure access to community rotations.
          </p>
        </div>
      </div>
      <div className="flex flex-col gap-4 px-6 pb-12 w-full max-w-[480px] mx-auto">
        <Link to="/dashboard">
            <Button className="w-full h-14 bg-primary text-black text-lg">
                Enable FaceID
            </Button>
        </Link>
        <Link to="/dashboard">
            <Button className="w-full h-12 text-[#4B4B4B] bg-transparent">
                Maybe Later
            </Button>
        </Link>
      </div>
    </div>
  );
};

export default SecureVaultScreen;