from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Get the Groq API key from an environment variable
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "response": "Please enter a message."
            })

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": """You are a concise AI shopping assistant.

Rules:
- Give short, direct answers.
- Usually answer in 3 to 6 sentences or bullet points.
- Do not give long explanations unless the user asks.
- For shopping recommendations, give at most 3 products.
- Mention price and one key reason when useful.
- For budgets, keep calculations simple and accurate.
- Use Indian Rupees (₹) when discussing money.
- Be friendly and helpful.
- If the user asks to compare products, clearly show the differences.
- Do not invent exact current prices if you are not given reliable price information."""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=250,
            temperature=0.5
        )

        answer = response.choices[0].message.content

        return jsonify({
            "response": answer
        })

    except Exception as e:
        print("Error:", e)

        return jsonify({
            "response": "Sorry, I couldn't process your request right now. Please try again."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)