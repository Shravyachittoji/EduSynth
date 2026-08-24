import streamlit as st
import sqlite3
import bcrypt

DB_NAME = "students.db"

# -------- REGISTER --------
def register_user(name, email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# -------- LOGIN --------
def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user:
        user_id, name, stored_password = user
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return {"id": user_id, "name": name}

    return None


# -------- AUTH PAGE --------
def show_auth_page():

    st.title("EduSynth Login System")

    choice = st.radio("Select Option", ["Login", "Register"])

    if choice == "Register":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if name and email and password:
                success = register_user(name, email, password)
                if success:
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Email already exists.")
            else:
                st.warning("Please fill all fields.")

    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.session_state.page = "subject_selection"
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
