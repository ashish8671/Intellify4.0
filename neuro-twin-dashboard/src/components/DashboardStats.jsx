import { useContext } from "react";
import { DetectionContext } from "../context/DetectionContext";
import StatCard from "./StatCard";
import {
  FaBug,
  FaExclamationTriangle,
  FaTools,
  FaCheckCircle,
} from "react-icons/fa";

function DashboardStats() {
  const { statistics } = useContext(DetectionContext);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6 mb-6">

      <StatCard
        title="Total Defects"
        value={statistics.total}
        icon={<FaBug />}
        color="text-cyan-400"
        bg="bg-cyan-500/10"
      />

      <StatCard
        title="High Risk"
        value={statistics.high}
        icon={<FaExclamationTriangle />}
        color="text-red-500"
        bg="bg-red-500/10"
      />

      <StatCard
        title="Medium Risk"
        value={statistics.medium}
        icon={<FaTools />}
        color="text-yellow-400"
        bg="bg-yellow-500/10"
      />

      <StatCard
        title="Low Risk"
        value={statistics.low}
        icon={<FaCheckCircle />}
        color="text-green-500"
        bg="bg-green-500/10"
      />

    </div>
  );
}

export default DashboardStats;