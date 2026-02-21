# Security Fix - Remove .env from Git History

## ⚠️ IMPORTANT: Your .env file with credentials was pushed to GitHub!

Follow these steps to remove it and secure your credentials:

## Step 1: Remove .env from Git History

Run these commands in your terminal:

```powershell
# Remove .env from git history
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from repository"

# Push the changes
git push origin main
```

## Step 2: Change Your Credentials IMMEDIATELY

Since your credentials were exposed on GitHub, you MUST change them:

### 1. Change Admin Password
Update in your `.env` file:
```env
ADMIN_PASSWORD=new_secure_password_here
```

### 2. Change Email Password
If you're using Gmail:
- Go to: https://myaccount.google.com/apppasswords
- Delete the old app password
- Generate a NEW app password
- Update in `.env`:
```env
MAIL_PASSWORD=new_app_password_here
```

### 3. Generate New Secret Key
```python
# Run this in Python to generate a new secret key:
import secrets
print(secrets.token_urlsafe(32))
```

Update in `.env`:
```env
SECRET_KEY=new_generated_secret_key
```

## Step 3: Verify .env is Ignored

```powershell
# Check git status - .env should NOT appear
git status

# Verify .gitignore contains .env
cat .gitignore
```

## Step 4: Push Updated .gitignore

```powershell
git add .gitignore
git commit -m "Add .gitignore to protect sensitive files"
git push origin main
```

## Step 5: Set Environment Variables in Render

When deploying to Render, set these in the Dashboard (NOT in code):

```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_new_secure_password
SECRET_KEY=your_new_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_new_app_password
MAIL_RECIPIENT=your_email@gmail.com
APP_URL=https://your-app.onrender.com
```

## Optional: Complete History Cleanup

If you want to completely remove .env from ALL git history:

```powershell
# WARNING: This rewrites history - use with caution
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (this will rewrite history)
git push origin main --force
```

## Verification Checklist

- [ ] .env removed from repository
- [ ] Admin password changed
- [ ] Email app password regenerated
- [ ] Secret key regenerated
- [ ] .gitignore includes .env
- [ ] Changes pushed to GitHub
- [ ] Verified .env not visible on GitHub

## Prevention

Your `.gitignore` now includes `.env` so this won't happen again!

## Need Help?

If you're unsure about any step, it's better to:
1. Delete the entire GitHub repository
2. Create a new one
3. Push fresh code without .env
