import os
from flask import Flask, request, jsonify, render_template, abort
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
# Enable CORS for development. For production, you might want to restrict this.
CORS(app) 

# --- Project Data ---
# In a real application, you might load this from a database or a JSON file.
# For this portfolio, managing it here is clean and simple.
PROJECTS = {
    "1": {
        "id": "1",
        "title": "Real-Time Face Mask Detection",
        "short_desc": "A CNN model to detect face masks in live video, achieving 98% accuracy.",
        "image_url": "https://placehold.co/600x400/1a1a3d/c084fc?text=Project+1",
        "overview": "This project involves building and training a Convolutional Neural Network (CNN) to accurately identify whether a person in a live video feed is wearing a face mask. The goal was to create a fast and reliable system that could be deployed in public spaces to help enforce safety regulations.",
        "challenges": "One of the main challenges was handling false positives (e.g., a hand near the face being detected as a mask). This was addressed by refining the dataset and implementing a more complex CNN architecture with additional convolutional layers to better capture facial features.",
        "tech_stack": ["Python", "TensorFlow & Keras", "OpenCV", "Scikit-learn", "NumPy"],
        "github_url": "#", # Replace with your actual GitHub URL
        "demo_url": "#" # Replace with your actual Live Demo URL
    },
    "2": {
        "id": "2",
        "title": "Movie Recommendation System",
        "short_desc": "Collaborative filtering engine using SVD to suggest movies to users.",
        "image_url": "https://placehold.co/600x400/1a1a3d/c084fc?text=Project+2",
        "overview": "This project showcases a recommendation engine built using collaborative filtering techniques. It analyzes user-item interaction data (movie ratings) to predict and recommend new movies to users, leveraging the Singular Value Decomposition (SVD) algorithm for matrix factorization.",
        "challenges": "A key challenge was the sparsity of the user-item matrix. This was mitigated by using dimensionality reduction techniques inherent in SVD, allowing the model to find latent features and make more robust recommendations.",
        "tech_stack": ["Python", "Pandas", "Scikit-learn", "Flask", "NumPy"],
        "github_url": "#",
        "demo_url": "#"
    },
    "3": {
        "id": "3",
        "title": "Sentiment Analysis on Reviews",
        "short_desc": "An NLP model using LSTMs to classify product reviews as positive or negative.",
        "image_url": "https://placehold.co/600x400/1a1a3d/c084fc?text=Project+3",
        "overview": "This Natural Language Processing (NLP) project focuses on classifying text sentiment. A Recurrent Neural Network (RNN) with Long Short-Term Memory (LSTM) units was trained on a large dataset of product reviews to determine whether the sentiment of a review is positive or negative.",
        "challenges": "Handling nuances of language like sarcasm and context was difficult. The solution involved using pre-trained word embeddings (like GloVe) to provide the model with a richer understanding of word semantics from the start.",
        "tech_stack": ["Python", "TensorFlow & Keras", "NLTK", "Pandas", "Scikit-learn"],
        "github_url": "#",
        "demo_url": "#"
    },
    "4": {
        "id": "4",
        "title": "Image Style Transfer",
        "short_desc": "Using GANs to apply the style of one image to the content of another.",
        "image_url": "https://placehold.co/600x400/1a1a3d/c084fc?text=Project+4",
        "overview": "This project explores the creative application of Generative Adversarial Networks (GANs). The model learns to separate the content of an image from its artistic style, allowing it to recompose the original content image with the style of a different artwork.",
        "challenges": "Achieving stable training with GANs was the primary difficulty. This was overcome by implementing specific techniques like spectral normalization and using a well-structured discriminator and generator architecture (like CycleGAN).",
        "tech_stack": ["Python", "PyTorch", "NumPy", "Pillow"],
        "github_url": "#",
        "demo_url": "#"
    },
    "5": {
        "id": "5",
        "title": "Automated Text Summarizer",
        "short_desc": "An extractive summarization tool using TF-IDF and sentence scoring.",
        "image_url": "https://placehold.co/600x400/1a1a3d/c084fc?text=Project+5",
        "overview": "This tool condenses long articles into a few key sentences. It works by calculating the TF-IDF (Term Frequency-Inverse Document Frequency) score for words, scoring sentences based on the weight of the words they contain, and selecting the top-scoring sentences to form the summary.",
        "challenges": "Ensuring the summary is coherent and grammatically correct was a challenge for this extractive method. While not perfect, the model's output was improved by ranking sentences not just by score but also by their original position in the text.",
        "tech_stack": ["Python", "NLTK", "Scikit-learn", "spaCy"],
        "github_url": "#",
        "demo_url": "#"
    }
}

# --- HTML Rendering Routes ---

@app.route('/')
def home():
    """
    Renders the main portfolio page (index_new.html).
    Passes a limited number of projects to the template for the preview.
    """
    # Convert projects to a list and get the first 4 for the homepage preview
    latest_projects = list(PROJECTS.values())[:4]
    return render_template('index_new.html', projects=latest_projects, total_projects=len(PROJECTS))

@app.route('/projects')
def all_projects():
    """
    Renders the page that displays all projects.
    """
    return render_template('projects_new.html', projects=PROJECTS.values())


@app.route('/project/<project_id>')
def project_detail(project_id):
    """
    Renders the detailed view for a single project.
    """
    project = PROJECTS.get(project_id)
    if not project:
        abort(404) # Return a 404 Not Found error if the project doesn't exist
    return render_template('project-detail_new.html', project=project)

# --- API Endpoint for Contact Form ---

@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Endpoint to receive form data and send it via email.
    """
    data = request.get_json()
    name, email, message = data.get('name'), data.get('email'), data.get('message')

    if not all([name, email, message]):
        return jsonify({"success": False, "error": "Missing form data"}), 400

    mail_server = os.getenv('MAIL_SERVER')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    mail_recipient = os.getenv('MAIL_RECIPIENT')

    if not all([mail_server, mail_port, mail_username, mail_password, mail_recipient]):
        print("ERROR: Email server configuration is missing in the .env file.")
        return jsonify({"success": False, "error": "Server configuration error"}), 500

    msg = MIMEMultipart()
    msg['From'] = mail_username
    msg['To'] = mail_recipient
    msg['Subject'] = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(mail_username, mail_password)
            server.send_message(msg)
        return jsonify({"success": True, "message": "Message sent successfully!"}), 200
    except smtplib.SMTPAuthenticationError:
        print("SMTP Authentication Error: Check your credentials in .env.")
        return jsonify({"success": False, "error": "Authentication error."}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500

@app.route('/diagnostic')
def diagnostic():
    """Diagnostic page to check all integrations"""
    return render_template('diagnostic.html')

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "message": "Flask app is running"}

@app.route('/test')
def simple_test():
    """Simple test page"""
    return render_template('simple-test.html')

@app.route('/old')
def old_home():
    """Old template for comparison"""
    latest_projects = list(PROJECTS.values())[:4]
    return render_template('index.html', projects=latest_projects, total_projects=len(PROJECTS))

@app.route('/projects-old')
def all_projects_old():
    """Old projects template for comparison"""
    return render_template('projects.html', projects=PROJECTS.values())

@app.route('/project-old/<project_id>')
def project_detail_old(project_id):
    """Old project detail template for comparison"""
    project = PROJECTS.get(project_id)
    if not project:
        abort(404)
    return render_template('project-detail.html', project=project)

@app.errorhandler(404)
def page_not_found(e):
    # You can create a custom 404.html page if you want
    return "<h1>404</h1><p>The page could not be found.</p>", 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)

