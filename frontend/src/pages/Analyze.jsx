import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AnimatedLogo from "../components/AnimatedLogo";
import { ArrowLeft } from "lucide-react";

export default function Analyze() {
    const [npk, setNpk] = useState({ N: 40, P: 25, K: 18 });
    const [temp, setTemp] = useState(26.4);
    const [moisture, setMoisture] = useState(44);
    const [humidity, setHumidity] = useState(58);

    const [soilType, setSoilType] = useState("Loamy");
    const [cropType, setCropType] = useState("Wheat");
    const [history, setHistory] = useState(() => {
        try {
            const raw = localStorage.getItem("sf_history");
            return raw ? JSON.parse(raw) : [];
        } catch (e) {
            return [];
        }
    });

    useEffect(() => {
        localStorage.setItem("sf_history", JSON.stringify(history));
    }, [history]);

    function handleSubmit(e) {
        e.preventDefault();
        const record = {
            id: Date.now(),
            timestamp: new Date().toLocaleString(),
            soilType,
            cropType,
            npk: { ...npk },
            temp,
            moisture,
            humidity,
        };
        setHistory((h) => [record, ...h]);
    }

    function handleClearHistory() {
        setHistory([]);
    }

    // Inline CircularGauge (uses currentColor via text-* Tailwind class applied to svg)
    const CircularGauge = ({ label, value = 0, max = 100, size = 120, colorClass = "text-teal-500" }) => {
        const strokeWidth = 10;
        const radius = (size - strokeWidth) / 2;
        const circumference = 2 * Math.PI * radius;
        const pct = max === 0 ? 0 : Math.max(0, Math.min(1, value / max));
        const dashOffset = circumference * (1 - pct);

        return (
            <div className="flex flex-col items-center gap-2">
                <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className={colorClass} aria-label={label}>
                    <g transform={`translate(${size / 2}, ${size / 2})`}>
                        <circle
                            r={radius}
                            strokeWidth={strokeWidth}
                            stroke="currentColor"
                            className="text-gray-200"
                            fill="transparent"
                        />
                        <circle
                            r={radius}
                            strokeWidth={strokeWidth}
                            stroke="currentColor"
                            className="transition-all duration-500"
                            strokeDasharray={circumference}
                            strokeDashoffset={dashOffset}
                            strokeLinecap="round"
                            fill="transparent"
                            transform="rotate(-90)"
                        />
                        <text x={0} y={4} textAnchor="middle" fontSize={16} fill="#111827" className="font-medium">
                            {Math.round(value)}
                        </text>
                    </g>
                </svg>
                <div className="text-sm text-center text-gray-700">{label}</div>
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-6xl mx-auto px-6">
                {/* Header */}
                <header className="flex items-center justify-between mb-8">
                    <div>
                        <Link to="/" className="inline-flex items-center gap-2  hover:bg-green-100 px-3 py-2 rounded-xl font-medium">
                            <span className="text-md"> <ArrowLeft /></span>
                            <span className="hidden sm:inline">Back to Home</span></Link>


                    </div>

                    <div className="flex-1 flex flex-col items-center">
                        <div className="w-30 h-30  flex items-center justify-center ">
                           <AnimatedLogo />
                        </div>

                        <h1 className="text-3xl sm:text-4xl font-extrabold text-green-600">Enter Crop Details</h1>
                        <p className="text-sm text-gray-500 mt-1">Provide information about your crop to get optimal requirements</p>
                    </div>

                    <div className="w-24" />
                </header>

                {/* MAIN CARD: gauges then form */}
                <section className="bg-white border border-gray-300 rounded-lg p-6 shadow-sm mb-6">
                    {/* Gauges centered */}
                    <div className="flex flex-col items-center">
                        <div className="flex flex-wrap justify-center md:justify-between gap-8 w-full max-w-3xl mb-6">
                            <CircularGauge label="Temperature (°C)" value={temp} max={60} size={150} colorClass="text-red-500" />
                            <CircularGauge label="Moisture (%)" value={moisture} max={100} size={150} colorClass="text-blue-500" />
                            <CircularGauge label="Humidity (%)" value={humidity} max={100} size={150} colorClass="text-blue-900" />
                        </div>

                        {/* Form below gauges (centered, constrained width) */}
                        <div className="w-full max-w-3xl">
                            <form onSubmit={handleSubmit} className="bg-white">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
                                    <label className="text-sm text-gray-700 md:col-span-1 flex items-center">Soil type</label>
                                    <select
                                        value={soilType}
                                        onChange={(e) => setSoilType(e.target.value)}
                                        className="md:col-span-2 border rounded-md px-3 py-2 w-full"
                                    >
                                        <option>Loamy</option>
                                        <option>Sandy</option>
                                        <option>Clay</option>
                                        <option>Silt</option>
                                    </select>

                                    <label className="text-sm text-gray-700 md:col-span-1 flex items-center">Crop</label>
                                    <input
                                        value={cropType}
                                        onChange={(e) => setCropType(e.target.value)}
                                        className="md:col-span-2 border rounded-md px-3 py-2 w-full"
                                    />

                                    <div className="md:col-span-3 flex gap-3 justify-start mt-2">
                                        <button type="submit" className="px-4 py-2 bg-gray-900 text-white rounded-md hover:bg-gray-800">
                                            Submit
                                        </button>
                                        <button
                                            type="button"
                                            onClick={handleClearHistory}
                                            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-400"
                                        >
                                            Clear History
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </section>

                {/* LOWER ROW: NPK box (left) and History box (right) */}
                <div className="flex flex-col md:flex-row gap-6">
                    {/* NPK box: left */}
                    <aside className="w-full md:w-1/3 border border-gray-300 rounded-lg p-6 bg-white shadow-sm">
                        <h3 className="text-lg font-medium mb-4 text-gray-800">Soil NPK</h3>

                        <div className="mb-6">
                            <div className="flex justify-between text-sm mb-2 text-gray-700">
                                <span className="font-medium">Nitrogen (N)</span>
                                <span>{npk.N}</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                                <div className="h-2 rounded-full bg-emerald-500" style={{ width: `${Math.min(100, npk.N)}%` }} />
                            </div>
                        </div>

                        <div className="mb-6">
                            <div className="flex justify-between text-sm mb-2 text-gray-700">
                                <span className="font-medium">Phosphorus (P)</span>
                                <span>{npk.P}</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                                <div className="h-2 rounded-full bg-yellow-500" style={{ width: `${Math.min(100, npk.P)}%` }} />
                            </div>
                        </div>

                        <div>
                            <div className="flex justify-between text-sm mb-2 text-gray-700">
                                <span className="font-medium">Potassium (K)</span>
                                <span>{npk.K}</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                                <div className="h-2 rounded-full bg-red-500" style={{ width: `${Math.min(100, npk.K)}%` }} />
                            </div>
                        </div>
                    </aside>

                    {/* History box: right */}
                    <section className="flex-1 border border-gray-300 rounded-lg p-6 bg-white shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                            <h4 className="text-lg font-medium text-gray-800">Prediction history</h4>
                            <div className="text-sm text-gray-500">{history.length} records</div>
                        </div>

                        <div className="max-h-64 overflow-auto divide-y">
                            {history.length === 0 && (
                                <div className="text-gray-500">No history yet — submit the form to add a record.</div>
                            )}

                            {history.map((rec) => (
                                <div key={rec.id} className="py-3">
                                    <div className="text-xs text-gray-600">{rec.timestamp}</div>
                                    <div className="font-semibold text-gray-800">
                                        {rec.cropType} — {rec.soilType}
                                    </div>
                                    <div className="text-sm text-gray-700 mt-1">
                                        N:{rec.npk.N} P:{rec.npk.P} K:{rec.npk.K} • T:{rec.temp}°C • M:{rec.moisture}% • H:{rec.humidity}%
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
}
