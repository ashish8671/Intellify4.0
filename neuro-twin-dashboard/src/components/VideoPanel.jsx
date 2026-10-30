import { useContext, useState } from "react";
import { DetectionContext } from "../context/DetectionContext";
import {
  FaUpload,
  FaExpand,
  FaDownload,
  FaSearchPlus,
} from "react-icons/fa";

const API_URL = "http://localhost:8000";

function VideoPanel() {
  const {
    detections,
    selectedDetection,
    setSelectedDetection,
    setDetections,
  } = useContext(DetectionContext);

  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setError("");
    setLoading(true);

    // Display uploaded image
    const imageUrl = URL.createObjectURL(file);
    setImage(imageUrl);

    try {
      const formData = new FormData();

	formData.append("file", file);
	formData.append("user_id", "1");
	formData.append("building_id", "1");
	formData.append("inspection_date", "2026-08-11");
	formData.append("location", "Pune");

      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("AI prediction failed");
      }

      const data = await response.json();

      console.log("AI Response:", data);

      // Get image dimensions
      const img = new Image();

      img.onload = () => {
        const imageWidth = img.width;
        const imageHeight = img.height;

        // Convert backend pixel bounding boxes
        // into percentages for the dashboard
        const formattedDetections = data.detections.map((item) => {
          const bbox = item.bbox;

          const x = (bbox.x1 / imageWidth) * 100;
          const y = (bbox.y1 / imageHeight) * 100;

          const width =
            ((bbox.x2 - bbox.x1) / imageWidth) * 100;

          const height =
            ((bbox.y2 - bbox.y1) / imageHeight) * 100;

          let color = "#facc15";

          if (item.severity === "High") {
            color = "#ef4444";
          } else if (item.severity === "Medium") {
            color = "#facc15";
          } else if (item.severity === "Low") {
            color = "#22c55e";
          }

          return {
            ...item,
            x,
            y,
            width,
            height,
            color,
          };
        });

        console.log(
          "Formatted detections:",
          formattedDetections
        );

        setDetections(formattedDetections);

        if (formattedDetections.length > 0) {
          setSelectedDetection(formattedDetections[0]);
        } else {
          setSelectedDetection(null);
        }

        setLoading(false);
      };

      img.src = imageUrl;

    } catch (err) {
      console.error(err);

      setError(
        "Unable to connect to Neuro-Twin AI backend."
      );

      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 rounded-2xl border border-slate-700 shadow-xl overflow-hidden">

      {/* Header */}

      <div className="flex justify-between items-center px-6 py-4 border-b border-slate-700">

        <div>
          <h2 className="text-xl font-semibold text-white">
            AI Inspection Viewer
          </h2>

          <p className="text-slate-400 text-sm">
            Upload structural image for AI visualization
          </p>
        </div>

        <span className="bg-green-500/20 text-green-400 px-4 py-1 rounded-full text-sm">
          {loading ? "Analyzing..." : "AI Ready"}
        </span>

      </div>

      {/* Toolbar */}

      <div className="flex gap-3 px-6 py-4 border-b border-slate-700">

        <label className="bg-cyan-500 hover:bg-cyan-600 transition cursor-pointer px-4 py-2 rounded-lg flex items-center gap-2 text-white">

          <FaUpload />

          {loading ? "Analyzing..." : "Upload & Analyze"}

          <input
            hidden
            type="file"
            accept="image/*"
            onChange={handleUpload}
            disabled={loading}
          />

        </label>

        <button className="bg-slate-800 hover:bg-slate-700 p-3 rounded-lg">
          <FaSearchPlus />
        </button>

        <button className="bg-slate-800 hover:bg-slate-700 p-3 rounded-lg">
          <FaExpand />
        </button>

        <button className="bg-slate-800 hover:bg-slate-700 p-3 rounded-lg">
          <FaDownload />
        </button>

      </div>

      {/* Error */}

      {error && (
        <div className="px-6 py-3 bg-red-500/10 border-b border-red-500/30 text-red-400">
          {error}
        </div>
      )}

      {/* Viewer */}

      <div className="relative h-[520px] bg-slate-950">

        {image ? (
          <div className="relative w-full h-full">

            <img
              src={image}
              alt="Inspection"
              className="w-full h-full object-contain"
            />

            {detections.map((item) => (
              <div
                key={item.id}
                onClick={() => setSelectedDetection(item)}
                className={`absolute border-[3px] rounded-lg cursor-pointer transition-all duration-300 ${
                  selectedDetection?.id === item.id
                    ? "scale-105 shadow-2xl"
                    : ""
                }`}
                style={{
                  left: `${item.x}%`,
                  top: `${item.y}%`,
                  width: `${item.width}%`,
                  height: `${item.height}%`,
                  borderColor: item.color,
                }}
              >

                <span
                  className="absolute -top-7 left-0 text-xs px-2 py-1 rounded text-white whitespace-nowrap"
                  style={{
                    backgroundColor: item.color,
                  }}
                >
                  {item.label} ({item.confidence}%)
                </span>

              </div>
            ))}

          </div>

        ) : (

          <div className="w-full h-full flex items-center justify-center">

            <div className="text-center">

              <FaUpload className="mx-auto text-6xl text-slate-600 mb-5" />

              <h3 className="text-white text-xl font-semibold">
                Upload Inspection Image
              </h3>

              <p className="text-slate-400 mt-2">
                JPG • PNG • JPEG
              </p>

            </div>

          </div>

        )}

      </div>

      {/* Footer */}

      <div className="grid grid-cols-4 border-t border-slate-700">

        <FooterCard
          title="Objects"
          value={detections.length}
        />

        <FooterCard
          title="Model"
          value="YOLOv11"
        />

        <FooterCard
          title="Confidence"
          value={
            selectedDetection
              ? `${selectedDetection.confidence}%`
              : "-"
          }
        />

        <FooterCard
          title="Inference"
          value="AI"
        />

      </div>

    </div>
  );
}

function FooterCard({ title, value }) {
  return (
    <div className="text-center p-4 border-r border-slate-700 last:border-r-0">

      <p className="text-slate-400 text-sm">
        {title}
      </p>

      <h3 className="text-white font-semibold mt-1">
        {value}
      </h3>

    </div>
  );
}

export default VideoPanel;
