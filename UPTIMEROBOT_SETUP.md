# FREE Keep-Alive Setup with UptimeRobot

## Why UptimeRobot?
- ✅ **100% FREE** (no credit card needed)
- ✅ Pings every 5 minutes
- ✅ Prevents Render cold starts
- ✅ Email alerts if your site goes down
- ✅ Better than Render's paid cron job!

## Quick Setup (2 Minutes)

### Step 1: Update Your Render Web Service

Go to [Render Dashboard](https://dashboard.render.com/) → Your existing web service → Settings:

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Environment Variables** (add these):
```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_new_secure_password
SECRET_KEY=your_new_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tnajaykumar563@gmail.com
MAIL_PASSWORD=your_new_app_password
MAIL_RECIPIENT=tnajaykumar563@gmail.com
```

Click **Save Changes** - Render will auto-deploy.

### Step 2: Set Up UptimeRobot (FREE)

1. Go to: **https://uptimerobot.com/**
2. Click **"Sign Up"** (FREE - no credit card)
3. Verify your email
4. Click **"Add New Monitor"**
5. Fill in:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Portfolio Keep-Alive
   - **URL**: `https://your-render-url.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
6. Click **"Create Monitor"**

**Done!** Your site will now stay awake 24/7 for FREE!

## How to Find Your Render URL

1. Go to Render Dashboard
2. Click your web service
3. Copy the URL at the top (e.g., `https://ajaytn.onrender.com`)
4. Use this in UptimeRobot with `/health` at the end

## Test It Works

```bash
# Test health endpoint
curl https://your-render-url.onrender.com/health

# Should return:
{"status": "healthy"}
```

## Benefits

| Feature | Render Cron | UptimeRobot |
|---------|-------------|-------------|
| Cost | 💰 Paid | ✅ FREE |
| Interval | 14 min | 5 min |
| Monitoring | ❌ No | ✅ Yes |
| Alerts | ❌ No | ✅ Email |

## Troubleshooting

**Site still slow?**
- Wait 5 minutes after UptimeRobot setup
- Check monitor shows "Up" in UptimeRobot
- Verify URL is correct with `/health` at end

**Monitor shows "Down"?**
- Check Render service is running
- Verify `/health` endpoint works
- Check Render logs for errors

## Summary

✅ UptimeRobot is FREE forever  
✅ Pings every 5 minutes  
✅ Prevents cold starts  
✅ Email alerts included  
✅ Setup takes 2 minutes  

Your portfolio will load instantly, 24/7, for FREE!
