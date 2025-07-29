import streamlit as st
import yaml
import os
from datetime import datetime, date

class CO2Tracker:
    def __init__(self):
        self.data_dir = "user_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_user_data_file(self, username):
        """Get the data file path for a specific user"""
        return os.path.join(self.data_dir, f"{username}_co2_data.yaml")
    
    def load_user_data(self, username):
        """Load CO₂ data for a specific user"""
        file_path = self.get_user_data_file(username)
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data if data else []
    
    def save_user_data(self, username, data):
        """Save CO₂ data for a specific user"""
        file_path = self.get_user_data_file(username)
        with open(file_path, "w") as f:
            yaml.dump(data, f)
    
    def clear_user_data(self, username):
        """Clear all CO₂ data for a specific user"""
        file_path = self.get_user_data_file(username)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def add_emission_entry(self, username, entry):
        """Add a new emission entry for a user"""
        data = self.load_user_data(username)
        data.append(entry)
        self.save_user_data(username, data)
    
    def show_tracker(self, username):
        """Display the CO₂ tracking interface"""
        st.title("🌱 Track Your CO₂ Emissions")
        st.markdown("Add your daily activities to track your carbon footprint")
        
        # Tabs for different tracking methods
        tab1, tab2, tab3 = st.tabs(["📝 Quick Entry", "📊 Detailed Entry", "📋 View History"])
        
        with tab1:
            self.show_quick_entry_form(username)
        
        with tab2:
            self.show_detailed_entry_form(username)
        
        with tab3:
            self.show_entry_history(username)
    
    def show_quick_entry_form(self, username):
        """Show quick entry form for common activities"""
        st.subheader("⚡ Quick Entry")
        st.markdown("Select from common activities with pre-calculated CO₂ values")
        
        # Predefined activities with CO₂ factors (kg CO₂)
        quick_activities = {
            "🚗 Car trip (10 km)": {"category": "Transportation", "co2": 2.31},
            "🚌 Bus trip (10 km)": {"category": "Transportation", "co2": 0.89},
            "🚊 Train trip (10 km)": {"category": "Transportation", "co2": 0.41},
            "✈️ Domestic flight (1000 km)": {"category": "Transportation", "co2": 254.0},
            "💡 Home electricity (1 day avg)": {"category": "Energy", "co2": 6.8},
            "🔥 Natural gas heating (1 day)": {"category": "Energy", "co2": 5.3},
            "🥩 Beef meal": {"category": "Food", "co2": 6.61},
            "🐔 Chicken meal": {"category": "Food", "co2": 1.57},
            "🌱 Vegetarian meal": {"category": "Food", "co2": 0.38},
            "🛒 Grocery shopping": {"category": "Shopping", "co2": 3.2},
        }
        
        with st.form("quick_entry_form"):
            selected_activity = st.selectbox(
                "Select Activity:",
                options=list(quick_activities.keys())
            )
            
            activity_data = quick_activities[selected_activity]
            
            col1, col2 = st.columns(2)
            with col1:
                quantity = st.number_input("Quantity/Times:", min_value=0.1, value=1.0, step=0.1)
            with col2:
                entry_date = st.date_input("Date:", value=date.today())
            
            estimated_co2 = activity_data["co2"] * quantity
            st.info(f"Estimated CO₂: **{estimated_co2:.2f} kg**")
            
            notes = st.text_area("Additional Notes (optional):", placeholder="Any additional details...")
            
            submit_btn = st.form_submit_button("➕ Add Entry", use_container_width=True)
            
            if submit_btn:
                entry = {
                    "date": entry_date.isoformat(),
                    "activity": selected_activity,
                    "category": activity_data["category"],
                    "co2_amount": round(estimated_co2, 2),
                    "quantity": quantity,
                    "notes": notes,
                    "entry_type": "quick",
                    "timestamp": datetime.now().isoformat()
                }
                
                self.add_emission_entry(username, entry)
                st.success(f"✅ Added {selected_activity} ({estimated_co2:.2f} kg CO₂)")
                st.rerun()
    
    def show_detailed_entry_form(self, username):
        """Show detailed entry form for custom activities"""
        st.subheader("📝 Detailed Entry")
        st.markdown("Create custom entries with your own CO₂ calculations")
        
        with st.form("detailed_entry_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_name = st.text_input("Activity Description:", placeholder="e.g., Drove to work")
                category = st.selectbox(
                    "Category:",
                    ["Transportation", "Energy", "Food", "Shopping", "Home", "Work", "Other"]
                )
            
            with col2:
                co2_amount = st.number_input("CO₂ Amount (kg):", min_value=0.0, step=0.01, format="%.2f")
                entry_date = st.date_input("Date:", value=date.today())
            
            # Additional details
            col3, col4 = st.columns(2)
            with col3:
                distance = st.number_input("Distance (km, optional):", min_value=0.0, step=0.1, format="%.1f")
            with col4:
                duration = st.number_input("Duration (hours, optional):", min_value=0.0, step=0.1, format="%.1f")
            
            notes = st.text_area("Notes:", placeholder="Additional details, calculation method, etc...")
            
            submit_btn = st.form_submit_button("➕ Add Detailed Entry", use_container_width=True)
            
            if submit_btn:
                if not activity_name.strip():
                    st.error("❌ Please provide an activity description.")
                elif co2_amount <= 0:
                    st.error("❌ CO₂ amount must be greater than 0.")
                else:
                    entry = {
                        "date": entry_date.isoformat(),
                        "activity": activity_name.strip(),
                        "category": category,
                        "co2_amount": round(co2_amount, 2),
                        "distance": distance if distance > 0 else None,
                        "duration": duration if duration > 0 else None,
                        "notes": notes,
                        "entry_type": "detailed",
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    self.add_emission_entry(username, entry)
                    st.success(f"✅ Added {activity_name} ({co2_amount:.2f} kg CO₂)")
                    st.rerun()
    
    def show_entry_history(self, username):
        """Show history of CO₂ entries"""
        st.subheader("📋 Entry History")
        
        data = self.load_user_data(username)
        
        if not data:
            st.info("No entries found. Start tracking your CO₂ emissions using the forms above!")
            return
        
        # Sort by date (newest first)
        sorted_data = sorted(data, key=lambda x: x['date'], reverse=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categories = ["All"] + list(set(entry['category'] for entry in data))
            selected_category = st.selectbox("Filter by Category:", categories)
        
        # Get date range for filters
        if data:
            min_date = min(datetime.fromisoformat(entry['date']).date() for entry in data)
            max_date = max(datetime.fromisoformat(entry['date']).date() for entry in data)
        else:
            min_date = max_date = datetime.now().date()

        with col2:
            start_date = st.date_input("From Date:", value=min_date, min_value=min_date, max_value=max_date)
        
        with col3:
            end_date = st.date_input("To Date:", value=max_date, min_value=min_date, max_value=max_date)
        
        # Filter data
        filtered_data = sorted_data
        if selected_category != "All":
            filtered_data = [entry for entry in filtered_data if entry['category'] == selected_category]
        
        if data:  # Only apply date filter if we have data
            filtered_data = [
                entry for entry in filtered_data
                if start_date <= datetime.fromisoformat(entry['date']).date() <= end_date
            ]
        
        # Display summary
        if filtered_data:
            total_filtered_co2 = sum(entry['co2_amount'] for entry in filtered_data)
            st.metric("Total CO₂ in Selection:", f"{total_filtered_co2:.2f} kg")
        
        # Display entries
        st.markdown("---")
        
        for i, entry in enumerate(filtered_data):
            with st.expander(
                f"📅 {entry['date']} - {entry['activity']} ({entry['co2_amount']} kg CO₂)",
                expanded=i < 5  # Expand first 5 entries
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Category:** {entry['category']}")
                    st.write(f"**CO₂ Amount:** {entry['co2_amount']} kg")
                    if entry.get('distance'):
                        st.write(f"**Distance:** {entry['distance']} km")
                    if entry.get('duration'):
                        st.write(f"**Duration:** {entry['duration']} hours")
                
                with col2:
                    st.write(f"**Entry Type:** {entry.get('entry_type', 'unknown').title()}")
                    if entry.get('quantity'):
                        st.write(f"**Quantity:** {entry['quantity']}")
                    if entry.get('timestamp'):
                        timestamp = datetime.fromisoformat(entry['timestamp'])
                        st.write(f"**Added:** {timestamp.strftime('%Y-%m-%d %H:%M')}")
                
                if entry.get('notes'):
                    st.write(f"**Notes:** {entry['notes']}")
                
                # Delete button
                if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                    st.warning(f"⚠️ Delete this entry: {entry['activity']}?")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Yes, Delete", type="primary", key=f"confirm_delete_{i}"):
                            data.remove(entry)
                            self.save_user_data(username, data)
                            st.success("Entry deleted!")
                            st.rerun()
                    with col2:
                        if st.button("Cancel", type="secondary", key=f"cancel_delete_{i}"):
                            st.rerun()
        
        if not filtered_data:
            st.info("No entries match the selected filters.")
