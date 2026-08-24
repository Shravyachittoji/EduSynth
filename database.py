import sqlite3

DB_NAME = "students.db"


# -----------------------------------------
# CREATE USERS TABLE
# -----------------------------------------
def create_users_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# CREATE QUIZ RESULTS TABLE
# -----------------------------------------
def create_quiz_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            level TEXT,
            score INTEGER,
            total_questions INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# INSERT QUIZ RESULT
# -----------------------------------------
def insert_quiz_result(user_id, subject, level, score, total_questions):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_results
        (user_id, subject, level, score, total_questions)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, subject, level, score, total_questions))

    conn.commit()
    conn.close()


# -----------------------------------------
# FETCH USER PERFORMANCE
# -----------------------------------------
def fetch_user_performance(user_id, subject):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, total_questions
        FROM quiz_results
        WHERE user_id = ? AND subject = ?
        ORDER BY timestamp ASC
    """, (user_id, subject))

    records = cursor.fetchall()
    conn.close()
    return records
# -----------------------------------------
# FETCH SUBJECT COMPARISON DATA
# -----------------------------------------
def fetch_subject_comparison(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, score, total_questions
        FROM quiz_results
        WHERE user_id = ?
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()
    return records
# -----------------------------------------
# CREATE DOUBTS TABLE
# -----------------------------------------
def create_doubts_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doubts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# INSERT DOUBT
# -----------------------------------------
def insert_doubt(user_id, subject, question, answer):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO doubts (user_id, subject, question, answer)
        VALUES (?, ?, ?, ?)
    """, (user_id, subject, question, answer))

    conn.commit()
    conn.close()
# -----------------------------------------
# CREATE CODING RESULTS TABLE
# -----------------------------------------
def create_coding_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coding_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            level TEXT,
            question TEXT,
            result INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------------------
# INSERT CODING RESULT
# -----------------------------------------
def insert_coding_result(user_id, subject, level, question, result):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO coding_results (user_id, subject, level, question, result)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, subject, level, question, result))

    conn.commit()
    conn.close()


# -----------------------------------------
# FETCH ALL QUIZ DATA (for analytics)
# -----------------------------------------
def fetch_all_quiz_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, level, score, total_questions, timestamp
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records


# -----------------------------------------
# FETCH CODING DATA (for analytics)
# -----------------------------------------
def fetch_coding_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, level, result, timestamp
        FROM coding_results
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records


# -----------------------------------------
# FETCH DOUBTS DATA (for analytics)
# -----------------------------------------
def fetch_doubts_data(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, timestamp
        FROM doubts
        WHERE user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records
