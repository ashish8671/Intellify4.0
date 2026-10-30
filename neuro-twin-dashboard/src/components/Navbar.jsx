import { FaBrain } from "react-icons/fa";
import { HiStatusOnline } from "react-icons/hi";

function Navbar() {
  const currentDate = new Date().toLocaleDateString();

  return (
    <header className="bg-slate-900 border-b border-slate-700 shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

        {/* Left */}

        <div className="flex items-center gap-4">

          <div className="bg-cyan-500 p-3 rounded-xl">

            <FaBrain className="text-white text-2xl"/>

          </div>

          <div>

            <h1 className="text-3xl font-bold text-white">
              Neuro-Twin Mesh
            </h1>

            <p className="text-slate-400">
              AI Structural Health Monitoring Dashboard
            </p>

          </div>

        </div>

        {/* Right */}

        <div className="flex items-center gap-6">

          <div className="text-right">

            <p className="text-white font-semibold">
              {currentDate}
            </p>

            <p className="text-slate-400">
              Building A-12
            </p>

          </div>

          <div className="flex items-center gap-2 bg-green-500/20 text-green-400 px-4 py-2 rounded-full">

            <HiStatusOnline/>

            LIVE

          </div>

        </div>

      </div>
    </header>
  );
}

export default Navbar;