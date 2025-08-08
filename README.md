# TruthLens

**TruthLens** is a Chrome extension that helps users detect misinformation, bias, and logical fallacies in short-form online content such as tweets or headlines. It uses AI (via Perplexity’s API) to provide an analysis of the content’s trustworthiness.

## Features

- Paste any short text into the extension.
- Get a risk level (Low / Medium / High).
- Receive reasoning, tips, and identified fallacies.
- View suggested fact-checking sources.

## How It Works

1. User enters text in the popup UI.
2. The extension sends it to a Flask backend.
3. The backend prompts the Perplexity AI API for analysis.
4. AI returns structured results in JSON.
5. Results are shown inside the popup.

## Tech Stack

- **Frontend:** HTML, JavaScript (popup UI)
- **Backend:** Python, Flask (`app.py`)
- **AI Service:** Perplexity API (`sonar-reasoning` model)
- **Browser:** Chrome (Manifest v3)

## Setup

1. Clone the repo.
2. Run the Flask server locally:
   ```bash
   python app.py
   ```
3. Load the extension in Chrome:
   - Go to `chrome://extensions`
   - Enable "Developer Mode"
   - Click "Load unpacked" and select the folder containing the `manifest.json`
4. Paste content and click **Analyze**.

## Notes

- Make sure the Flask server is running at `http://localhost:5000`.
- The AI sources are suggestions and may not be real-time verified.
- API key is hardcoded in `app.py` – replace with environment variable in production.

## Authors
- Rami Ayoub  
- Mahmood Jazmawy