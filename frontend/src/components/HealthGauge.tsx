import React from 'react';

interface HealthGaugeProps {
  score: number;
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const HealthGauge: React.FC<HealthGaugeProps> = ({ score, label = "Code Health", size = 'md' }) => {
  const getColor = (val: number) => {
    if (val >= 85) return { stroke: '#06b6d4', text: 'text-cyan-400', badge: 'bg-cyan-950 text-cyan-400 border-cyan-800' };
    if (val >= 70) return { stroke: '#f59e0b', text: 'text-amber-400', badge: 'bg-amber-950 text-amber-400 border-amber-800' };
    return { stroke: '#ef4444', text: 'text-rose-400', badge: 'bg-rose-950 text-rose-400 border-rose-800' };
  };

  const style = getColor(score);
  const strokeWidth = size === 'lg' ? 12 : 8;
  const radius = size === 'lg' ? 60 : 40;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative flex items-center justify-center">
        <svg className="transform -rotate-90" width={radius * 2.5} height={radius * 2.5}>
          <circle
            cx={radius * 1.25}
            cy={radius * 1.25}
            r={radius}
            stroke="#1f2937"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          <circle
            cx={radius * 1.25}
            cy={radius * 1.25}
            r={radius}
            stroke={style.stroke}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute text-center">
          <span className={`font-extrabold ${size === 'lg' ? 'text-3xl' : 'text-xl'} ${style.text}`}>
            {score}
          </span>
          <span className="text-xs text-slate-500 font-bold block">/ 100</span>
        </div>
      </div>
      <span className="text-xs font-semibold text-slate-400 mt-2">{label}</span>
    </div>
  );
};
