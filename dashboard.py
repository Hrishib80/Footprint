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
        st.title("📊 CO₂ Emissions Dashboard")
        st.markdown(f"**Personal carbon footprint overview for {username}**")
        
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
        st.subheader("📈 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Total emissions
        total_emissions = df['co2_amount'].sum()
        with col1:
            st.metric(
                label="Total CO₂ Emissions",
                value=f"{total_emissions:.2f} kg",
                delta=None
            )
        
        # Average daily emissions
        if len(df) > 0:
            days_tracked = (df['date'].max() - df['date'].min()).days + 1
            avg_daily = total_emissions / max(days_tracked, 1)
        else:
            avg_daily = 0
        
        with col2:
            st.metric(
                label="Daily Average",
                value=f"{avg_daily:.2f} kg/day",
                delta=None
            )
        
        # Total entries
        with col3:
            st.metric(
                label="Total Entries",
                value=len(df),
                delta=None
            )
        
        # Most common category
        if len(df) > 0:
            most_common = df['category'].mode().iloc[0] if not df['category'].mode().empty else "N/A"
        else:
            most_common = "N/A"
        
        with col4:
            st.metric(
                label="Top Category",
                value=most_common,
                delta=None
            )
    
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
