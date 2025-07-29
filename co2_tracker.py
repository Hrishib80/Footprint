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
        # Modern header with green gradient
        st.markdown("""
        <div style='background: linear-gradient(90deg, #00C851, #00A040); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0; text-align: center;'>🌱 Track Your CO₂ Emissions</h1>
            <p style='color: white; margin: 5px 0 0 0; text-align: center; opacity: 0.9;'>Add your daily activities to track your carbon footprint</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # Predefined activities with CO₂ factors (kg CO₂) - Enhanced list
        quick_activities = {
            "🚗 Car trip (10 km)": {"category": "Transportation", "co2": 2.31, "fuel_type": "gasoline"},
            "🚙 SUV trip (10 km)": {"category": "Transportation", "co2": 3.2, "fuel_type": "gasoline"},
            "🚗 Electric car (10 km)": {"category": "Transportation", "co2": 0.5, "fuel_type": "electric"},
            "🏍️ Motorcycle (10 km)": {"category": "Transportation", "co2": 1.8, "fuel_type": "gasoline"},
            "🚌 Bus trip (10 km)": {"category": "Transportation", "co2": 0.89, "occupancy": "shared"},
            "🚊 Train trip (10 km)": {"category": "Transportation", "co2": 0.41, "occupancy": "shared"},
            "🚇 Metro/Subway (10 km)": {"category": "Transportation", "co2": 0.28, "occupancy": "shared"},
            "🚲 Bike ride (10 km)": {"category": "Transportation", "co2": 0.0, "eco_friendly": True},
            "🚶 Walking (5 km)": {"category": "Transportation", "co2": 0.0, "eco_friendly": True},
            "✈️ Domestic flight (1000 km)": {"category": "Transportation", "co2": 254.0, "distance": "long"},
            "✈️ International flight (3000 km)": {"category": "Transportation", "co2": 820.0, "distance": "very_long"},
            "💡 Home electricity (1 day avg)": {"category": "Energy", "co2": 6.8, "source": "grid"},
            "☀️ Solar electricity (1 day)": {"category": "Energy", "co2": 0.2, "source": "renewable"},
            "🔥 Natural gas heating (1 day)": {"category": "Energy", "co2": 5.3, "source": "fossil"},
            "🔥 Oil heating (1 day)": {"category": "Energy", "co2": 7.1, "source": "fossil"},
            "💡 LED lights (8 hours)": {"category": "Energy", "co2": 0.8, "efficiency": "high"},
            "🥩 Beef meal": {"category": "Food", "co2": 6.61, "protein": "red_meat"},
            "🐔 Chicken meal": {"category": "Food", "co2": 1.57, "protein": "white_meat"},
            "🐟 Fish meal": {"category": "Food", "co2": 2.87, "protein": "seafood"},
            "🥛 Dairy meal": {"category": "Food", "co2": 3.2, "protein": "dairy"},
            "🌱 Vegetarian meal": {"category": "Food", "co2": 0.38, "protein": "plant", "eco_friendly": True},
            "🌿 Vegan meal": {"category": "Food", "co2": 0.22, "protein": "plant", "eco_friendly": True},
            "☕ Coffee (1 cup)": {"category": "Food", "co2": 0.37, "beverage": True},
            "🍺 Beer (1 bottle)": {"category": "Food", "co2": 0.74, "beverage": True},
            "🛒 Grocery shopping": {"category": "Shopping", "co2": 3.2, "type": "essentials"},
            "👕 Clothing purchase": {"category": "Shopping", "co2": 8.5, "type": "apparel"},
            "📱 Electronics purchase": {"category": "Shopping", "co2": 85.0, "type": "electronics"},
            "🏠 Home heating (1 day)": {"category": "Home", "co2": 12.5, "system": "HVAC"},
            "❄️ Air conditioning (8 hours)": {"category": "Home", "co2": 8.9, "system": "cooling"},
            "🚿 Hot shower (10 min)": {"category": "Home", "co2": 2.3, "water": "heated"},
            "🧺 Laundry load": {"category": "Home", "co2": 2.8, "appliance": "washing"},
            "💻 Work from home (8 hours)": {"category": "Work", "co2": 4.6, "location": "remote"},
            "🏢 Office work (8 hours)": {"category": "Work", "co2": 6.2, "location": "office"},
        }
        
        with st.form("quick_entry_form"):
            selected_activity = st.selectbox(
                "Select Activity:",
                options=list(quick_activities.keys())
            )
            
            activity_data = quick_activities[selected_activity]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                quantity = st.number_input("Quantity/Times:", min_value=0.1, value=1.0, step=0.1)
            with col2:
                entry_date = st.date_input("Date:", value=date.today())
            with col3:
                # Show activity attributes
                activity_attrs = {k: v for k, v in activity_data.items() if k not in ['category', 'co2']}
                if activity_attrs:
                    attr_text = ", ".join([f"{k}: {v}" for k, v in activity_attrs.items()])
                    st.info(f"Attributes: {attr_text}")
            
            estimated_co2 = activity_data["co2"] * quantity
            
            # Color-coded CO2 estimate
            if estimated_co2 < 1:
                co2_color = "🟢"  # Green for low
            elif estimated_co2 < 5:
                co2_color = "🟡"  # Yellow for medium
            else:
                co2_color = "🔴"  # Red for high
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E8, #F0FFF0); padding: 10px; border-radius: 5px; margin: 10px 0;'>
                <h4 style='margin: 0; color: #1B5E20;'>{co2_color} Estimated CO₂: <span style='color: #00C851;'>{estimated_co2:.2f} kg</span></h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced form fields
            col4, col5 = st.columns(2)
            with col4:
                location = st.text_input("Location (optional):", placeholder="e.g., City, Route")
            with col5:
                weather = st.selectbox("Weather (optional):", ["", "Sunny", "Rainy", "Cloudy", "Snowy", "Windy"])
            
            notes = st.text_area("Additional Notes (optional):", placeholder="Any additional details, companions, purpose of trip, etc...")
            
            submit_btn = st.form_submit_button("➕ Add Entry", use_container_width=True)
            
            if submit_btn:
                entry = {
                    "date": entry_date.isoformat(),
                    "activity": selected_activity,
                    "category": activity_data["category"],
                    "co2_amount": round(estimated_co2, 2),
                    "quantity": quantity,
                    "location": location if location.strip() else None,
                    "weather": weather if weather else None,
                    "notes": notes,
                    "entry_type": "quick",
                    "timestamp": datetime.now().isoformat(),
                    "attributes": {k: v for k, v in activity_data.items() if k not in ['category', 'co2']}
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
            
            # Additional details - Enhanced
            col3, col4 = st.columns(2)
            with col3:
                distance = st.number_input("Distance (km, optional):", min_value=0.0, step=0.1, format="%.1f")
            with col4:
                duration = st.number_input("Duration (hours, optional):", min_value=0.0, step=0.1, format="%.1f")
            
            # More attributes
            col5, col6 = st.columns(2)
            with col5:
                participants = st.number_input("Number of people involved:", min_value=1, value=1, step=1)
                location = st.text_input("Location:", placeholder="City, country, route")
            with col6:
                purpose = st.selectbox("Purpose:", ["", "Work", "Personal", "Recreation", "Essential", "Emergency"])
                efficiency = st.selectbox("Efficiency rating:", ["", "Very High", "High", "Medium", "Low", "Very Low"])
            
            notes = st.text_area("Notes:", placeholder="Additional details, calculation method, alternatives considered, etc...")
            
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
                        "participants": participants,
                        "location": location if location.strip() else None,
                        "purpose": purpose if purpose else None,
                        "efficiency": efficiency if efficiency else None,
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
        
        with col2:
            # Date range filter
            if data:
                min_date = min(datetime.fromisoformat(entry['date']).date() for entry in data)
                max_date = max(datetime.fromisoformat(entry['date']).date() for entry in data)
                start_date = st.date_input("From Date:", value=min_date, min_value=min_date, max_value=max_date)
        
        with col3:
            if data:
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
                    if entry.get('participants'):
                        st.write(f"**People involved:** {entry['participants']}")
                    if entry.get('location'):
                        st.write(f"**Location:** {entry['location']}")
                
                with col2:
                    st.write(f"**Entry Type:** {entry.get('entry_type', 'unknown').title()}")
                    if entry.get('quantity'):
                        st.write(f"**Quantity:** {entry['quantity']}")
                    if entry.get('purpose'):
                        st.write(f"**Purpose:** {entry['purpose']}")
                    if entry.get('efficiency'):
                        st.write(f"**Efficiency:** {entry['efficiency']}")
                    if entry.get('weather'):
                        st.write(f"**Weather:** {entry['weather']}")
                    if entry.get('timestamp'):
                        timestamp = datetime.fromisoformat(entry['timestamp'])
                        st.write(f"**Added:** {timestamp.strftime('%Y-%m-%d %H:%M')}")
                
                # Show attributes if available
                if entry.get('attributes'):
                    st.write("**Activity Attributes:**")
                    attrs = entry['attributes']
                    attr_text = ", ".join([f"{k}: {v}" for k, v in attrs.items()])
                    st.caption(attr_text)
                
                if entry.get('notes'):
                    st.write(f"**Notes:** {entry['notes']}")
                
                # Delete button
                if st.button(f"🗑️ Delete", key=f"delete_{i}", type="secondary"):
                    # Simple confirmation using session state
                    confirm_key = f"confirm_delete_{i}"
                    if confirm_key not in st.session_state:
                        st.session_state[confirm_key] = False
                    
                    if not st.session_state[confirm_key]:
                        st.session_state[confirm_key] = True
                        st.warning(f"⚠️ Are you sure you want to delete: **{entry['activity']}**?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("✅ Yes, Delete", key=f"yes_{i}"):
                                data.remove(entry)
                                self.save_user_data(username, data)
                                st.success("Entry deleted!")
                                st.rerun()
                        with col_no:
                            if st.button("❌ Cancel", key=f"no_{i}"):
                                st.session_state[confirm_key] = False
                                st.rerun()
        
        if not filtered_data:
            st.info("No entries match the selected filters.")
