import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/Button';

const RadarScreen = () => {
  return (
    <div className="relative flex h-screen w-full flex-col bg-background-dark overflow-hidden max-w-[430px] mx-auto">
      <div className="flex items-center bg-background-dark p-4 pb-2 justify-between">
        <div aria-label="Back" className="text-white flex size-12 shrink-0 items-center cursor-pointer">
          <span className="material-symbols-outlined text-2xl">arrow_back_ios_new</span>
        </div>
        <div className="flex-1 text-center">
          <span className="text-xs font-bold uppercase tracking-widest text-primary">Radar</span>
        </div>
        <div className="size-12 shrink-0 flex items-center justify-end">
          <span className="text-sm font-medium text-white/50 cursor-pointer">Skip</span>
        </div>
      </div>
      <div className="flex w-full flex-row items-center justify-center gap-3 py-4">
        <div className="h-1.5 w-8 rounded-full bg-white/20"></div>
        <div className="h-1.5 w-8 rounded-full bg-primary"></div>
        <div className="h-1.5 w-8 rounded-full bg-white/20"></div>
      </div>
      <div className="relative flex flex-1 items-center justify-center px-6">
        <div className="relative w-full aspect-square max-w-[340px] rounded-full bg-zinc-900/40 border border-white/5 flex items-center justify-center overflow-hidden">
          <div className="absolute inset-0 opacity-20 grayscale invert" style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuC-NnbsfZQQ0TldR5eEKN_KoMQaNU5eNYV3rvL8vS3kyY0PR464-TqkLu2qiP5yABawRdr3fGQ79pc5DCVChlGBA6ke1B1LOM6pZBsMAg_yG4iJE6i7codN-tyhhzQKpiVh7Mx9YJiO3JG4MVbYxsNtWZSLD-TPbioEMS_fYuTd10CPkHeJrlAKHyYRkgIx8dKgH_fHKZmJwuT_eWVn2n1NO-6MhMiSQ6ZLnF68ag8-cRKw_QQgy-eLxqF5X9WryQmdnWUxjBzk3wY7')", backgroundSize: 'cover' }}></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="absolute w-[80%] h-[80%] border border-white/10 rounded-full"></div>
            <div className="absolute w-[60%] h-[60%] border border-white/10 rounded-full"></div>
            <div className="absolute w-[40%] h-[40%] border border-white/10 rounded-full"></div>
            <div className="absolute inset-0 rounded-full" style={{background: 'conic-gradient(from 0deg, #f27f0d22 0deg, transparent 90deg)', transform: 'rotate(45deg)'}}></div>
          </div>
          <div className="relative z-10">
            <div className="size-4 bg-white rounded-full border-4 border-black shadow-[0_0_15px_rgba(255,255,255,0.5)]"></div>
            <div className="absolute -top-20 -left-12 size-3 bg-primary rounded-full shadow-[0_0_10px_#f27f0d] radar-pulse"></div>
            <div className="absolute top-16 right-20 size-3 bg-primary rounded-full shadow-[0_0_10px_#f27f0d]"></div>
            <div className="absolute -bottom-14 left-16 size-3 bg-primary rounded-full shadow-[0_0_10px_#f27f0d] radar-pulse"></div>
            <div className="absolute bottom-4 -right-10 size-3 bg-primary rounded-full shadow-[0_0_10px_#f27f0d]"></div>
          </div>
        </div>
      </div>
      <div className="px-8 pb-12 flex flex-col gap-2">
        <h1 className="text-white tracking-tight text-[36px] font-bold leading-tight text-center">
          Find Local Rotations
        </h1>
        <p className="text-white/60 text-lg font-normal leading-relaxed text-center px-4">
          Real-time money sharing in your neighborhood.
        </p>
      </div>
      <div className="px-6 pb-12 pt-4">
        <Link to="/onboarding/join">
          <Button className="w-full bg-white text-black text-lg">
            Next
            <span className="material-symbols-outlined font-bold">arrow_forward</span>
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default RadarScreen;