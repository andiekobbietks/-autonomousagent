import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';

const WelcomeScreen = () => {
  return (
    <div className="relative flex h-screen w-full flex-col overflow-hidden bg-background-dark group/design-root">
      <div className="absolute inset-0 z-0">
        <div
          className="h-full w-full bg-cover bg-center bg-no-repeat"
          style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDHnR2185P0dqDPSiwIBXtwrjouMpVdiEs2Lhnroi83mucAuxU06JtI0Ohc4lbkhQUBme8xqLRzslEtiPoKOkKawVtYxL_2SwqW3_7fmdXKa4Zxos1BHX3DK5bwOCTstkvHzkV_q5gitk-ZTeIGoadYjS-8y-1g9WUHEaZSHptxvpfaqTJBxCLDVttoRxsQOB4QPv1E_wTojTaL883ggQZtubi8jYL-Ya7gV53l759YNsGr7OePerYL54sDrBTFNUU30t0OWbF96Fzc")'}}
        ></div>
        <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent"></div>
      </div>
      <div className="relative z-10 flex flex-1 flex-col justify-between px-6 pb-12 pt-16">
        <div className="mt-8">
          <h1 className="text-white tracking-tight text-[48px] font-extrabold leading-[1.1] text-left">
            Accelerate <br />
            Your Community <br />
            Wealth
          </h1>
        </div>
        <div className="flex flex-col gap-8">
          <div className="flex w-full flex-row items-center justify-start gap-2.5">
            <div className="h-1.5 w-8 rounded-full bg-primary shadow-[0_0_10px_rgba(89,244,37,0.5)]"></div>
            <div className="h-1.5 w-1.5 rounded-full bg-white/30"></div>
            <div className="h-1.5 w-1.5 rounded-full bg-white/30"></div>
          </div>
          <div className="w-full">
            <Link to="/onboarding/radar">
              <Button className="w-full h-16 bg-primary text-black text-lg font-extrabold uppercase tracking-wide">
                Get Started
              </Button>
            </Link>
          </div>
          <p className="text-center text-white/50 text-sm font-medium">
            Already a member? <Link to="/login" className="text-primary font-bold cursor-pointer">Log In</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;