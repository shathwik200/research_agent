from flask import Flask, render_template, request
import markdown
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(os.getenv('MODEL'))

def read_markdown_file():
    report_path = os.path.join(os.path.dirname(__file__), 'report.md')
    if os.path.exists(report_path):
        with open(report_path, 'r') as file:
            content = file.read()
            return markdown.markdown(content)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    content = None
    if request.method == 'POST':
        topic = request.form.get('topic')
        try:
            # Generate research content using Gemini
            prompt = f"Write a detailed research report about {topic} with latest trends and developments"
            response = model.generate_content(prompt)
            
            # Save to markdown file
            with open('report.md', 'w') as f:
                f.write(response.text)
            
            content = markdown.markdown(response.text)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
