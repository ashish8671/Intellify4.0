const API_URL = "http://localhost:8000";

export async function predictImage(file) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("AI prediction failed");
    }

    return response.json();
}
