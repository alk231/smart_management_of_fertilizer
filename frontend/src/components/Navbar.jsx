// src/components/Navbar.jsx
import { Link } from "react-router-dom";
import { Home } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex items-center gap-8 text-white px-8 py-3 rounded-2xl backdrop-blur-md bg-white/10 shadow-lg">
      {/* Home */}
      <Link to="/" className="flex items-center gap-2 hover:text-orange-400 transition">
        <Home className="h-5 w-5" />
        <span className="font-semibold text-lg">Home</span>
      </Link>

      <Link to="/about" className="hover:text-orange-400 transition font-medium">
        About
      </Link>

      <Link to="/store" className="hover:text-orange-400 transition font-medium">
        Store
      </Link>
    </nav>
  );
}
