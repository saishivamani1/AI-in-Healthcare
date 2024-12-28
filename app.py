from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import google.generativeai as genai
import os

model = genai.GenerativeModel('gemini-pro')

# Configuration for Streamlit
STREAMLIT_PORT = 8501  # Default Streamlit port
STREAMLIT_SCRIPT = r"C:\Users\DELL\Desktop\WEB REAPERS\Report_analysis.py"  # Streamlit script path

STREAMLIT_PORT2 = 8502  # Default Streamlit port
STREAMLIT_SCRIPT2 = r"C:\Users\DELL\Desktop\WEB REAPERS\Data_Analytics.py"

STREAMLIT_PORT3 = 8503 
STREAMLIT_SCRIPT3 = r"C:\Users\DELL\Desktop\WEB REAPERS\predictor.py"


my_api_key_gemini = "api-key"

genai.configure(api_key=my_api_key_gemini)

app = Flask(__name__)

# Define your 404 error handler to redirect to the index page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            prompt = request.form['prompt']
            question = prompt

            response = model.generate_content(question)

            if response.text:
                return response.text
            else:
                return "Sorry, but I think Gemini didn't want to answer that!"
        except Exception as e:
            return "Sorry, but Gemini didn't want to answer that!"

    return render_template('hc.html', **locals())


@app.route("/streamlit")
def streamlit_redirect():
    """Redirects to the Streamlit app."""
    return redirect(f"http://localhost:{STREAMLIT_PORT}")

@app.route("/streamlit2")
def streamlit_redirect2():
    """Redirects to the Streamlit app."""
    return redirect(f"http://localhost:{STREAMLIT_PORT2}")

@app.route("/streamlit3")
def streamlit_redirect3():
    """Redirects to the Streamlit app."""
    return redirect(f"http://localhost:{STREAMLIT_PORT3}")


if __name__ == "__main__":
    # Start Streamlit in a separate subprocess
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", STREAMLIT_SCRIPT, "--server.port", str(STREAMLIT_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    streamlit_process2 = subprocess.Popen(
        ["streamlit", "run", STREAMLIT_SCRIPT2, "--server.port", str(STREAMLIT_PORT2)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    streamlit_process3 = subprocess.Popen(
        ["streamlit", "run", STREAMLIT_SCRIPT3, "--server.port", str(STREAMLIT_PORT3)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Run the Flask app
        app.run(debug=True, use_reloader=False)
    finally:
        # Terminate Streamlit when Flask app stops
        streamlit_process.terminate()
