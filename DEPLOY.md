# 🚀 Deployment Guide — Render (Flask) + FreeSQLDatabase (MySQL)

Your backend will be live at a public URL like:
`https://college-event-backend.onrender.com`

---

## PART 1 — Get a Free MySQL Database

### Option A: FreeSQLDatabase.com (Easiest — 100% free)
1. Go to → https://www.freesqldatabase.com
2. Sign up with your email
3. You'll receive an email with:
   - **Host** (e.g. `sql12.freesqldatabase.com`)
   - **Database name** (e.g. `sql12123456`)
   - **Username** (e.g. `sql12123456`)
   - **Password** (random string)
   - **Port** → `3306`
4. Save these — you'll paste them into Render

### Option B: Railway MySQL (Generous free tier)
1. Go to → https://railway.app
2. Sign up → New Project → Add MySQL
3. Click MySQL → go to **Connect** tab
4. Copy Host, Port, User, Password, Database

---

## PART 2 — Push your project to GitHub

Your project folder should look like this:
```
college-event-management-system/
├── app.py
├── requirements.txt
├── render.yaml
├── Procfile
├── home.html
├── login.html
├── register.html
├── booking.html
├── admin.html
└── ... (all other HTML files)
```

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/college-event-management-system.git
git push -u origin main
```

---

## PART 3 — Deploy on Render

1. Go to → https://render.com
2. Sign up / Log in (free)
3. Click **"New +"** → **"Web Service"**
4. Click **"Connect a repository"** → select your GitHub repo
5. Fill in these settings:

| Field | Value |
|-------|-------|
| Name | `college-event-backend` |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |

6. Scroll down to **"Environment Variables"** and add:

| Key | Value |
|-----|-------|
| `MYSQL_HOST` | (from FreeSQLDatabase email) |
| `MYSQL_PORT` | `3306` |
| `MYSQL_USER` | (from FreeSQLDatabase email) |
| `MYSQL_PASSWORD` | (from FreeSQLDatabase email) |
| `MYSQL_DATABASE` | (from FreeSQLDatabase email) |

7. Click **"Create Web Service"**
8. Wait ~3 minutes for the build to finish ✅

---

## PART 4 — Update your HTML files

Your HTML files use `fetch('/api/...')` which works when served from the same server.

Since Render serves everything from `app.py` (Flask serves your HTML files too), **no changes needed** — just make sure all HTML files are in the **same folder** as `app.py`.

Your live URL will be:
```
https://college-event-backend.onrender.com/home.html
```

---

## Default Admin Login
| Field | Value |
|-------|-------|
| Register No | `ADMIN001` |
| Password | `admin123` |

---

## Troubleshooting

**Build fails?**
- Make sure `requirements.txt` is in the root of your repo
- Check Render logs under "Logs" tab

**Database connection error?**
- Double-check the 5 environment variables in Render dashboard
- Try connecting with MySQL Workbench using the same credentials to verify

**App works locally but not on Render?**
- Make sure `host='0.0.0.0'` is set in `app.run()` (already done ✅)
- Make sure `gunicorn` is in `requirements.txt` (already done ✅)

**Free tier goes to sleep?**
- Render free tier sleeps after 15 min of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to Starter ($7/mo) for always-on
