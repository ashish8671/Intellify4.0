import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { useContext } from "react";
import { DetectionContext } from "../context/DetectionContext";

ChartJS.register(ArcElement, Tooltip, Legend);

function DefectChart() {
  const { statistics } = useContext(DetectionContext);

  const data = {
    labels: ["High", "Medium", "Low"],
    datasets: [
      {
        data: [
          statistics.high,
          statistics.medium,
          statistics.low,
        ],
        backgroundColor: [
          "#ef4444",
          "#facc15",
          "#22c55e",
        ],
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-700 p-6 mt-6">
      <h2 className="text-xl font-bold text-white mb-6">
        Defect Distribution
      </h2>

      <div className="max-w-xs mx-auto">
        <Pie data={data} />
      </div>
    </div>
  );
}

export default DefectChart;