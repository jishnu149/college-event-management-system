# ============================================================
#  College Event Management System — Flask + MySQL Backend
#  Plain text passwords (simple & reliable for college project)
#  Install:  pip install flask flask-cors mysql-connector-python
#  Run:      python app.py
# ============================================================

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ─── DB Connection ────────────────────────────────────────────
def get_db():
    return mysql.connector.connect(
        host     = os.environ.get('MYSQL_HOST',     'localhost'),
        port     = int(os.environ.get('MYSQL_PORT', 3306)),
        user     = os.environ.get('MYSQL_USER',     'root'),
        password = os.environ.get('MYSQL_PASSWORD', ''),
        database = os.environ.get('MYSQL_DATABASE', 'college_events'),
        charset  = 'utf8mb4',
        autocommit = False
    )

# ─── DB Init ──────────────────────────────────────────────────
def init_db():
    conn = get_db()
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            name  VARCHAR(100) NOT NULL,
            reg   VARCHAR(50)  NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            phone VARCHAR(15)  NOT NULL,
            pass  VARCHAR(255) NOT NULL,
            role  VARCHAR(10)  NOT NULL DEFAULT 'student'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            name        VARCHAR(150) NOT NULL,
            category    VARCHAR(20)  NOT NULL,
            event_date  DATE         NOT NULL,
            venue       VARCHAR(150) NOT NULL,
            seats       INT          NOT NULL DEFAULT 50,
            description TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            reg       VARCHAR(50)  NOT NULL,
            name      VARCHAR(100) NOT NULL,
            email     VARCHAR(120) NOT NULL,
            event     VARCHAR(150) NOT NULL,
            booked_at VARCHAR(50),
            UNIQUE KEY unique_booking (reg, event)
        )
    """)

    conn.commit()

    # Seed admin
    cur.execute("SELECT id FROM users WHERE role='admin'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (name,reg,email,phone,pass,role) VALUES (%s,%s,%s,%s,%s,%s)",
            ('Admin', 'ADMIN001', 'admin@college.edu', '0000000000', 'admin123', 'admin')
        )
        conn.commit()
        print("✅ Admin seeded  →  reg: ADMIN001  |  pass: admin123")

    # Seed events
    cur.execute("SELECT COUNT(*) FROM events")
    if cur.fetchone()[0] == 0:
        seed = [
            ('Paper Presentation',  'academic',  '2025-04-10', 'Seminar Hall A', 50,  'Present your research to a panel of judges.'),
            ('Quiz Competition',    'academic',  '2025-04-12', 'Room 101',        40,  'Test your knowledge across subjects.'),
            ('Debate Competition',  'academic',  '2025-04-14', 'Seminar Hall B',  60,  'Argue your way to victory.'),
            ('Hackathon',           'technical', '2025-04-15', 'CS Lab',          30,  '24-hour coding marathon.'),
            ('Code Sprint',         'technical', '2025-04-16', 'CS Lab',          30,  'Competitive programming event.'),
            ('Web Design Contest',  'technical', '2025-04-17', 'IT Lab',          25,  'Design stunning websites.'),
            ('Dance Competition',   'cultural',  '2025-04-20', 'Main Stage',     100,  'Showcase your dance talent.'),
            ('Singing Competition', 'cultural',  '2025-04-21', 'Auditorium',      80,  'Sing your heart out.'),
            ('Drama / Skit',        'cultural',  '2025-04-22', 'Auditorium',      80,  'Act out an original script.'),
            ('Cricket',             'sports',    '2025-04-25', 'Ground A',        22,  'T10 cricket tournament.'),
            ('Football',            'sports',    '2025-04-26', 'Ground B',        22,  '7-a-side football knockout.'),
            ('Badminton',           'sports',    '2025-04-27', 'Indoor Court',    16,  'Singles and doubles tournament.'),
        ]
        cur.executemany(
            "INSERT INTO events (name,category,event_date,venue,seats,description) VALUES (%s,%s,%s,%s,%s,%s)",
            seed
        )
        conn.commit()
        print("✅ Events seeded.")

    cur.close()
    conn.close()
    print("✅ Database ready.")


# ════════════════════════════════════════════════════════════
#  AUTH ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/api/register', methods=['POST'])
def register():
    data  = request.get_json()
    name  = (data.get('name')  or '').strip()
    reg   = (data.get('reg')   or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    pwd   = (data.get('pass')  or '').strip()

    if not all([name, reg, email, phone, pwd]):
        return jsonify({'error': 'All fields are required.'}), 400

    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id FROM users WHERE reg=%s OR email=%s', (reg, email))
        if cur.fetchone():
            return jsonify({'error': 'Register number or email already exists.'}), 409
        cur.execute(
            'INSERT INTO users (name,reg,email,phone,pass,role) VALUES (%s,%s,%s,%s,%s,"student")',
            (name, reg, email, phone, pwd)
        )
        conn.commit()
        return jsonify({'message': 'Account created successfully.'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    reg  = (data.get('reg')  or '').strip()
    pwd  = (data.get('pass') or '').strip()

    if not reg or not pwd:
        return jsonify({'error': 'Register number and password are required.'}), 400

    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            'SELECT id,name,reg,email,phone,role FROM users WHERE reg=%s AND pass=%s AND role="student"',
            (reg, pwd)
        )
        user = cur.fetchone()
        if not user:
            return jsonify({'error': 'Invalid register number or password.'}), 401
        return jsonify({'message': 'Login successful.', 'user': user}), 200
    finally:
        cur.close(); conn.close()


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    reg  = (data.get('reg')  or '').strip()
    pwd  = (data.get('pass') or '').strip()
    if not reg or not pwd:
        return jsonify({'error': 'Credentials are required.'}), 400

    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            'SELECT id,name,reg,email,role FROM users WHERE reg=%s AND pass=%s AND role="admin"',
            (reg, pwd)
        )
        user = cur.fetchone()
        if not user:
            return jsonify({'error': 'Invalid admin credentials.'}), 401
        return jsonify({'message': 'Admin login successful.', 'user': user}), 200
    finally:
        cur.close(); conn.close()


# ════════════════════════════════════════════════════════════
#  USER / PROFILE ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/api/user/<reg>', methods=['GET'])
def get_user(reg):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id,name,reg,email,phone,role FROM users WHERE reg=%s', (reg,))
        user = cur.fetchone()
        if not user: return jsonify({'error': 'User not found.'}), 404
        return jsonify(user), 200
    finally:
        cur.close(); conn.close()


@app.route('/api/user/<reg>', methods=['PUT'])
def update_user(reg):
    data  = request.get_json()
    name  = (data.get('name')  or '').strip()
    email = (data.get('email') or '').strip()
    phone = (data.get('phone') or '').strip()
    if not all([name, email, phone]):
        return jsonify({'error': 'Name, email and phone are required.'}), 400
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute('UPDATE users SET name=%s,email=%s,phone=%s WHERE reg=%s', (name, email, phone, reg))
        conn.commit()
        if cur.rowcount == 0: return jsonify({'error': 'User not found.'}), 404
        return jsonify({'message': 'Profile updated successfully.'}), 200
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


@app.route('/api/user/<reg>/password', methods=['PUT'])
def change_password(reg):
    data     = request.get_json()
    old_pass = (data.get('oldPass') or '').strip()
    new_pass = (data.get('newPass') or '').strip()
    if not old_pass or not new_pass:
        return jsonify({'error': 'Old and new password are required.'}), 400
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id FROM users WHERE reg=%s AND pass=%s', (reg, old_pass))
        if not cur.fetchone():
            return jsonify({'error': 'Old password is incorrect.'}), 401
        cur.execute('UPDATE users SET pass=%s WHERE reg=%s', (new_pass, reg))
        conn.commit()
        return jsonify({'message': 'Password updated successfully.'}), 200
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


# ════════════════════════════════════════════════════════════
#  BOOKING ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data  = request.get_json()
    reg   = (data.get('reg')   or '').strip()
    name  = (data.get('name')  or '').strip()
    email = (data.get('email') or '').strip()
    event = (data.get('event') or '').strip()
    time  = (data.get('time')  or '').strip()

    if not all([reg, name, email, event]):
        return jsonify({'error': 'All booking fields are required.'}), 400

    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id FROM bookings WHERE reg=%s AND event=%s', (reg, event))
        if cur.fetchone():
            return jsonify({'error': 'You have already registered for this event.'}), 409
        cur.execute(
            'INSERT INTO bookings (reg,name,email,event,booked_at) VALUES (%s,%s,%s,%s,%s)',
            (reg, name, email, event, time)
        )
        conn.commit()
        return jsonify({'message': 'Registered successfully!', 'id': cur.lastrowid}), 201
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


@app.route('/api/bookings/<reg>', methods=['GET'])
def get_bookings(reg):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            'SELECT id,reg,name,email,event,booked_at AS time FROM bookings WHERE reg=%s ORDER BY id DESC',
            (reg,)
        )
        return jsonify(cur.fetchall()), 200
    finally:
        cur.close(); conn.close()


@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute('DELETE FROM bookings WHERE id=%s', (booking_id,))
        conn.commit()
        if cur.rowcount == 0: return jsonify({'error': 'Booking not found.'}), 404
        return jsonify({'message': 'Booking cancelled.'}), 200
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


# ════════════════════════════════════════════════════════════
#  EVENTS ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/api/events', methods=['GET'])
def get_events():
    category = request.args.get('category', '').strip().lower()
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        if category:
            cur.execute('SELECT * FROM events WHERE category=%s ORDER BY event_date', (category,))
        else:
            cur.execute('SELECT * FROM events ORDER BY event_date')
        rows = cur.fetchall()
        for r in rows:
            r['event_date'] = str(r['event_date'])
        return jsonify(rows), 200
    finally:
        cur.close(); conn.close()


@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT * FROM events WHERE id=%s', (event_id,))
        event = cur.fetchone()
        if not event: return jsonify({'error': 'Event not found.'}), 404
        event['event_date'] = str(event['event_date'])
        return jsonify(event), 200
    finally:
        cur.close(); conn.close()


# ════════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/api/admin/bookings', methods=['GET'])
def admin_get_bookings():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id,reg,name,email,event,booked_at AS time FROM bookings ORDER BY id DESC')
        return jsonify(cur.fetchall()), 200
    finally:
        cur.close(); conn.close()


@app.route('/api/admin/bookings', methods=['DELETE'])
def admin_clear_bookings():
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute('DELETE FROM bookings')
        conn.commit()
        return jsonify({'message': f'Deleted {cur.rowcount} booking(s).'}), 200
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


@app.route('/api/admin/bookings/<int:booking_id>', methods=['DELETE'])
def admin_delete_booking(booking_id):
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute('DELETE FROM bookings WHERE id=%s', (booking_id,))
        conn.commit()
        if cur.rowcount == 0: return jsonify({'error': 'Booking not found.'}), 404
        return jsonify({'message': 'Booking deleted.'}), 200
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT id,name,reg,email,phone,role FROM users ORDER BY id DESC')
        return jsonify(cur.fetchall()), 200
    finally:
        cur.close(); conn.close()


@app.route('/api/admin/users/<reg>', methods=['DELETE'])
def admin_delete_user(reg):
    conn = get_db(); cur = conn.cursor()
    try:
        cur.execute('DELETE FROM users WHERE reg=%s AND role="student"', (reg,))
        conn.commit()
        if cur.rowcount == 0: return jsonify({'error': 'Student not found.'}), 404
        return jsonify({'message': 'Student deleted.'}), 200
    except Exception as e:
        conn.rollback(); return jsonify({'error': str(e)}), 500
    finally:
        cur.close(); conn.close()


@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute('SELECT COUNT(*) AS total FROM users WHERE role="student"')
        total_students = cur.fetchone()['total']
        cur.execute('SELECT COUNT(*) AS total FROM bookings')
        total_bookings = cur.fetchone()['total']
        cur.execute('SELECT event, COUNT(*) AS count FROM bookings GROUP BY event ORDER BY count DESC')
        event_breakdown = cur.fetchall()
        return jsonify({
            'totalStudents':  total_students,
            'totalBookings':  total_bookings,
            'eventBreakdown': event_breakdown
        }), 200
    finally:
        cur.close(); conn.close()


# ─── Serve HTML files ─────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'home.html')


# ─── Start ───────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 3000))
    print(f"\n🚀 Server running at http://localhost:{port}")
    print(f"   Open: http://localhost:{port}/home.html\n")
    app.run(host='0.0.0.0', port=port, debug=True)
