import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/Input';
import Button from '../components/Button';
import { register } from '../services/authService';

const JoinNetworkScreen = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        referral_code: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(formData);
            navigate('/onboarding/secure');
        } catch (error) {
            console.error('Registration failed', error);
        }
    };
  return (
    <div className="bg-background-dark text-white min-h-screen flex flex-col">
      <div className="flex items-center bg-transparent p-4 pb-2 justify-between">
        <div aria-label="Go back" className="text-white flex size-12 shrink-0 items-center cursor-pointer">
          <span className="material-symbols-outlined" style={{fontSize: '24px'}}>arrow_back_ios</span>
        </div>
        <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center">Join the Network</h2>
        <div className="size-12"></div>
      </div>
      <div className="flex w-full flex-row items-center justify-center gap-3 py-4">
        <div className="h-1.5 w-8 rounded-full bg-white/20"></div>
        <div className="h-1.5 w-8 rounded-full bg-white/20"></div>
        <div className="h-1.5 w-8 rounded-full bg-primary"></div>
      </div>
      <div className="px-6 pt-8 pb-4">
        <h1 className="text-white tracking-tight text-[36px] font-bold leading-tight text-left">Final Step</h1>
        <p className="text-white/60 text-base font-normal leading-relaxed pt-2">
          Enter your credentials to activate your account and start sharing with the community.
        </p>
      </div>
      <form onSubmit={handleSubmit} className="flex-1 px-6 space-y-6 pt-4">
        <div className="flex flex-col">
          <label className="text-white/80 text-sm font-medium leading-normal pb-2 ml-1">Username</label>
          <Input name="username" placeholder="Choose a username" type="text" onChange={handleChange} />
        </div>
        <div className="flex flex-col">
          <label className="text-white/80 text-sm font-medium leading-normal pb-2 ml-1">Email</label>
          <Input name="email" placeholder="Enter your email" type="email" onChange={handleChange} />
        </div>
        <div className="flex flex-col">
          <label className="text-white/80 text-sm font-medium leading-normal pb-2 ml-1">Password</label>
          <Input name="password" placeholder="Create a password" type="password" onChange={handleChange} />
        </div>
        <div className="flex flex-col">
          <label className="text-white/80 text-sm font-medium leading-normal pb-2 ml-1">Invite Code (Optional)</label>
          <div className="relative group">
            <Input name="referral_code" placeholder="VERIFY-XXXX" type="text" onChange={handleChange} />
            <div className="absolute right-4 top-1/2 -translate-y-1/2">
              <span className="material-symbols-outlined text-white/40" style={{fontSize: '20px'}}>qr_code_scanner</span>
            </div>
          </div>
        </div>
      </form>
      <div className="p-6 pb-10 space-y-6">
          <Button onClick={handleSubmit} className="w-full bg-primary text-white text-lg tracking-wider">
            JOIN THE NETWORK
            <span className="material-symbols-outlined" style={{fontSize: '24px'}}>bolt</span>
          </Button>
        <div className="text-center">
          <p className="text-[#4A4A4A] text-xs font-normal leading-normal">
            By joining, you agree to our
            <a className="underline hover:text-white/60 transition-colors" href="#">Terms of Service</a>
            and
            <a className="underline hover:text-white/60 transition-colors" href="#">Privacy Policy</a>.
          </p>
        </div>
      </div>
    </div>
  );
};

export default JoinNetworkScreen;