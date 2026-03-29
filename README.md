# 🎓 College Event Management System

<p align="center">
  <img src="https://img.shields.io/badge/Flask-Python-blue?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql" />
  <img src="https://img.shields.io/badge/Render-Deployed-purple?style=for-the-badge&logo=render" />
  <img src="https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge" />
</p>

<p align="center">
  <b>A full-stack web application to manage and book college events — built with Flask, MySQL, and vanilla HTML/CSS/JS.</b>
</p>

<p align="center">
  🌐 <a href="https://college-event-management-system-f5o3.onrender.com/home.html"><strong>Live Demo → college-event-management-system-f5o3.onrender.com</strong></a>
</p>

---

## 🚀 Features

### 👨‍🎓 Student Side
- 📝 **Register & Login** — Create an account with your register number, email and phone
- 🎉 **Browse Events** — Explore events across 4 categories: Academic, Technical, Cultural and Sports
- 📅 **Event Details** — View venue, date, time and live countdown for each event
- ✅ **Book Events** — Register for upcoming events with one click
- ❌ **Booking Closed Automatically** — Past events are greyed out and cannot be booked
- 📋 **My Bookings** — View all your registered events in one place
- 👤 **Profile Management** — Update your name, email and phone anytime

### 🔐 Admin Side
- 🔑 **Secure Admin Login** — Separate login portal for admins
- 📊 **All Registrations** — View every student booking across all events
- 📈 **Event Popularity Chart** — Animated bar chart showing most booked events
- 🗑️ **Manage Bookings** — Delete individual or all bookings
- 👥 **Manage Students** — View and delete student accounts

---

## 🗂️ Event Categories

| Category | Events |
|----------|--------|
| 🎭 Cultural | Vibrance, Christmas Celebration |
| ⚽ Sports | Football Tournament, Championship Trophy |
| 📚 Academic | Student Workshop, Seminar on Sustainability |
| 💻 Technical | DevsHouse, 5G Hackathon |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | MySQL (FreeSQLDatabase) |
| Hosting | Render |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```
college-event-management-system/
│
├── app.py                  ← Flask backend (all API routes)
├── requirements.txt        ← Python dependencies
├── Procfile                ← Render start command
├── render.yaml             ← Render deployment config
│
├── home.html               ← Landing page
├── login.html              ← Student login
├── register.html           ← Student registration
├── login_select.html       ← Choose student / admin
├── admin_login.html        ← Admin login
├── admin.html              ← Admin dashboard
│
├── categories.html         ← Event categories
├── cultural.html           ← Cultural events
├── technical.html          ← Technical events
├── academic.html           ← Academic events
├── sports.html             ← Sports events
│
├── details.html            ← Event detail + booking
├── booking.html            ← Booking confirmation
├── mybookings.html         ← Student's booked events
└── profile.html            ← Student profile
```

---

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Student registration |
| POST | `/api/login` | Student login |
| POST | `/api/admin/login` | Admin login |
| GET | `/api/user/<reg>` | Get student profile |
| PUT | `/api/user/<reg>` | Update profile |
| POST | `/api/bookings` | Book an event |
| GET | `/api/bookings/<reg>` | Get student bookings |
| DELETE | `/api/bookings/<id>` | Cancel a booking |
| GET | `/api/admin/bookings` | All bookings (admin) |
| DELETE | `/api/admin/bookings` | Clear all bookings |
| GET | `/api/admin/stats` | Dashboard stats |

---

## 🖥️ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/jishnu149/college-event-management-system.git
cd college-event-management-system
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set environment variables**
```bash
set MYSQL_HOST=your_host
set MYSQL_USER=your_user
set MYSQL_PASSWORD=your_password
set MYSQL_DATABASE=your_database
set MYSQL_PORT=3306
```

**4. Run the server**
```bash
python app.py
```

**5. Open in browser**
```
http://localhost:3000/home.html
```

---

## 🔑 Default Admin Credentials

| Field | Value |
|-------|-------|
| Admin ID | `ADMIN001` |
| Password | `admin123` |

---

## 🌐 Live Project

> **🔗 [https://college-event-management-system-f5o3.onrender.com/home.html](https://college-event-management-system-f5o3.onrender.com/home.html)**

---

## 👨‍💻 Developer

Made with ❤️ by **Jishnu**

[![GitHub](https://img.shields.io/badge/GitHub-jishnu149-black?style=flat-square&logo=github)](https://github.com/jishnu149)
