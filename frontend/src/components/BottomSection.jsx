import { Link } from "react-router-dom";
import { Sprout, Target, BarChart2, Leaf } from "lucide-react";

const items = [
  {
    id: 1,
    Icon: Sprout,
    title: "Crop Analysis",
    desc: "Get detailed insights about your crop's optimal growing conditions",
  },
  {
    id: 2,
    Icon: Target,
    title: "Precise Requirements",
    desc: "Receive accurate water, fertilizer, and temperature recommendations",
  },
  {
    id: 3,
    Icon: BarChart2,
    title: "Yield Prediction",
    desc: "Estimate your expected crop yield based on field conditions",
  },
  {
    id: 4,
    Icon: Leaf,
    title: "Soil Optimization",
    desc: "Learn about the ideal soil pH and type for your crops",
  },
];

export default function BottomSection() {
  return (
    <section className="bg-white py-24">
      <div className="max-w-7xl mx-auto px-6">
        {/* Heading */}
        <div className="text-center mb-12">
          <h2 className="text-4xl sm:text-5xl font-extrabold text-emerald-600">
            How It Works
          </h2>
          <p className="mt-4 text-gray-600 max-w-2xl mx-auto">
            Three simple steps to optimize your crop management
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {items.map(({ id, Icon, title, desc }) => (
            <article
              key={id}
              className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm hover:shadow-lg transition-transform transform hover:-translate-y-1"
            >
              <div className="mb-6 h-12 w-12 rounded-lg bg-emerald-50 flex items-center justify-center">
                <Icon className="h-6 w-6 text-emerald-600" />
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                {title}
              </h3>
              <p className="text-sm text-gray-600 leading-relaxed">{desc}</p>
            </article>
          ))}
        </div>

        {/* CTA Section */}
        <div className="bg-emerald-600 rounded-2xl py-14 px-6 text-center shadow-md">
          <h3 className="text-2xl sm:text-3xl font-extrabold text-white mb-4">
            Ready to optimize your crops?
          </h3>
          <p className="text-white/90 text-lg mb-8 max-w-2xl mx-auto">
            Start analyzing your crop requirements today and maximize your yield
          </p>

          <Link
            to="/analyze"
            className="inline-block rounded-xl bg-orange-500 px-8 py-4 text-lg font-semibold text-white shadow-md hover:bg-orange-600 focus:outline-none focus:ring-4 focus:ring-orange-300 transition"
          >
            Analyze Your Crop
          </Link>
        </div>
      </div>
    </section>
  );
}
