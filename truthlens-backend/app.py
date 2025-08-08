from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Load API key (replace with env var in production)
PERPLEXITY_API_KEY = "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"

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
    "Content-Type": "application/json"
}


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"""
You are an AI content analyst.

Your task is to review the following short-form content (such as a tweet, headline, or news post) and return your response strictly in JSON format using these exact keys:
- "risk": (Low / Medium / High)
- "reason": (What do you conclude about the content? Base your opinion on reasoning and available evidence. Do not attempt to hedge or soften the conclusion. Your job is not to be politically correct but to speak truthfully and analytically.)
- "tip": (What the user should consider doing or reading next)
- "fallacies": (List any cognitive biases or logical fallacies used in the content)
- "sources": (List of websites, fact-checking platforms, organizations, or databases you would use to verify this claim, don't use simulated sources )

Do not include any explanation, thinking process, or comments before or after the JSON object. The output must begin with '{{' and end with '}}' only.
CONTENT:
\"\"\"{text}\"\"\"
"""

    payload = {
        "model": "sonar-reasoning",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(PERPLEXITY_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()

        raw_reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        print("Raw reply from AI:\n", raw_reply)

        # Extract only the JSON part of the response
        json_start = raw_reply.find("{")
        json_end = raw_reply.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            return jsonify({"error": "No JSON found in response", "raw": raw_reply}), 500

        json_string = raw_reply[json_start:json_end]

        try:
            ai_data = json.loads(json_string)
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "Failed to parse AI response as JSON",
                "raw_response": raw_reply,
                "json_attempt": json_string,
                "exception": str(e)
            }), 500

        return jsonify({
            "risk": ai_data.get("risk", "Unknown"),
            "reason": ai_data.get("reason", "No reason provided."),
            "tip": ai_data.get("tip", "No tip provided."),
            "fallacies": ai_data.get("fallacies", "None detected."),
            "sources": ai_data.get("sources", "No sources listed.")
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
