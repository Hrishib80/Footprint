import streamlit as st
from passlib.hash import pbkdf2_sha256
from database import db_manager

class AuthManager:
    def __init__(self):
        pass
    
    def load_users(self):
        """Load users from database (compatibility method)"""
        return db_manager.get_all_users()
    
    def login_user(self, username, password, users=None):
        """Verify user login credentials"""
        user = db_manager.get_user(username)
        if user and pbkdf2_sha256.verify(password, user.password_hash):
            return True
        return False
    
    def signup_user(self, username, password):
        """Register a new user"""
        # Check if user already exists
        existing_user = db_manager.get_user(username)
        if existing_user:
            return False, "🚫 Username already exists!"
        
        # Validate username and password
        if len(username.strip()) < 3:
            return False, "🚫 Username must be at least 3 characters long!"
        
        if len(password) < 6:
            return False, "🚫 Password must be at least 6 characters long!"
        
        # Create user in database
        password_hash = pbkdf2_sha256.hash(password)
        success = db_manager.create_user(username.strip(), password_hash)
        
        if success:
            return True, "✅ Signup successful! You can now login."
        else:
            return False, "🚫 Error creating account. Please try again."
    
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
                    if self.login_user(username, password):
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
