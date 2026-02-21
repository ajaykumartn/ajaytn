import os
import json
import time
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiofiles
from pathlib import Path
from functools import lru_cache

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Portfolio API", 
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware (must be before other middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY', 'your-secret-key-change-this'))

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static files (must be before routes)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configuration
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads" / "projects"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
DATA_FILE = str(BASE_DIR / 'data' / 'portfolio_data.json')

# Create necessary directories on startup
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
(BASE_DIR / 'data').mkdir(parents=True, exist_ok=True)

# Ensure data file exists
if not Path(DATA_FILE).exists():
    # Create default empty data structure
    default_data = {
        "about": {},
        "projects": [],
        "skills": {},
        "experience": [],
        "achievements": {}
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(default_data, f, indent=2)

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class AboutData(BaseModel):
    name: str
    title: str
    desc1: str
    desc2: str
    desc3: str
    years: str
    projects_count: str
    technologies: Optional[str] = "5+"

class SkillsData(BaseModel):
    languages: str
    aiml: str
    datascience: str
    tools: str

class AchievementsData(BaseModel):
    ach1_title: str
    ach1_desc: str
    ach2_title: str
    ach2_desc: str
    cert1_title: str
    cert1_details: str
    cert2_title: str
    cert2_details: str

class ProjectData(BaseModel):
    title: str
    short_desc: str
    image_url: str
    overview: str
    challenges: str
    tech_stack: str
    github_url: str
    demo_url: str

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

# Helper functions
@lru_cache(maxsize=1)
def load_portfolio_data():
    """Load portfolio data from JSON file with caching"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_portfolio_data(data):
    """Save portfolio data to JSON file and clear cache"""
    data_dir = BASE_DIR / 'data'
    data_dir.mkdir(exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    # Clear cache after saving
    load_portfolio_data.cache_clear()

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def get_current_user(request: Request):
    """Dependency to check if user is logged in"""
    if not request.session.get('admin_logged_in'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return True

# Old projects data (fallback)
PROJECTS = {
    "1": {
        "id": "1",
        "title": "Real-Time Face Mask Detection",
        "short_desc": "A CNN model to detect face masks in live video, achieving 98% accuracy.",
        "image_url": "https://placehold.co/600x400/1a1a3d/c084fc?text=Project+1",
        "overview": "This project involves building and training a Convolutional Neural Network (CNN) to accurately identify whether a person in a live video feed is wearing a face mask.",
        "challenges": "One of the main challenges was handling false positives. This was addressed by refining the dataset and implementing a more complex CNN architecture.",
        "tech_stack": ["Python", "TensorFlow & Keras", "OpenCV", "Scikit-learn", "NumPy"],
        "github_url": "#",
        "demo_url": "#"
    }
}

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main portfolio page"""
    portfolio_data = load_portfolio_data()
    projects_list = portfolio_data.get('projects', list(PROJECTS.values()))
    latest_projects = projects_list[:4]
    
    return templates.TemplateResponse("index_new.html", {
        "request": request,
        "projects": latest_projects,
        "total_projects": len(projects_list),
        "about": portfolio_data.get('about', {}),
        "skills": portfolio_data.get('skills', {}),
        "experience": portfolio_data.get('experience', []),
        "achievements": portfolio_data.get('achievements', {})
    })

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Render the contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get("/projects", response_class=HTMLResponse)
async def all_projects(request: Request):
    """Render all projects page"""
    portfolio_data = load_portfolio_data()
    projects_list = portfolio_data.get('projects', list(PROJECTS.values()))
    return templates.TemplateResponse("projects_new.html", {
        "request": request,
        "projects": projects_list
    })

@app.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    """Render project detail page"""
    portfolio_data = load_portfolio_data()
    projects_list = portfolio_data.get('projects', list(PROJECTS.values()))
    
    # Find project by ID
    project = None
    for p in projects_list:
        if str(p.get('id')) == str(project_id):
            project = p
            break
    
    # Fallback to old PROJECTS dict
    if not project:
        project = PROJECTS.get(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return templates.TemplateResponse("project-detail_new.html", {
        "request": request,
        "project": project
    })

@app.post("/send-email")
async def send_email(contact_data: ContactForm):
    """Send contact form email"""
    mail_server = os.getenv('MAIL_SERVER')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    mail_recipient = os.getenv('MAIL_RECIPIENT')

    if not all([mail_server, mail_port, mail_username, mail_password, mail_recipient]):
        raise HTTPException(status_code=500, detail="Email server configuration error")

    msg = MIMEMultipart()
    msg['From'] = mail_username
    msg['To'] = mail_recipient
    msg['Subject'] = f"New Contact Form Submission from {contact_data.name}"
    body = f"Name: {contact_data.name}\nEmail: {contact_data.email}\n\nMessage:\n{contact_data.message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(mail_server, mail_port) as server:
            server.starttls()
            server.login(mail_username, mail_password)
            server.send_message(msg)
        return {"success": True, "message": "Message sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin routes
@app.get("/admin")
async def admin_redirect():
    """Redirect to admin login"""
    return RedirectResponse(url="/admin/login")

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Render admin login page"""
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(request: Request, login_data: LoginRequest):
    """Handle admin login"""
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    if login_data.username == admin_username and login_data.password == admin_password:
        request.session['admin_logged_in'] = True
        return {"success": True}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, _: bool = Depends(get_current_user)):
    """Render admin dashboard"""
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

@app.get("/admin/logout")
async def admin_logout(request: Request):
    """Logout admin"""
    request.session.pop('admin_logged_in', None)
    return RedirectResponse(url="/admin/login")

# Admin API endpoints
@app.get("/admin/api/data")
async def get_admin_data(_: bool = Depends(get_current_user)):
    """Get all portfolio data"""
    return load_portfolio_data()

@app.post("/admin/api/about")
async def update_about(about_data: AboutData, _: bool = Depends(get_current_user)):
    """Update about section"""
    data = load_portfolio_data()
    data['about'] = {
        'name': about_data.name,
        'title': about_data.title,
        'description': [about_data.desc1, about_data.desc2, about_data.desc3],
        'stats': {
            'years': about_data.years,
            'projects': about_data.projects_count,
            'technologies': about_data.technologies
        }
    }
    save_portfolio_data(data)
    return {"success": True, "message": "About section updated successfully"}

@app.post("/admin/api/skills")
async def update_skills(skills_data: SkillsData, _: bool = Depends(get_current_user)):
    """Update skills section"""
    data = load_portfolio_data()
    data['skills'] = {
        'languages': [s.strip() for s in skills_data.languages.split(',')],
        'aiml': [s.strip() for s in skills_data.aiml.split(',')],
        'datascience': [s.strip() for s in skills_data.datascience.split(',')],
        'tools': [s.strip() for s in skills_data.tools.split(',')]
    }
    save_portfolio_data(data)
    return {"success": True, "message": "Skills updated successfully"}

@app.post("/admin/api/experience")
async def update_experience(request: Request, _: bool = Depends(get_current_user)):
    """Update experience section"""
    data = load_portfolio_data()
    form_data = await request.json()
    data['experience'] = form_data.get('experience', [])
    save_portfolio_data(data)
    return {"success": True, "message": "Experience updated successfully"}

@app.post("/admin/api/achievements")
async def update_achievements(ach_data: AchievementsData, _: bool = Depends(get_current_user)):
    """Update achievements section"""
    data = load_portfolio_data()
    data['achievements'] = {
        'achievements': [
            {'title': ach_data.ach1_title, 'description': ach_data.ach1_desc},
            {'title': ach_data.ach2_title, 'description': ach_data.ach2_desc}
        ],
        'certifications': [
            {'title': ach_data.cert1_title, 'details': ach_data.cert1_details},
            {'title': ach_data.cert2_title, 'details': ach_data.cert2_details}
        ]
    }
    save_portfolio_data(data)
    return {"success": True, "message": "Achievements updated successfully"}

@app.get("/admin/api/projects")
async def get_projects(_: bool = Depends(get_current_user)):
    """Get all projects"""
    data = load_portfolio_data()
    return {"projects": data.get('projects', [])}

@app.post("/admin/api/projects")
async def add_project(project_data: ProjectData, _: bool = Depends(get_current_user)):
    """Add new project"""
    data = load_portfolio_data()
    if 'projects' not in data:
        data['projects'] = []
    
    # Generate new ID
    max_id = max([int(p.get('id', 0)) for p in data['projects']], default=0)
    
    new_project = {
        'id': str(max_id + 1),
        'title': project_data.title,
        'short_desc': project_data.short_desc,
        'image_url': project_data.image_url,
        'overview': project_data.overview,
        'challenges': project_data.challenges,
        'tech_stack': [t.strip() for t in project_data.tech_stack.split(',')],
        'github_url': project_data.github_url,
        'demo_url': project_data.demo_url
    }
    
    data['projects'].append(new_project)
    save_portfolio_data(data)
    return {"success": True, "message": "Project added successfully", "project": new_project}

@app.put("/admin/api/projects/{project_id}")
async def update_project(project_id: str, project_data: ProjectData, _: bool = Depends(get_current_user)):
    """Update existing project"""
    data = load_portfolio_data()
    if 'projects' not in data:
        raise HTTPException(status_code=404, detail="No projects found")
    
    for i, p in enumerate(data['projects']):
        if str(p.get('id')) == str(project_id):
            data['projects'][i] = {
                'id': project_id,
                'title': project_data.title,
                'short_desc': project_data.short_desc,
                'image_url': project_data.image_url,
                'overview': project_data.overview,
                'challenges': project_data.challenges,
                'tech_stack': [t.strip() for t in project_data.tech_stack.split(',')],
                'github_url': project_data.github_url,
                'demo_url': project_data.demo_url
            }
            save_portfolio_data(data)
            return {"success": True, "message": "Project updated successfully"}
    
    raise HTTPException(status_code=404, detail="Project not found")

@app.delete("/admin/api/projects/{project_id}")
async def delete_project(project_id: str, _: bool = Depends(get_current_user)):
    """Delete project"""
    data = load_portfolio_data()
    if 'projects' not in data:
        raise HTTPException(status_code=404, detail="No projects found")
    
    for i, p in enumerate(data['projects']):
        if str(p.get('id')) == str(project_id):
            data['projects'].pop(i)
            save_portfolio_data(data)
            return {"success": True, "message": "Project deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Project not found")

@app.post("/admin/api/upload-image")
async def upload_image(image: UploadFile = File(...), _: bool = Depends(get_current_user)):
    """Upload project image"""
    if not image:
        raise HTTPException(status_code=400, detail="No image file provided")
    
    if not allowed_file(image.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: png, jpg, jpeg, gif, webp")
    
    # Check file size
    contents = await image.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 16MB")
    
    # Generate unique filename
    timestamp = str(int(time.time()))
    name, ext = os.path.splitext(image.filename)
    filename = f"{name}_{timestamp}{ext}"
    
    filepath = UPLOAD_FOLDER / filename
    
    # Save file
    async with aiofiles.open(filepath, 'wb') as f:
        await f.write(contents)
    
    image_url = f"/static/uploads/projects/{filename}"
    return {"success": True, "image_url": image_url}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "FastAPI app is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
