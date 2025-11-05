from flask import Flask, request, render_template
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Set up Gemini
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["query"]
        result = model.invoke(user_input)
        response = result.content
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)


