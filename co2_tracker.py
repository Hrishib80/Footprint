import streamlit as st
from datetime import datetime, date
from database import db_manager

class CO2Tracker:
    def __init__(self):
        pass
    
    def load_user_data(self, username):
        """Load CO₂ data for a specific user from database"""
        return db_manager.get_user_co2_entries(username)
    
    def save_user_data(self, username, data):
        """Save CO₂ data for a specific user (compatibility method - not used with database)"""
        # This method is kept for compatibility but not used with database
        pass
    
    def clear_user_data(self, username):
        """Clear all CO₂ data for a specific user"""
        return db_manager.clear_user_co2_entries(username)
    
    def add_emission_entry(self, username, entry):
        """Add a new emission entry for a user"""
        return db_manager.add_co2_entry(username, entry)
    
    def show_tracker(self, username):
        """Display the CO₂ tracking interface"""
        # Modern header with green gradient
        st.markdown("""
        <div style='background: linear-gradient(90deg, #00C851, #00A040); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0; text-align: center;'>🌱 Track Your CO₂ Emissions</h1>
            <p style='color: white; margin: 5px 0 0 0; text-align: center; opacity: 0.9;'>Add your daily activities to track your carbon footprint</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for different activity categories
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚗 Transportation", "🍽️ Diet", "⚡ Electricity", "🏠 Other Activities", "📋 History"])
        
        with tab1:
            self.show_transportation_tracker(username)
        
        with tab2:
            self.show_diet_tracker(username)
        
        with tab3:
            self.show_electricity_tracker(username)
            
        with tab4:
            self.show_other_activities_tracker(username)
        
        with tab5:
            self.show_entry_history(username)
    
    def show_transportation_tracker(self, username):
        """Transportation-specific CO2 tracking with customizable inputs"""
        st.markdown("### 🚗 Transportation Emissions")
        st.markdown("Track your travel-related carbon footprint")
        
        transportation_activities = {
            "🚗 Car (Gasoline)": {"base_co2": 0.231, "unit": "per km"},
            "🚙 SUV (Gasoline)": {"base_co2": 0.32, "unit": "per km"},
            "🚗 Electric Car": {"base_co2": 0.05, "unit": "per km"},
            "🏍️ Motorcycle": {"base_co2": 0.18, "unit": "per km"},
            "🚌 Bus": {"base_co2": 0.089, "unit": "per km"},
            "🚊 Train": {"base_co2": 0.041, "unit": "per km"},
            "🚇 Metro/Subway": {"base_co2": 0.028, "unit": "per km"},
            "✈️ Domestic Flight": {"base_co2": 0.254, "unit": "per km"},
            "✈️ International Flight": {"base_co2": 0.273, "unit": "per km"},
            "🚲 Bicycle": {"base_co2": 0.0, "unit": "per km"},
            "🚶 Walking": {"base_co2": 0.0, "unit": "per km"}
        }
        
        with st.form("transportation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                transport_type = st.selectbox("Transportation Type:", 
                                            options=list(transportation_activities.keys()))
                distance = st.number_input("Distance (km):", min_value=0.1, value=10.0, step=0.1)
                passengers = st.number_input("Number of passengers:", min_value=1, value=1, step=1)
            
            with col2:
                entry_date = st.date_input("Date:", value=date.today())
                fuel_efficiency = st.selectbox("Fuel Efficiency:", 
                                             ["Average", "High Efficiency", "Low Efficiency"])
                purpose = st.selectbox("Trip Purpose:", 
                                     ["Commute", "Business", "Leisure", "Shopping", "Other"])
            
            # Additional attributes
            st.markdown("**Optional Details:**")
            col3, col4 = st.columns(2)
            with col3:
                weather = st.selectbox("Weather Conditions:", 
                                     ["Clear", "Rainy", "Snowy", "Windy", "Hot", "Cold"])
                location = st.text_input("Location/Route:", placeholder="e.g., City center to airport")
            
            with col4:
                traffic = st.selectbox("Traffic Conditions:", 
                                     ["Light", "Moderate", "Heavy"])
                notes = st.text_area("Additional Notes:", placeholder="Any extra details...")
            
            # Calculate CO2
            base_co2 = transportation_activities[transport_type]["base_co2"]
            
            # Adjust for efficiency
            efficiency_multiplier = {"Average": 1.0, "High Efficiency": 0.8, "Low Efficiency": 1.3}
            adjusted_co2 = base_co2 * efficiency_multiplier[fuel_efficiency]
            
            # Adjust for passengers (shared transport reduces per-person emissions)
            if passengers > 1 and transport_type not in ["🚲 Bicycle", "🚶 Walking"]:
                adjusted_co2 = adjusted_co2 / passengers
            
            total_co2 = adjusted_co2 * distance
            
            # CO2 display
            if total_co2 < 1:
                co2_color = "#4CAF50"  # Green
                emoji = "🟢"
            elif total_co2 < 5:
                co2_color = "#FF9800"  # Orange  
                emoji = "🟡"
            else:
                co2_color = "#F44336"  # Red
                emoji = "🔴"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E8, #F0FFF0); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid {co2_color};'>
                <h4 style='margin: 0; color: #1B5E20;'>{emoji} Total CO₂ Emissions: <span style='color: {co2_color}; font-weight: bold;'>{total_co2:.2f} kg</span></h4>
                <p style='margin: 5px 0 0 0; color: #2E7D32; font-size: 0.9em;'>Base: {base_co2:.3f} kg/km × {distance} km × efficiency factor</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("🚗 Add Transportation Entry", use_container_width=True):
                entry_data = {
                    "activity": transport_type,
                    "category": "Transportation",
                    "date": entry_date.isoformat(),
                    "co2_amount": round(total_co2, 2),
                    "distance": distance,
                    "participants": passengers,
                    "purpose": purpose,
                    "weather": weather,
                    "location": location,
                    "efficiency": fuel_efficiency,
                    "notes": notes,
                    "entry_type": "transportation",
                    "attributes": {
                        "fuel_efficiency": fuel_efficiency,
                        "traffic": traffic,
                        "base_co2_per_km": base_co2
                    }
                }
                
                if self.add_emission_entry(username, entry_data):
                    st.success(f"Transportation entry added! Total CO₂: {total_co2:.2f} kg")
                    st.rerun()
                else:
                    st.error("Failed to add entry. Please try again.")

    def show_diet_tracker(self, username):
        """Diet-specific CO2 tracking with meal customization"""
        st.markdown("### 🍽️ Diet & Food Emissions")
        st.markdown("Track the carbon footprint of your meals and beverages")
        
        food_items = {
            "🥩 Beef": {"base_co2": 27.0, "unit": "per kg"},
            "🐄 Lamb": {"base_co2": 39.2, "unit": "per kg"},
            "🐷 Pork": {"base_co2": 12.1, "unit": "per kg"},
            "🐔 Chicken": {"base_co2": 6.9, "unit": "per kg"},
            "🐟 Fish (Farmed)": {"base_co2": 13.6, "unit": "per kg"},
            "🦐 Seafood": {"base_co2": 18.2, "unit": "per kg"},
            "🥛 Dairy Milk": {"base_co2": 3.2, "unit": "per liter"},
            "🧀 Cheese": {"base_co2": 13.5, "unit": "per kg"},
            "🥚 Eggs": {"base_co2": 4.2, "unit": "per kg"},
            "🍞 Bread": {"base_co2": 1.3, "unit": "per kg"},
            "🍚 Rice": {"base_co2": 2.7, "unit": "per kg"},
            "🥔 Potatoes": {"base_co2": 0.5, "unit": "per kg"},
            "🥕 Vegetables": {"base_co2": 2.0, "unit": "per kg"},
            "🍎 Fruits": {"base_co2": 1.1, "unit": "per kg"},
            "🌱 Legumes/Beans": {"base_co2": 0.7, "unit": "per kg"},
            "🥜 Nuts": {"base_co2": 2.3, "unit": "per kg"},
            "☕ Coffee": {"base_co2": 16.9, "unit": "per kg"},
            "🍺 Beer": {"base_co2": 1.3, "unit": "per liter"},
            "🍷 Wine": {"base_co2": 2.9, "unit": "per liter"}
        }
        
        with st.form("diet_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                food_type = st.selectbox("Food/Beverage:", options=list(food_items.keys()))
                quantity = st.number_input("Quantity (kg/liters):", min_value=0.01, value=0.5, step=0.01)
                meal_type = st.selectbox("Meal Type:", 
                                       ["Breakfast", "Lunch", "Dinner", "Snack", "Beverage"])
            
            with col2:
                entry_date = st.date_input("Date:", value=date.today())
                preparation = st.selectbox("Preparation Method:", 
                                        ["Home Cooked", "Restaurant", "Fast Food", "Processed"])
                dietary_preference = st.selectbox("Dietary Preference:", 
                                                ["Omnivore", "Vegetarian", "Vegan", "Pescatarian"])
            
            # Additional details
            st.markdown("**Meal Details:**")
            col3, col4 = st.columns(2)
            with col3:
                origin = st.selectbox("Food Origin:", 
                                    ["Local", "Regional", "National", "International"])
                organic = st.checkbox("Organic/Sustainable")
            
            with col4:
                waste = st.slider("Food Waste %:", 0, 50, 10)
                notes = st.text_area("Meal Notes:", placeholder="Describe your meal...")
            
            # Calculate CO2
            base_co2 = food_items[food_type]["base_co2"]
            
            # Adjust for origin
            origin_multiplier = {"Local": 1.0, "Regional": 1.2, "National": 1.5, "International": 2.0}
            origin_co2 = base_co2 * origin_multiplier[origin]
            
            # Adjust for preparation
            prep_multiplier = {"Home Cooked": 1.0, "Restaurant": 1.3, "Fast Food": 1.8, "Processed": 1.5}
            prep_co2 = origin_co2 * prep_multiplier[preparation]
            
            # Adjust for organic (typically slightly higher but more sustainable)
            if organic:
                prep_co2 *= 0.9  # Slight reduction for sustainable practices
            
            # Account for waste
            waste_factor = 1 + (waste / 100)
            total_co2 = prep_co2 * quantity * waste_factor
            
            # CO2 display with dietary impact
            if total_co2 < 1:
                co2_color = "#4CAF50"
                emoji = "🟢"
            elif total_co2 < 5:
                co2_color = "#FF9800"
                emoji = "🟡"
            else:
                co2_color = "#F44336"
                emoji = "🔴"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FFF3E0, #FFF8F0); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid {co2_color};'>
                <h4 style='margin: 0; color: #E65100;'>{emoji} Total CO₂: <span style='color: {co2_color}; font-weight: bold;'>{total_co2:.2f} kg</span></h4>
                <p style='margin: 5px 0 0 0; color: #F57C00; font-size: 0.9em;'>Base: {base_co2:.1f} kg × {quantity} kg × origin × preparation factors</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("🍽️ Add Diet Entry", use_container_width=True):
                entry_data = {
                    "activity": food_type,
                    "category": "Diet",
                    "date": entry_date.isoformat(),
                    "co2_amount": round(total_co2, 2),
                    "quantity": quantity,
                    "purpose": meal_type,
                    "notes": notes,
                    "entry_type": "diet",
                    "attributes": {
                        "preparation": preparation,
                        "origin": origin,
                        "organic": organic,
                        "dietary_preference": dietary_preference,
                        "waste_percent": waste,
                        "base_co2_per_unit": base_co2
                    }
                }
                
                if self.add_emission_entry(username, entry_data):
                    st.success(f"Diet entry added! CO₂ from food: {total_co2:.2f} kg")
                    st.rerun()
                else:
                    st.error("Failed to add entry. Please try again.")

    def show_electricity_tracker(self, username):
        """Electricity and energy consumption tracking"""
        st.markdown("### ⚡ Electricity & Energy Consumption")
        st.markdown("Track your home and work energy usage")
        
        energy_sources = {
            "💡 Grid Electricity": {"base_co2": 0.68, "unit": "per kWh"},
            "☀️ Solar Energy": {"base_co2": 0.02, "unit": "per kWh"},
            "💨 Wind Energy": {"base_co2": 0.01, "unit": "per kWh"},
            "💧 Hydroelectric": {"base_co2": 0.024, "unit": "per kWh"},
            "⚛️ Nuclear": {"base_co2": 0.012, "unit": "per kWh"},
            "🔥 Natural Gas": {"base_co2": 0.49, "unit": "per kWh"},
            "⛽ Oil": {"base_co2": 0.82, "unit": "per kWh"},
            "⚫ Coal": {"base_co2": 1.05, "unit": "per kWh"}
        }
        
        appliances = {
            "🏠 Whole House": {"avg_kwh": 30, "duration": "daily"},
            "❄️ Air Conditioning": {"avg_kwh": 3.5, "duration": "hourly"},
            "🔥 Heating System": {"avg_kwh": 4.0, "duration": "hourly"},
            "🌊 Water Heater": {"avg_kwh": 4.5, "duration": "hourly"},
            "❄️ Refrigerator": {"avg_kwh": 0.15, "duration": "hourly"},
            "🧺 Washing Machine": {"avg_kwh": 2.3, "duration": "per load"},
            "👔 Dryer": {"avg_kwh": 3.3, "duration": "per load"},
            "📺 TV": {"avg_kwh": 0.15, "duration": "hourly"},
            "💻 Computer": {"avg_kwh": 0.3, "duration": "hourly"},
            "💡 LED Lights": {"avg_kwh": 0.01, "duration": "hourly"},
            "🍳 Electric Stove": {"avg_kwh": 2.3, "duration": "hourly"}
        }
        
        with st.form("electricity_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                energy_source = st.selectbox("Energy Source:", options=list(energy_sources.keys()))
                appliance = st.selectbox("Appliance/Usage:", options=list(appliances.keys()))
                
                # Get suggested kWh based on appliance
                suggested_kwh = appliances[appliance]["avg_kwh"]
                duration_type = appliances[appliance]["duration"]
                
                usage_kwh = st.number_input(f"Energy Used (kWh):", 
                                          min_value=0.01, 
                                          value=float(suggested_kwh), 
                                          step=0.01,
                                          help=f"Average for {appliance}: {suggested_kwh} kWh {duration_type}")
            
            with col2:
                entry_date = st.date_input("Date:", value=date.today())
                usage_duration = st.number_input("Usage Duration (hours):", min_value=0.1, value=1.0, step=0.1)
                efficiency_rating = st.selectbox("Appliance Efficiency:", 
                                               ["Standard", "Energy Star", "High Efficiency", "Old/Inefficient"])
            
            # Additional details
            st.markdown("**Energy Details:**")
            col3, col4 = st.columns(2)
            with col3:
                time_of_use = st.selectbox("Time of Use:", 
                                         ["Peak Hours", "Off-Peak", "Weekend", "Night"])
                renewable_mix = st.slider("Renewable Energy Mix %:", 0, 100, 30)
            
            with col4:
                location = st.text_input("Location:", placeholder="e.g., Home, Office")
                notes = st.text_area("Usage Notes:", placeholder="Additional details...")
            
            # Calculate CO2
            base_co2 = energy_sources[energy_source]["base_co2"]
            
            # Adjust for efficiency
            efficiency_multiplier = {
                "Standard": 1.0, 
                "Energy Star": 0.8, 
                "High Efficiency": 0.7, 
                "Old/Inefficient": 1.4
            }
            efficient_co2 = base_co2 * efficiency_multiplier[efficiency_rating]
            
            # Adjust for renewable mix (if using grid electricity)
            if "Grid" in energy_source and renewable_mix > 0:
                renewable_reduction = (renewable_mix / 100) * 0.9  # 90% reduction for renewable portion
                efficient_co2 = efficient_co2 * (1 - renewable_reduction)
            
            # Time of use can affect grid CO2 (peak times often use more fossil fuels)
            time_multiplier = {"Peak Hours": 1.2, "Off-Peak": 0.9, "Weekend": 0.95, "Night": 0.85}
            if "Grid" in energy_source:
                efficient_co2 *= time_multiplier[time_of_use]
            
            total_co2 = efficient_co2 * usage_kwh
            
            # CO2 display
            if total_co2 < 2:
                co2_color = "#4CAF50"
                emoji = "🟢"
            elif total_co2 < 10:
                co2_color = "#FF9800"
                emoji = "🟡"
            else:
                co2_color = "#F44336"
                emoji = "🔴"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E3F2FD, #F0F8FF); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid {co2_color};'>
                <h4 style='margin: 0; color: #1565C0;'>{emoji} Total CO₂: <span style='color: {co2_color}; font-weight: bold;'>{total_co2:.2f} kg</span></h4>
                <p style='margin: 5px 0 0 0; color: #1976D2; font-size: 0.9em;'>Base: {base_co2:.3f} kg/kWh × {usage_kwh} kWh × efficiency factor</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("⚡ Add Energy Entry", use_container_width=True):
                entry_data = {
                    "activity": f"{appliance} ({energy_source})",
                    "category": "Energy",
                    "date": entry_date.isoformat(),
                    "co2_amount": round(total_co2, 2),
                    "quantity": usage_kwh,
                    "duration": usage_duration,
                    "location": location,
                    "efficiency": efficiency_rating,
                    "notes": notes,
                    "entry_type": "energy",
                    "attributes": {
                        "energy_source": energy_source,
                        "appliance": appliance,
                        "time_of_use": time_of_use,
                        "renewable_mix": renewable_mix,
                        "base_co2_per_kwh": base_co2
                    }
                }
                
                if self.add_emission_entry(username, entry_data):
                    st.success(f"Energy entry added! CO₂ from electricity: {total_co2:.2f} kg")
                    st.rerun()
                else:
                    st.error("Failed to add entry. Please try again.")

    def show_other_activities_tracker(self, username):
        """Tracker for other activities like shopping, work, entertainment"""
        st.markdown("### 🏠 Other Activities")
        st.markdown("Track emissions from shopping, work, entertainment and lifestyle")
        
        other_activities = {
            "🛒 Grocery Shopping": {"base_co2": 3.2, "unit": "per trip"},
            "👕 Clothing Purchase": {"base_co2": 8.5, "unit": "per item"},
            "📱 Electronics": {"base_co2": 85.0, "unit": "per device"},
            "📦 Online Shopping": {"base_co2": 0.5, "unit": "per package"},
            "🏢 Office Work": {"base_co2": 6.2, "unit": "per day"},
            "💻 Remote Work": {"base_co2": 4.6, "unit": "per day"},
            "🎬 Movie Theater": {"base_co2": 1.8, "unit": "per visit"},
            "🎵 Concert/Event": {"base_co2": 5.5, "unit": "per event"},
            "🏋️ Gym/Fitness": {"base_co2": 2.1, "unit": "per session"},
            "🏥 Medical Visit": {"base_co2": 3.4, "unit": "per visit"},
            "✂️ Package Delivery": {"base_co2": 1.2, "unit": "per package"},
            "🚿 Hot Shower": {"base_co2": 2.3, "unit": "per 10 min"},
            "🧺 Laundry": {"base_co2": 2.8, "unit": "per load"},
            "🗑️ Waste Generation": {"base_co2": 0.5, "unit": "per kg"}
        }
        
        with st.form("other_activities_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                activity_type = st.selectbox("Activity Type:", options=list(other_activities.keys()))
                quantity = st.number_input("Quantity/Times:", min_value=0.1, value=1.0, step=0.1)
                category_sub = st.selectbox("Sub-category:", 
                                          ["Shopping", "Work", "Entertainment", "Health", "Home", "Other"])
            
            with col2:
                entry_date = st.date_input("Date:", value=date.today())
                duration = st.number_input("Duration (hours):", min_value=0.1, value=1.0, step=0.1)
                priority = st.selectbox("Necessity Level:", 
                                      ["Essential", "Important", "Optional", "Luxury"])
            
            # Additional details
            st.markdown("**Activity Details:**")
            col3, col4 = st.columns(2)
            with col3:
                location = st.text_input("Location:", placeholder="e.g., Local mall, Online")
                participants = st.number_input("Number of people:", min_value=1, value=1, step=1)
            
            with col4:
                sustainability = st.selectbox("Sustainability Choice:", 
                                            ["Standard", "Eco-friendly", "Sustainable", "Recycled/Reused"])
                notes = st.text_area("Activity Notes:", placeholder="Additional details...")
            
            # Calculate CO2
            base_co2 = other_activities[activity_type]["base_co2"]
            
            # Adjust for sustainability
            sustainability_multiplier = {
                "Standard": 1.0, 
                "Eco-friendly": 0.7, 
                "Sustainable": 0.5, 
                "Recycled/Reused": 0.3
            }
            sustainable_co2 = base_co2 * sustainability_multiplier[sustainability]
            
            # Adjust for participants (some activities have shared impact)
            if participants > 1 and activity_type in ["🎬 Movie Theater", "🎵 Concert/Event", "🏋️ Gym/Fitness"]:
                sustainable_co2 = sustainable_co2 / participants
            
            total_co2 = sustainable_co2 * quantity
            
            # CO2 display
            if total_co2 < 3:
                co2_color = "#4CAF50"
                emoji = "🟢"
            elif total_co2 < 10:
                co2_color = "#FF9800"
                emoji = "🟡"
            else:
                co2_color = "#F44336"
                emoji = "🔴"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #F3E5F5, #FCE4EC); padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid {co2_color};'>
                <h4 style='margin: 0; color: #7B1FA2;'>{emoji} Total CO₂: <span style='color: {co2_color}; font-weight: bold;'>{total_co2:.2f} kg</span></h4>
                <p style='margin: 5px 0 0 0; color: #8E24AA; font-size: 0.9em;'>Base: {base_co2:.1f} kg × {quantity} × sustainability factor</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("🏠 Add Activity Entry", use_container_width=True):
                entry_data = {
                    "activity": activity_type,
                    "category": category_sub,
                    "date": entry_date.isoformat(),
                    "co2_amount": round(total_co2, 2),
                    "quantity": quantity,
                    "duration": duration,
                    "participants": participants,
                    "location": location,
                    "purpose": priority,
                    "notes": notes,
                    "entry_type": "other",
                    "attributes": {
                        "sustainability": sustainability,
                        "necessity_level": priority,
                        "base_co2_per_unit": base_co2
                    }
                }
                
                if self.add_emission_entry(username, entry_data):
                    st.success(f"Activity entry added! CO₂: {total_co2:.2f} kg")
                    st.rerun()
                else:
                    st.error("Failed to add entry. Please try again.")
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
            else:
                start_date = date.today()
        
        with col3:
            if data:
                end_date = st.date_input("To Date:", value=max_date, min_value=min_date, max_value=max_date)
            else:
                end_date = date.today()
        
        # Filter data
        filtered_data = sorted_data
        if selected_category != "All":
            filtered_data = [entry for entry in filtered_data if entry['category'] == selected_category]
        
        # Apply date filter
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
                    confirm_key = f"confirm_delete_{entry['id']}"
                    if confirm_key not in st.session_state:
                        st.session_state[confirm_key] = False
                    
                    if not st.session_state[confirm_key]:
                        st.session_state[confirm_key] = True
                        st.warning(f"⚠️ Are you sure you want to delete: **{entry['activity']}**?")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button("✅ Yes, Delete", key=f"yes_{entry['id']}"):
                                if db_manager.delete_co2_entry(entry['id'], username):
                                    st.success("Entry deleted!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete entry.")
                        with col_no:
                            if st.button("❌ Cancel", key=f"no_{entry['id']}"):
                                st.session_state[confirm_key] = False
                                st.rerun()
        
        if not filtered_data:
            st.info("No entries match the selected filters.")
