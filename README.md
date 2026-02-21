# AI/ML Developer Portfolio

A modern, high-performance portfolio website built with **FastAPI**, featuring an admin dashboard, dynamic content management, and optimized for deployment on Render.

## ✨ Features

### Frontend
- 🎨 **Modern Responsive Design** - Works perfectly on all devices
- ✨ **Smooth Animations** - AOS (Animate On Scroll) library
- 🎭 **Interactive Elements** - 3D tilt effects, particle backgrounds
- 📱 **Mobile-First** - Optimized for mobile and desktop
- 🎯 **SEO Optimized** - Fast loading with GZip compression

### Backend
- ⚡ **FastAPI** - High-performance async Python framework
- 🔐 **Admin Dashboard** - Manage all content without coding
- 📝 **Dynamic Content** - JSON-based data storage
- 🖼️ **Image Upload** - Direct image upload for projects
- 📧 **Contact Form** - Email integration with SMTP
- 🚀 **Keep-Alive** - Prevents cold starts on free hosting

### Admin Dashboard
- ✏️ Edit About section
- 🛠️ Manage Skills
- 💼 Add/Edit/Delete Experience
- 🏆 Update Achievements & Certifications
- 📁 Full Project Management (CRUD)
- 🖼️ Image Upload for Projects

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd portfolio
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file:
   ```env
   # Admin Credentials
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your_secure_password
   SECRET_KEY=your_secret_key_here
   
   # Email Configuration (Optional)
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_RECIPIENT=your_email@gmail.com
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Access the application:**
   - Portfolio: http://localhost:5000
   - Admin Dashboard: http://localhost:5000/admin
   - API Docs: http://localhost:5000/docs

## 📁 Project Structure

```
portfolio/
├── main.py                      # FastAPI application
├── keep_alive.py                # Keep-alive service for Render
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── Procfile                     # Render deployment config
├── render.yaml                  # Render blueprint
├── runtime.txt                  # Python version
├── RENDER_DEPLOYMENT.md         # Deployment guide
│
├── data/
│   └── portfolio_data.json      # Dynamic content storage
│
├── static/
│   ├── css/
│   │   ├── main.css            # Main styles
│   │   └── contact.css         # Contact page styles
│   ├── js/
│   │   └── app.js              # JavaScript functionality
│   ├── images/                  # Static images
│   └── uploads/
│       └── projects/            # Uploaded project images
│
└── templates/
    ├── index_new.html           # Homepage
    ├── projects_new.html        # All projects page
    ├── project-detail_new.html  # Project detail page
    ├── contact.html             # Contact page
    ├── admin_login.html         # Admin login
    └── admin_dashboard.html     # Admin dashboard
```

## 🎨 Customization

### Via Admin Dashboard (No Coding Required)
1. Login at `/admin` with your credentials
2. Edit any section through the intuitive interface
3. Upload images directly
4. Changes reflect immediately on the website

### Manual Customization
- **Styles**: Edit `static/css/main.css`
- **Scripts**: Modify `static/js/app.js`
- **Templates**: Update HTML files in `templates/`
- **Data**: Edit `data/portfolio_data.json` (or use admin dashboard)

## 🚀 Deployment to Render

### Quick Deploy (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render auto-detects `render.yaml`
   - Click "Apply"

3. **Set Environment Variables:**
   In Render Dashboard, add:
   - `ADMIN_PASSWORD`: Your admin password
   - `SECRET_KEY`: Random secret key
   - `APP_URL`: Your Render URL (after deployment)

4. **Done!** Your portfolio is live with keep-alive enabled.

For detailed deployment instructions, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

## 🔐 Admin Dashboard

### Access
- URL: `https://your-app.onrender.com/admin`
- Default username: `admin`
- Password: Set in `.env` file

### Features
- **About Section**: Edit name, title, descriptions, stats
- **Skills**: Manage all skill categories
- **Experience**: Add/edit/delete work experience
- **Achievements**: Update achievements and certifications
- **Projects**: Full CRUD operations with image upload

## 📧 Contact Form Setup

To enable the contact form:

1. **For Gmail:**
   - Enable 2-Factor Authentication
   - Generate App Password: https://myaccount.google.com/apppasswords
   - Use App Password in `.env` file

2. **Update `.env`:**
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_RECIPIENT=where_to_receive@gmail.com
   ```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Aiofiles** - Async file operations

### Frontend
- **Jinja2** - Template engine
- **Lucide Icons** - Icon library
- **AOS** - Scroll animations
- **Vanilla Tilt** - 3D effects

### Deployment
- **Render** - Cloud hosting
- **Keep-Alive** - Prevents cold starts

## 📊 Performance

- **Response Time**: < 100ms (cached)
- **Page Load**: < 1 second
- **API Performance**: 2-3x faster than Flask
- **Cold Start**: Prevented with keep-alive

## 🔧 API Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows
```

### Static Files Not Loading
- Check `static/` folder exists
- Verify file paths in templates
- Clear browser cache

### Admin Login Not Working
- Check `.env` file exists
- Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD`
- Check `SECRET_KEY` is set

### Images Not Uploading
- Verify `static/uploads/projects/` folder exists
- Check file permissions
- Ensure file size < 16MB

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, use the contact form on the website or open an issue on GitHub.

---

**Built with ❤️ using FastAPI**