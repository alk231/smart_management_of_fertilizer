// src/pages/Home.jsx

import Navbar from "../components/NavBar";
import { ArrowRight } from "lucide-react";
import AnimatedPlant from "./AnimatedPlant";

const scrollToBottom = () => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: "smooth", // smooth scrolling
    block: "end",       // aligns to bottom
  });
};


export default function Hero() {
  return (
    <header className="relative min-h-screen overflow-hidden">

      {/* Navbar */}
      <Navbar />

      {/* Background image */}
      <img
        src="/hero-bg.jpg"
        alt="Field background"
        className="absolute inset-0 w-full h-full object-cover object-center"
        loading="eager"
        draggable="false"
      />

      {/* Colored overlay (green) + optional blur */}
      <div
        aria-hidden="true"
        className="absolute inset-0 bg-green-700/60 backdrop-blur-sm"
      />

      {/* Content */}
      <div className="relative z-10 flex min-h-screen items-center justify-center px-6">
        <div className="text-center max-w-4xl">
          {/* Icon in circle */}
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center ">
            {/* use any lucide-react icon */}
            <div className="w-30 h-30">
              <AnimatedPlant size={120} />
            </div>
            {/* or <ArrowRight className="h-6 w-6 text-white" /> */}
          </div>

          {/* Headline */}
          <h1 className="mb-4 text-white text-5xl sm:text-6xl md:text-7xl font-extrabold leading-tight drop-shadow-lg">
            Smart Crop Management
          </h1>

          {/* Subtitle */}
          <p className="mx-auto mb-8 max-w-2xl text-white/90 text-lg sm:text-xl">
            Optimize your crop yield with data-driven insights and
            recommendations
          </p>

          {/* CTA */}
          <div className="flex justify-center">

            <button className="inline-flex items-center gap-3 rounded-2xl bg-orange-500 px-6 py-3 text-white text-lg font-medium shadow-lg hover:bg-orange-600 focus:outline-none focus:ring-4 focus:ring-orange-300 transition" onClick={scrollToBottom}>
              <span>Get Started</span>
              <ArrowRight className="h-5 w-5" />

            </button>


          </div>
        </div>
      </div>
    </header>
  );
}
