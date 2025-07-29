import streamlit as st
from auth import AuthManager
from dashboard import Dashboard
from co2_tracker import CO2Tracker

# Configure the app
st.set_page_config(
    page_title="🌍 CO₂ Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "auth"

# Initialize managers
auth_manager = AuthManager()
dashboard = Dashboard()
co2_tracker = CO2Tracker()

def logout():
    """Handle user logout"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.current_page = "auth"
    st.rerun()

def main():
    """Main application logic"""
    
    # If not authenticated, show authentication page
    if not st.session_state.authenticated:
        auth_manager.show_auth_page()
        return
    
    # Sidebar navigation for authenticated users
    with st.sidebar:
        st.title("🌍 CO₂ Tracker")
        st.markdown(f"**Welcome, {st.session_state.username}!**")
        st.markdown("---")
        
        # Navigation menu
        page = st.radio(
            "Navigate to:",
            ["Dashboard", "Track CO₂", "Profile"],
            key="navigation"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content area
    if page == "Dashboard":
        dashboard.show_dashboard(st.session_state.username)
    elif page == "Track CO₂":
        co2_tracker.show_tracker(st.session_state.username)
    elif page == "Profile":
        show_profile()

def show_profile():
    """Show user profile page"""
    st.title("👤 User Profile")
    st.subheader(f"Username: {st.session_state.username}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Account Information**")
        st.write(f"• Username: {st.session_state.username}")
        st.write(f"• Account Status: Active")
        
    with col2:
        st.info("**Carbon Tracking Stats**")
        # Get user's tracking statistics
        user_data = co2_tracker.load_user_data(st.session_state.username)
        total_entries = len(user_data) if user_data else 0
        st.write(f"• Total Entries: {total_entries}")
        
        if user_data:
            total_emissions = sum(entry.get('co2_amount', 0) for entry in user_data)
            st.write(f"• Total CO₂ Tracked: {total_emissions:.2f} kg")
    
    st.markdown("---")
    st.subheader("🔧 Account Actions")
    
    if st.button("🗑️ Clear All CO₂ Data", type="secondary"):
        if st.confirm("Are you sure you want to delete all your CO₂ tracking data? This action cannot be undone."):
            co2_tracker.clear_user_data(st.session_state.username)
            st.success("All CO₂ data has been cleared!")
            st.rerun()

if __name__ == "__main__":
    main()
