import { useContext } from "react";
import { DetectionContext } from "../context/DetectionContext";

import {
  FaExclamationTriangle,
  FaCheckCircle,
  FaTools,
  FaArrowRight,
} from "react-icons/fa";

function SeverityPanel() {
  const {
    detections,
    selectedDetection,
    setSelectedDetection,
  } = useContext(DetectionContext);

  const getIcon = (severity) => {
    switch (severity) {
      case "High":
        return <FaExclamationTriangle className="text-red-500" />;

      case "Medium":
        return <FaTools className="text-yellow-400" />;

      default:
        return <FaCheckCircle className="text-green-500" />;
    }
  };

  const getBorderColor = (severity) => {
    switch (severity) {
      case "High":
        return "border-red-500";

      case "Medium":
        return "border-yellow-400";

      default:
        return "border-green-500";
    }
  };

  const getBackground = (severity) => {
    switch (severity) {
      case "High":
        return "bg-red-500/10";

      case "Medium":
        return "bg-yellow-500/10";

      default:
        return "bg-green-500/10";
    }
  };

  const getPriority = (severity) => {
    switch (severity) {
      case "High":
        return "Immediate";

      case "Medium":
        return "Planned";

      default:
        return "Monitor";
    }
  };

  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-700 shadow-xl overflow-hidden h-[520px] flex flex-col">

      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-700 flex-shrink-0">

        <div className="flex items-center justify-between">

          <div>
            <h2 className="text-lg font-bold text-white">
              Detected Defects
            </h2>

            <p className="text-slate-400 text-xs mt-1">
              {detections.length} defect
              {detections.length !== 1 ? "s" : ""} detected
            </p>
          </div>

          <div className="bg-slate-800 px-3 py-1 rounded-full">
            <span className="text-cyan-400 text-sm font-semibold">
              {detections.length}
            </span>
          </div>

        </div>

      </div>

      {/* Scrollable defect list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">

        {detections.map((item, index) => (

          <div
            key={item.id}
            onClick={() => setSelectedDetection(item)}
            className={`
              cursor-pointer
              rounded-xl
              border
              p-3
              transition-all
              duration-200
              ${getBorderColor(item.severity)}
              ${getBackground(item.severity)}
              ${
                selectedDetection?.id === item.id
                  ? "ring-2 ring-cyan-400"
                  : ""
              }
              hover:bg-slate-800/70
            `}
          >

            {/* Defect header */}
            <div className="flex items-center justify-between">

              <div className="flex items-center gap-2 min-w-0">

                <div className="text-lg flex-shrink-0">
                  {getIcon(item.severity)}
                </div>

                <div className="min-w-0">

                  <h3 className="text-white font-semibold text-sm truncate">
                    {item.label} #{index + 1}
                  </h3>

                  <p className="text-slate-400 text-xs">
                    Confidence:{" "}
                    <span className="text-white">
                      {item.confidence}%
                    </span>
                  </p>

                </div>

              </div>

              <FaArrowRight className="text-slate-500 text-xs flex-shrink-0" />

            </div>

            {/* Information grid */}
            <div className="mt-3 grid grid-cols-2 gap-2">

              <Info
                title="Severity"
                value={item.severity || "Unknown"}
              />

              <Info
                title="Status"
                value="Detected"
              />

              <Info
                title="Location"
                value={
                  item.x !== undefined && item.y !== undefined
                    ? `X: ${Number(item.x).toFixed(2)}%  Y: ${Number(
                        item.y
                      ).toFixed(2)}%`
                    : "Not available"
                }
              />

              <Info
                title="Priority"
                value={getPriority(item.severity)}
              />

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

function Info({ title, value }) {
  return (
    <div className="bg-slate-800 rounded-lg px-3 py-2 min-w-0">

      <p className="text-slate-500 text-[10px] uppercase tracking-wide">
        {title}
      </p>

      <p className="text-white text-xs font-medium mt-1 break-words">
        {value}
      </p>

    </div>
  );
}

export default SeverityPanel;
