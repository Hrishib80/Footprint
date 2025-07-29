import streamlit as st
import yaml
import os
from passlib.hash import pbkdf2_sha256

class AuthManager:
    def __init__(self):
        self.user_file = "users.yaml"
    
    def load_users(self):
        """Load users from YAML file"""
        if not os.path.exists(self.user_file):
            return {}
        with open(self.user_file, "r") as f:
            return yaml.safe_load(f) or {}
    
    def save_users(self, users):
        """Save users to YAML file"""
        with open(self.user_file, "w") as f:
            yaml.dump(users, f)
    
    def login_user(self, username, password, users):
        """Verify user login credentials"""
        if username in users and pbkdf2_sha256.verify(password, users[username]['password']):
            return True
        return False
    
    def signup_user(self, username, password):
        """Register a new user"""
        users = self.load_users()
        if username in users:
            return False, "🚫 Username already exists!"
        
        # Validate username and password
        if len(username.strip()) < 3:
            return False, "🚫 Username must be at least 3 characters long!"
        
        if len(password) < 6:
            return False, "🚫 Password must be at least 6 characters long!"
        
        users[username] = {
            "password": pbkdf2_sha256.hash(password),
            "created_at": str(st.session_state.get('current_time', 'Unknown'))
        }
        self.save_users(users)
        return True, "✅ Signup successful! You can now login."
    
    def show_auth_page(self):
        """Display the authentication page"""
        st.title("🔐 CO₂ Tracker Login")
        st.markdown("Track your carbon footprint and make a difference!")
        
        # Create tabs for login and signup
        tab1, tab2 = st.tabs(["🔓 Login", "📝 Sign Up"])
        
        with tab1:
            self.show_login_form()
        
        with tab2:
            self.show_signup_form()
    
    def show_login_form(self):
        """Display login form"""
        st.subheader("Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if login_btn:
                if not username.strip() or not password.strip():
                    st.error("❌ Please enter both username and password.")
                else:
                    users = self.load_users()
                    if self.login_user(username, password, users):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success(f"✅ Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password.")
    
    def show_signup_form(self):
        """Display signup form"""
        st.subheader("Create New Account")
        
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username", placeholder="At least 3 characters")
            new_password = st.text_input("Choose Password", type="password", placeholder="At least 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            signup_btn = st.form_submit_button("📝 Create Account", use_container_width=True)
            
            if signup_btn:
                if not new_username.strip() or not new_password.strip() or not confirm_password.strip():
                    st.error("❌ All fields are required.")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match.")
                else:
                    success, message = self.signup_user(new_username.strip(), new_password)
                    if success:
                        st.success(message)
                        st.info("👈 Please switch to the Login tab to sign in with your new account.")
                    else:
                        st.error(message)
