import React from "react";

const CircularGauge = ({ label, value = 0, max = 100, size = 100, colorClass = "text-blue-500" }) => {
  // radius chosen to fit stroke inside the SVG viewbox
  const radius = size / 2.8;
  const circumference = 2 * Math.PI * radius;

  // safe progress: clamp and avoid division by zero
  const safeMax = max === 0 ? 1 : max;
  const clampedValue = Math.max(0, Math.min(value, safeMax));
  const progress = (clampedValue / safeMax) * circumference;

  return (
    <div className="flex flex-col items-center">
      {/* apply colorClass to svg so stroke="currentColor" uses it */}
      <svg
        width={size}
        height={size}
        className={`${colorClass}`}
        viewBox={`0 0 ${size} ${size}`}
        aria-label={label}
      >
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          className="text-gray-200"
          strokeWidth={8}
          fill="none"
        />

        {/* Foreground progress */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          className="transition-all duration-500"
          strokeWidth={8}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={Math.max(0, circumference - progress)}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>

      <span className="mt-2 font-medium">{value}</span>
      <span className="text-sm text-gray-600">{label}</span>
    </div>
  );
};

export default CircularGauge;
