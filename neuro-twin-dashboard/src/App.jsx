import Navbar from "./components/Navbar";
import DashboardStats from "./components/DashboardStats";
import InspectionCard from "./components/InspectionCard";
import VideoPanel from "./components/VideoPanel";
import SeverityPanel from "./components/SeverityPanel";
import SOPPanel from "./components/SOPPanel";
import DefectChart from "./components/DefectChart";

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navbar */}
      <Navbar />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-6 py-6">

        {/* Dashboard Statistics */}
        <DashboardStats />

        {/* Inspection Information */}
        <InspectionCard />

        {/* Main Dashboard */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

          {/* Left Side - Video Panel */}
          <div className="lg:col-span-2 min-w-0">
            <VideoPanel />
          </div>

          {/* Right Side - Defect List */}
          <div>
            <SeverityPanel />
          </div>

        </div>

        {/* SOP Recommendation */}
        <div className="mt-6">
          <SOPPanel />
        </div>
        
      </main>

    </div>
  );
}

export default App;
