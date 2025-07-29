import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from co2_tracker import CO2Tracker

class Dashboard:
    def __init__(self):
        self.co2_tracker = CO2Tracker()
    
    def show_dashboard(self, username):
        """Display the main dashboard"""
        # Modern header with green gradient effect
        st.markdown("""
        <div style='background: linear-gradient(90deg, #00C851, #00A040); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0; text-align: center;'>📊 CO₂ Emissions Dashboard</h1>
            <p style='color: white; margin: 5px 0 0 0; text-align: center; opacity: 0.9;'>Personal carbon footprint overview for {}</p>
        </div>
        """.format(username), unsafe_allow_html=True)
        
        # Load user data
        user_data = self.co2_tracker.load_user_data(username)
        
        if not user_data:
            st.info("🌱 Welcome to your CO₂ tracker! Start by adding your first emission entry in the 'Track CO₂' section.")
            self.show_getting_started()
            return
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(user_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Key metrics
        self.show_key_metrics(df)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.show_emissions_over_time(df)
            self.show_category_breakdown(df)
        
        with col2:
            self.show_monthly_comparison(df)
            self.show_recent_activities(df)
    
    def show_key_metrics(self, df):
        """Display key metrics cards"""
        st.markdown("### 📈 Key Metrics")
        
        # Modern metric cards with green styling
        col1, col2, col3, col4 = st.columns(4)
        
        # Total emissions with color coding
        total_emissions = df['co2_amount'].sum()
        with col1:
            # Determine color based on total emissions
            if total_emissions < 50:
                delta_color = "#00C851"  # Green for low emissions
            elif total_emissions < 150:
                delta_color = "#FF8C00"  # Orange for medium
            else:
                delta_color = "#DC3545"  # Red for high
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E8, #F0FFF0); padding: 15px; border-radius: 8px; border-left: 4px solid {delta_color};'>
                <h4 style='margin: 0; color: #1B5E20;'>Total CO₂ Emissions</h4>
                <h2 style='margin: 5px 0 0 0; color: {delta_color};'>{total_emissions:.2f} kg</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Average daily emissions
        if len(df) > 0:
            days_tracked = (df['date'].max() - df['date'].min()).days + 1
            avg_daily = total_emissions / max(days_tracked, 1)
        else:
            avg_daily = 0
        
        with col2:
            avg_color = "#00C851" if avg_daily < 5 else "#FF8C00" if avg_daily < 10 else "#DC3545"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E8, #F0FFF0); padding: 15px; border-radius: 8px; border-left: 4px solid {avg_color};'>
                <h4 style='margin: 0; color: #1B5E20;'>Daily Average</h4>
                <h2 style='margin: 5px 0 0 0; color: {avg_color};'>{avg_daily:.2f} kg/day</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Total entries
        with col3:
            entry_color = "#00C851" if len(df) > 20 else "#FF8C00" if len(df) > 5 else "#1B5E20"
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E8, #F0FFF0); padding: 15px; border-radius: 8px; border-left: 4px solid {entry_color};'>
                <h4 style='margin: 0; color: #1B5E20;'>Total Entries</h4>
                <h2 style='margin: 5px 0 0 0; color: {entry_color};'>{len(df)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Most common category
        if len(df) > 0:
            most_common = df['category'].mode().iloc[0] if not df['category'].mode().empty else "N/A"
        else:
            most_common = "N/A"
        
        with col4:
            category_icons = {
                "Transportation": "🚗", "Energy": "⚡", "Food": "🍽️", 
                "Shopping": "🛒", "Home": "🏠", "Work": "🏢", "Other": "📦"
            }
            icon = category_icons.get(most_common, "📊")
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #E8F5E8, #F0FFF0); padding: 15px; border-radius: 8px; border-left: 4px solid #00C851;'>
                <h4 style='margin: 0; color: #1B5E20;'>Top Category</h4>
                <h2 style='margin: 5px 0 0 0; color: #00C851;'>{icon} {most_common}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    def show_emissions_over_time(self, df):
        """Show emissions trend over time"""
        st.subheader("📅 Emissions Over Time")
        
        # Group by date and sum emissions
        daily_emissions = df.groupby('date')['co2_amount'].sum().reset_index()
        
        fig = px.line(
            daily_emissions,
            x='date',
            y='co2_amount',
            title='Daily CO₂ Emissions',
            labels={'co2_amount': 'CO₂ Emissions (kg)', 'date': 'Date'}
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="CO₂ Emissions (kg)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_category_breakdown(self, df):
        """Show emissions by category"""
        st.subheader("🏷️ Emissions by Category")
        
        category_emissions = df.groupby('category')['co2_amount'].sum().reset_index()
        
        fig = px.pie(
            category_emissions,
            values='co2_amount',
            names='category',
            title='CO₂ Emissions by Category'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_monthly_comparison(self, df):
        """Show monthly emissions comparison"""
        st.subheader("📆 Monthly Comparison")
        
        # Add month-year column
        df['month_year'] = df['date'].dt.to_period('M').astype(str)
        monthly_emissions = df.groupby('month_year')['co2_amount'].sum().reset_index()
        
        fig = px.bar(
            monthly_emissions,
            x='month_year',
            y='co2_amount',
            title='Monthly CO₂ Emissions',
            labels={'co2_amount': 'CO₂ Emissions (kg)', 'month_year': 'Month'}
        )
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="CO₂ Emissions (kg)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_recent_activities(self, df):
        """Show recent activities"""
        st.subheader("🕒 Recent Activities")
        
        # Get last 5 entries
        recent_df = df.tail(5).sort_values('date', ascending=False)
        
        if len(recent_df) > 0:
            for _, row in recent_df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{row['activity']}**")
                        st.caption(f"{row['category']}")
                    with col2:
                        st.write(f"{row['co2_amount']:.2f} kg")
                    with col3:
                        st.write(row['date'].strftime('%m/%d/%Y'))
                    st.divider()
        else:
            st.info("No recent activities found.")
    
    def show_getting_started(self):
        """Show getting started information"""
        st.subheader("🚀 Getting Started")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Track Your Carbon Footprint:**
            - 🚗 Transportation (car, bus, train, flight)
            - ⚡ Energy consumption (electricity, heating)
            - 🍽️ Food choices (meals, groceries)
            - 🛍️ Shopping and consumption
            - 🏠 Home activities
            """)
        
        with col2:
            st.markdown("""
            **Why Track CO₂?**
            - 🌍 Understand your environmental impact
            - 📊 Identify areas for improvement
            - 🎯 Set and achieve reduction goals
            - 💚 Make informed eco-friendly choices
            """)
        
        st.info("💡 Tip: Start by tracking your daily commute and energy usage. These are usually the biggest contributors to personal carbon footprints!")
