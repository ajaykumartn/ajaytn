# AI/ML Developer Portfolio

A modern, responsive portfolio website built with Flask, featuring smooth animations and interactive elements.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Main site: http://127.0.0.1:5000


## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── run.py                 # Startup script with diagnostics
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (email config)
├── static/
│   ├── css/
│   │   └── main.css     # Custom styles and animations
│   └── js/
│       └── app.js       # Interactive functionality
└── templates/
    ├── index_new.html        # Main portfolio page
    ├── projects_new.html     # All projects page
    ├── project-detail_new.html # Individual project details
```

## 🔧 Features

- **Responsive Design**: Works on all devices
- **Smooth Animations**: AOS (Animate On Scroll) library
- **Interactive Particles**: Particles.js background
- **3D Tilt Effects**: Vanilla-tilt.js for project cards
- **Contact Form**: Email integration (requires SMTP setup)
- **Modern UI**: Tailwind CSS with custom styling


## 🎨 Customization

- Update project data in `app.py` (PROJECTS dictionary)
- Modify styles in `static/css/main.css`
- Customize animations in `static/js/app.js`
- Replace placeholder content in templates

## 📱 External Libraries Used

- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Beautiful icon library
- **AOS**: Animate On Scroll library
- **Particles.js**: Interactive particle backgrounds
- **Vanilla Tilt**: 3D tilt hover effects

## 🚨 Common Issues

1. **Static files not loading**: Check Flask static folder configuration
2. **Animations not working**: Verify AOS library is loaded
3. **Icons missing**: Ensure Lucide icons script is loaded
4. **Contact form errors**: Check email configuration in `.env`