import React from 'react';

interface OshvaLogoProps {
  size?: number;
  className?: string;
  animate?: boolean;
}

export const OshvaLogo: React.FC<OshvaLogoProps> = ({ 
  size = 40, 
  className = "", 
  animate = false 
}) => {
  return (
    <div 
      className={`relative inline-flex items-center justify-center ${className}`}
      style={{ width: size, height: size }}
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        className={animate ? "animate-spin" : ""}
        style={{ animationDuration: animate ? "3s" : undefined }}
      >
        {/* Blue segment (top) */}
        <path
          d="M 50 10 A 40 40 0 0 1 85.36 35 L 50 50 Z"
          fill="#2563eb"
          className="drop-shadow-sm"
        />
        
        {/* Orange segment (bottom-right) */}
        <path
          d="M 85.36 35 A 40 40 0 0 1 50 90 L 50 50 Z"
          fill="#ea580c"
          className="drop-shadow-sm"
        />
        
        {/* Green segment (bottom-left) */}
        <path
          d="M 50 90 A 40 40 0 0 1 14.64 35 L 50 50 Z"
          fill="#059669"
          className="drop-shadow-sm"
        />
        
        {/* Central wellness symbol */}
        <circle
          cx="50"
          cy="50"
          r="8"
          fill="white"
          className="drop-shadow-md"
        />
        
        {/* Inner wellness dot */}
        <circle
          cx="50"
          cy="50"
          r="3"
          fill="#1f2937"
          className="opacity-80"
        />
      </svg>
      
      {/* Pulsing effect overlay for loading states */}
      {animate && (
        <div 
          className="absolute inset-0 rounded-full bg-gradient-to-br from-blue-500/20 via-orange-500/20 to-green-500/20 animate-pulse"
          style={{ width: size, height: size }}
        />
      )}
    </div>
  );
};

export default OshvaLogo;