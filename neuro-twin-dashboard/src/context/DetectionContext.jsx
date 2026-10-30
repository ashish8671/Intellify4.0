import { createContext, useMemo, useState } from "react";
import detectionsData from "../data/detections.json";
import sopData from "../data/sop.json";
import inspection from "../data/inspection.json";
import { predictImage } from "../services/detectionService";

export const DetectionContext = createContext();

export function DetectionProvider({ children }) {

    // Detected defects
    const [detections, setDetections] = useState(detectionsData);

    // Currently selected defect
    const [selectedDetection, setSelectedDetection] = useState(
        detectionsData.length > 0 ? detectionsData[0] : null
    );

    // Uploaded image
    const [uploadedImage, setUploadedImage] = useState(null);

    // AI loading state
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    // Error message
    const [error, setError] = useState(null);


    // ==========================================
    // DASHBOARD STATISTICS
    // ==========================================

    const statistics = useMemo(() => {

        const total = detections.length;

        const high = detections.filter(
            (item) => item.severity === "High"
        ).length;

        const medium = detections.filter(
            (item) => item.severity === "Medium"
        ).length;

        const low = detections.filter(
            (item) => item.severity === "Low"
        ).length;

        return {
            total,
            high,
            medium,
            low,
        };

    }, [detections]);


    // ==========================================
    // SELECTED DEFECT SOP
    // ==========================================

    const selectedSOP = useMemo(() => {

        if (!selectedDetection) {
            return null;
        }

        // Prefer SOP returned by AI
        if (selectedDetection.sop) {
            return selectedDetection.sop;
        }

        // Fallback to local SOP data
        return (
            sopData[selectedDetection.label] || {
                repairMethod: "No SOP Available",
                priority: "N/A",
                estimatedTime: "-",
                estimatedCost: "-",
                material: "-",
                description: "-",
                inspectionRequired: "-",
                engineerApproval: "-"
            }
        );

    }, [selectedDetection]);


    // ==========================================
    // AI IMAGE ANALYSIS
    // ==========================================

    const analyzeImage = async (file) => {

        if (!file) {
            return;
        }

        setIsAnalyzing(true);
        setError(null);

        try {

            // Create preview
            const imageURL = URL.createObjectURL(file);
            setUploadedImage(imageURL);

            // Send image to FastAPI
            const result = await predictImage(file);

            console.log("Neuro-Twin AI Response:", result);

            // Check API response
            if (result.error) {
                throw new Error(result.error);
            }

            // Update detections
            const newDetections = result.detections || [];

            setDetections(newDetections);

            // Automatically select first defect
            if (newDetections.length > 0) {
                setSelectedDetection(newDetections[0]);
            } else {
                setSelectedDetection(null);
            }

        } catch (err) {

            console.error("AI analysis error:", err);

            setError(
                err.message || "Unable to analyze image"
            );

        } finally {

            setIsAnalyzing(false);

        }
    };


    // ==========================================
    // CONTEXT VALUE
    // ==========================================

    const value = {

        detections,
        setDetections,

        selectedDetection,
        setSelectedDetection,

        statistics,

        selectedSOP,

        inspection,

        uploadedImage,

        isAnalyzing,

        error,

        analyzeImage
    };


    return (
        <DetectionContext.Provider value={value}>
            {children}
        </DetectionContext.Provider>
    );
}
