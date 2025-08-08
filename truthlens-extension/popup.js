function formatSources(rawSources) {
  if (!rawSources || rawSources === "Not specified") return "Not specified";

  // Split strictly on line breaks
  const lines = rawSources
    .split(/\r?\n/)
    .map(line => line.trim())
    .filter(line => line.length > 0);

  if (lines.length === 0) return rawSources;

  return "<ul>" + lines.map(line => `<li>${line}</li>`).join("") + "</ul>";
}

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const text = document.getElementById("inputText").value.trim();
  const resultDiv = document.getElementById("result");

  if (!text) {
    resultDiv.textContent = "Please enter some text.";
    return;
  }

  resultDiv.textContent = "Analyzing...";

  try {
    const response = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!response.ok) throw new Error("Server error");

    const data = await response.json();

    resultDiv.innerHTML = `
      <strong>Risk Level:</strong> ${data.risk}<br>
      <strong>Reason:</strong> ${data.reason}<br>
      <strong>Recommendation:</strong> ${data.tip}<br>
      <strong>Biases/Fallacies:</strong> ${data.fallacies}<br>
      <strong>Sources Checked:</strong><br>
	  <ul>
	  ${Array.isArray(data.sources) ? data.sources.map(s => `<li>${s}</li>`).join("") : `<li>${data.sources}</li>`}
	  </ul>
    `;
  } catch (err) {
    resultDiv.textContent = "Error: " + err.message;
  }
});
