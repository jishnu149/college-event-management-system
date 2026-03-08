const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '/')));

// Database setup
const dbPath = path.join(__dirname, 'database.sqlite');
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to the SQLite database.');
        
        // Create users table
        db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            reg TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            pass TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )`, (err) => {
            if (err) {
                console.error("Error creating users table:", err);
            } else {
                // Ensure admin exists
                const insertAdmin = `INSERT INTO users (name, reg, email, phone, pass, role) 
                                   VALUES ('Administrator', '5260', 'admin@vit.edu', '0000000000', '1234', 'admin')`;
                db.run(insertAdmin, (err) => {
                    if (err && err.message.indexOf('UNIQUE constraint failed') === -1) {
                         console.error("Error inserting admin user:", err);
                    }
                });
            }
        });

        // Create bookings table
        db.run(`CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            event TEXT NOT NULL,
            time TEXT NOT NULL,
            UNIQUE(reg, event)
        )`, (err) => {
            if (err) {
                console.error("Error creating bookings table:", err);
            }
        });
    }
});


// --- API Endpoints ---

// 1. Register User
app.post('/api/register', (req, res) => {
    const { name, reg, email, phone, pass } = req.body;

    if (!name || !reg || !email || !phone || !pass) {
        return res.status(400).json({ error: "All fields are required" });
    }

    const sql = `INSERT INTO users (name, reg, email, phone, pass) VALUES (?, ?, ?, ?, ?)`;
    db.run(sql, [name, reg, email, phone, pass], function(err) {
        if (err) {
            if (err.message.includes('UNIQUE constraint failed')) {
                return res.status(409).json({ error: "Account already exists!" });
            }
            return res.status(500).json({ error: "Database error" });
        }
        res.status(201).json({ message: "Account created successfully" });
    });
});

// 2. Login User
app.post('/api/login', (req, res) => {
    const { reg, pass } = req.body;

    if (!reg || !pass) {
        return res.status(400).json({ error: "Register number and password required" });
    }

    const sql = `SELECT * FROM users WHERE reg = ? AND role = 'user'`;
    db.get(sql, [reg], (err, user) => {
        if (err) {
            return res.status(500).json({ error: "Database error" });
        }
        if (!user) {
            return res.status(404).json({ error: "Account not found. Please register." });
        }
        if (user.pass !== pass) {
            return res.status(401).json({ error: "Wrong password!" });
        }
        
        // Don't send the password back
        const { pass: userPass, ...userData } = user;
        res.status(200).json({ message: "Login successful", user: userData });
    });
});

// 3. Admin Login
app.post('/api/admin/login', (req, res) => {
    const { id, pass } = req.body;

    if (!id || !pass) {
        return res.status(400).json({ error: "Admin ID and password required" });
    }

    const sql = `SELECT * FROM users WHERE reg = ? AND role = 'admin'`;
    db.get(sql, [id], (err, admin) => {
        if (err) {
            return res.status(500).json({ error: "Database error" });
        }
        if (!admin) {
             return res.status(404).json({ error: "Invalid Admin Credentials!" });
        }
        if (admin.pass !== pass) {
             return res.status(401).json({ error: "Invalid Admin Credentials!" });
        }
        
        const { pass: adminPass, ...adminData } = admin;
        res.status(200).json({ message: "Admin login successful", user: adminData });
    });
});

// 4. Book Event
app.post('/api/bookings', (req, res) => {
    const { reg, name, email, event, time } = req.body;

    if (!reg || !name || !email || !event || !time) {
        return res.status(400).json({ error: "All fields are required" });
    }

    const sql = `INSERT INTO bookings (reg, name, email, event, time) VALUES (?, ?, ?, ?, ?)`;
    db.run(sql, [reg, name, email, event, time], function(err) {
        if (err) {
             if (err.message.includes('UNIQUE constraint failed')) {
                return res.status(409).json({ error: "Already registered!" });
            }
            return res.status(500).json({ error: "Database error" });
        }
        res.status(201).json({ message: "Booking Successful!" });
    });
});

// 5. Get Bookings for a User
app.get('/api/bookings/:reg', (req, res) => {
    const { reg } = req.params;

    const sql = `SELECT * FROM bookings WHERE reg = ? ORDER BY id DESC`;
    db.all(sql, [reg], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: "Database error" });
        }
        res.status(200).json(rows);
    });
});

// 6. Get All Bookings (Admin)
app.get('/api/admin/bookings', (req, res) => {
    const sql = `SELECT * FROM bookings ORDER BY id DESC`;
    db.all(sql, [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: "Database error" });
        }
        res.status(200).json(rows);
    });
});

// 7. Clear All Bookings (Admin)
app.delete('/api/admin/bookings', (req, res) => {
    const sql = `DELETE FROM bookings`;
    db.run(sql, function(err) {
        if (err) {
            return res.status(500).json({ error: "Database error" });
        }
        res.status(200).json({ message: "All records deleted successfully" });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
