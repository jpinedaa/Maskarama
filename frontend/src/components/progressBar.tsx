import Image from 'next/image';
import React, { useState, useEffect } from 'react';

interface ProgressBarProps {
  currentPhase: number;
  totalPhases: number;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ currentPhase, totalPhases }) => {
  const progress = ((currentPhase - 1) / (totalPhases - 1)) * 100;
  const [animatingPhase, setAnimatingPhase] = useState<number | null>(null);
  
  useEffect(() => {
    setAnimatingPhase(currentPhase);
    const timer = setTimeout(() => setAnimatingPhase(null), 1000);
    return () => clearTimeout(timer);
  }, [currentPhase]);

  const Diamond = ({ position, phase }: { position: number; phase: number }) => {
    const isFilled = currentPhase > phase;
    const isAnimating = animatingPhase === phase + 1;

    return (
      <div 
        className='absolute left-1/2 w-10 h-10'
        style={{ 
          bottom: `${position}%`, 
          transform: 'translate(-50%, 10%)'
        }}
      >
        <Image 
          src={isFilled ? `/webp/turndiamondfull.webp` : `/webp/turndiamondempty.webp`}
          alt={isFilled ? 'filled phase' : 'empty phase'}
          width={56}
          height={56}
          className={`object-contain w-10 h-10 transition-opacity duration-500 ${
            isFilled ? (isAnimating ? 'opacity-0 animate-fadeIn' : 'opacity-100') : 'opacity-50'
          }`} 
        />
      </div>
    );
  };

  return (
    <div className="w-4 h-[calc(90%)] max-h-full bg-neutral-800/40 relative -ml-2">
      <div 
        className="w-full bg-accent rounded-full transition-all duration-500 ease-out absolute top-0 mx-auto"
        style={{ height: `${progress}%` }}
      />
      <Diamond position={0} phase={3} />
      <Diamond position={33} phase={2} />
      <Diamond position={66} phase={1} />
      <Diamond position={100} phase={0} />
    </div>
  );
};

export default ProgressBar;