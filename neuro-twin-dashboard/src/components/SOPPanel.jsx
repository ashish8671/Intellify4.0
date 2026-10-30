import { useContext } from "react";
import {
  FaRobot,
  FaTools,
  FaClock,
  FaRupeeSign,
  FaBoxes,
  FaClipboardCheck,
  FaUserShield,
} from "react-icons/fa";

import { DetectionContext } from "../context/DetectionContext";
import { generateInspectionReport } from "../utils/pdfGenerator";

function SOPPanel() {
  const {
    selectedDetection,
    selectedSOP,
    inspection,
    statistics,
    detections,
  } = useContext(DetectionContext);

  if (!selectedDetection || !selectedSOP) {
    return (
      <div className="bg-slate-900 rounded-xl border border-slate-700 p-6">
        <h2 className="text-white text-xl font-bold">
          AI Repair Assistant
        </h2>

        <p className="text-slate-400 mt-3">
          Select a defect to view the recommended repair procedure.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-700 p-6 shadow-lg">

      <div className="flex items-center gap-3 mb-6">

        <div className="bg-cyan-500/20 p-3 rounded-lg">
          <FaRobot className="text-cyan-400 text-2xl" />
        </div>

        <div>
          <h2 className="text-white text-2xl font-bold">
            AI Repair Assistant
          </h2>

          <p className="text-slate-400">
            Standard Operating Procedure
          </p>
        </div>

      </div>

      <div className="bg-slate-800 rounded-lg p-4 mb-6">

        <h3 className="text-slate-400">
          Selected Defect
        </h3>

        <h2 className="text-white text-2xl font-bold mt-2">
          {selectedDetection.label}
        </h2>

        <span
          className={`inline-block mt-3 px-3 py-1 rounded-full text-sm
          ${
            selectedDetection.severity === "High"
              ? "bg-red-500/20 text-red-400"
              : selectedDetection.severity === "Medium"
              ? "bg-yellow-500/20 text-yellow-400"
              : "bg-green-500/20 text-green-400"
          }`}
        >
          {selectedDetection.severity}
        </span>

      </div>

      <div className="grid grid-cols-2 gap-4">

        <Card
          icon={<FaTools />}
          title="Repair Method"
          value={selectedSOP.repairMethod}
        />

        <Card
          icon={<FaClock />}
          title="Estimated Time"
          value={selectedSOP.estimatedTime}
        />

        <Card
          icon={<FaRupeeSign />}
          title="Estimated Cost"
          value={selectedSOP.estimatedCost}
        />

        <Card
          icon={<FaBoxes />}
          title="Material"
          value={selectedSOP.material}
        />

        <Card
          icon={<FaClipboardCheck />}
          title="Inspection Required"
          value={selectedSOP.inspectionRequired}
        />

        <Card
          icon={<FaUserShield />}
          title="Engineer Approval"
          value={selectedSOP.engineerApproval}
        />

      </div>

      <div className="bg-slate-800 rounded-lg p-5 mt-6">

        <h3 className="text-white font-semibold mb-2">
          Description
        </h3>

        <p className="text-slate-300">
          {selectedSOP.description}
        </p>

      </div>

      <button
        onClick={() =>
          generateInspectionReport({
            inspection,
            statistics,
            detections,
          })
        }
        className="w-full mt-6 bg-cyan-500 hover:bg-cyan-600 transition-all py-3 rounded-lg font-semibold text-white"
      >
        📄 Generate Inspection Report
      </button>

    </div>
  );
}

function Card({ icon, title, value }) {
  return (
    <div className="bg-slate-800 rounded-lg p-4 flex gap-3">

      <div className="text-cyan-400 text-xl mt-1">
        {icon}
      </div>

      <div>
        <p className="text-slate-400 text-sm">
          {title}
        </p>

        <h3 className="text-white font-semibold">
          {value}
        </h3>
      </div>

    </div>
  );
}

export default SOPPanel;