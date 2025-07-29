import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from database import db_manager
import random

class FunRewardSystem:
    def __init__(self):
        # Simplified achievements with fun emojis
        self.achievements = {
            "first_entry": {"name": "🌱 First Steps", "points": 50, "icon": "🌱"},
            "week_tracker": {"name": "🔥 Week Streak", "points": 100, "icon": "🔥"},
            "low_carbon": {"name": "🍃 Eco Hero", "points": 75, "icon": "🍃"},
            "transport_hero": {"name": "🚲 Green Rider", "points": 80, "icon": "🚲"},
            "plant_power": {"name": "🌿 Plant Power", "points": 90, "icon": "🌿"},
            "energy_star": {"name": "⚡ Energy Star", "points": 85, "icon": "⚡"},
            "data_master": {"name": "📊 Tracker Pro", "points": 150, "icon": "📊"},
        }
        
        # Fun levels with emojis
        self.levels = [
            {"name": "🌱 Sprout", "threshold": 0, "color": "#4CAF50"},
            {"name": "🌿 Seedling", "threshold": 100, "color": "#66BB6A"},
            {"name": "🌳 Tree", "threshold": 300, "color": "#388E3C"},
            {"name": "🌍 Guardian", "threshold": 600, "color": "#2E7D32"},
            {"name": "⭐ Eco Star", "threshold": 1000, "color": "#FFD700"},
            {"name": "🏆 Champion", "threshold": 1500, "color": "#FF9800"},
            {"name": "👑 Legend", "threshold": 2500, "color": "#E91E63"},
        ]

    def show_rewards_dashboard(self, username):
        """Fun and visual rewards dashboard"""
        # Header with fun gradient
        st.markdown("""
        <div style='background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4); 
                    padding: 30px; border-radius: 20px; margin-bottom: 30px; text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h1 style='color: white; margin: 0; font-size: 3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🎉 Your Eco Journey!</h1>
            <p style='color: white; margin: 10px 0 0 0; font-size: 1.3em; opacity: 0.9;'>Level up by protecting our planet!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get user data
        rewards_data = db_manager.get_user_rewards(username)
        if not rewards_data:
            rewards_data = {'total_points': 0, 'achievements': []}
            db_manager.update_user_rewards(username, rewards_data)
        
        # Update achievements
        self.check_new_achievements(username, rewards_data)
        
        # Show level and progress
        self.show_level_card(rewards_data)
        
        # Show achievements grid
        self.show_achievement_grid(rewards_data)
        
        # Show weekly stats
        self.show_weekly_stats(username)
        
        # Show fun tips
        self.show_fun_tips()

    def show_level_card(self, rewards_data):
        """Big colorful level display"""
        points = rewards_data.get('total_points', 0)
        current_level = self.get_current_level(points)
        level_info = self.levels[current_level]
        
        # Calculate progress to next level
        if current_level < len(self.levels) - 1:
            next_level = self.levels[current_level + 1]
            progress = (points - level_info['threshold']) / (next_level['threshold'] - level_info['threshold'])
            points_needed = next_level['threshold'] - points
        else:
            progress = 1.0
            points_needed = 0
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {level_info['color']}, {level_info['color']}88); 
                        color: white; padding: 40px; border-radius: 25px; text-align: center; 
                        box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin: 20px 0;
                        transform: scale(1.02); transition: all 0.3s ease;'>
                <div style='font-size: 5em; margin-bottom: 15px;'>{level_info['name'].split()[0]}</div>
                <h1 style='margin: 0; font-size: 2.5em;'>{level_info['name']}</h1>
                <h2 style='margin: 10px 0; font-size: 3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{points} Points</h2>
                
                {'<p style="font-size: 1.2em; margin: 15px 0;">🎯 ' + str(points_needed) + ' points to next level!</p>' if points_needed > 0 else '<p style="font-size: 1.2em; margin: 15px 0;">🌟 MAX LEVEL! 🌟</p>'}
            </div>
            """, unsafe_allow_html=True)
            
            if points_needed > 0:
                st.progress(progress)

    def show_achievement_grid(self, rewards_data):
        """Colorful achievement badges"""
        st.markdown("## 🏅 Achievement Collection")
        
        earned = set(rewards_data.get('achievements', []))
        
        cols = st.columns(4)
        for i, (ach_id, ach) in enumerate(self.achievements.items()):
            with cols[i % 4]:
                is_earned = ach_id in earned
                
                if is_earned:
                    # Shiny earned badge
                    st.markdown(f"""
                    <div style='background: linear-gradient(45deg, #FFD700, #FFA500, #FF6B6B); 
                                padding: 20px; border-radius: 20px; text-align: center; margin: 10px 0;
                                box-shadow: 0 8px 25px rgba(255,215,0,0.4); 
                                border: 3px solid #FFD700; animation: glow 2s ease-in-out infinite alternate;'>
                        <div style='font-size: 4em; margin: 10px 0;'>{ach['icon']}</div>
                        <h4 style='margin: 10px 0; color: #8B4513; font-weight: bold;'>{ach['name']}</h4>
                        <div style='background: rgba(255,255,255,0.9); padding: 8px 15px; border-radius: 20px; margin: 10px 0;'>
                            <strong style='color: #8B4513;'>✨ {ach['points']} pts</strong>
                        </div>
                    </div>
                    <style>
                    @keyframes glow {{
                        from {{ box-shadow: 0 8px 25px rgba(255,215,0,0.4); }}
                        to {{ box-shadow: 0 8px 35px rgba(255,215,0,0.8); }}
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    # Locked badge
                    st.markdown(f"""
                    <div style='background: #f0f0f0; padding: 20px; border-radius: 20px; text-align: center; 
                                margin: 10px 0; border: 2px dashed #ccc; opacity: 0.6;'>
                        <div style='font-size: 4em; margin: 10px 0; filter: grayscale(100%);'>{ach['icon']}</div>
                        <h4 style='margin: 10px 0; color: #666;'>{ach['name']}</h4>
                        <div style='background: #e0e0e0; padding: 8px 15px; border-radius: 20px; margin: 10px 0;'>
                            <strong style='color: #666;'>🔒 {ach['points']} pts</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    def show_weekly_stats(self, username):
        """Fun weekly progress with emojis"""
        st.markdown("## 📊 This Week's Impact")
        
        co2_data = db_manager.get_user_co2_entries(username)
        if not co2_data:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                        padding: 30px; border-radius: 20px; text-align: center;'>
                <div style='font-size: 5em; margin-bottom: 15px;'>🌱</div>
                <h3>Ready to start your eco journey?</h3>
                <p>Track your first activity to see your weekly progress!</p>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Calculate this week's CO2
        df = pd.DataFrame(co2_data)
        df['date'] = pd.to_datetime(df['date'])
        this_week = df[df['date'] >= datetime.now() - timedelta(days=7)]
        week_total = this_week['co2_amount'].sum() if len(this_week) > 0 else 0
        
        # Fun visual based on performance
        if week_total < 30:
            emoji = "🌟"
            color = "#4CAF50"
            message = "Amazing week!"
            grade = "A+"
        elif week_total < 60:
            emoji = "🌱"
            color = "#8BC34A"
            message = "Great job!"
            grade = "A"
        elif week_total < 100:
            emoji = "👍"
            color = "#FFC107"
            message = "Good progress!"
            grade = "B"
        else:
            emoji = "💪"
            color = "#FF9800"
            message = "Keep improving!"
            grade = "C"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}, {color}cc); color: white; 
                        padding: 25px; border-radius: 20px; text-align: center;'>
                <div style='font-size: 4em; margin-bottom: 10px;'>{emoji}</div>
                <h3>Week Grade</h3>
                <h1 style='margin: 10px 0; font-size: 3em;'>{grade}</h1>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                        padding: 25px; border-radius: 20px; text-align: center;'>
                <div style='font-size: 4em; margin-bottom: 10px;'>🌍</div>
                <h3>CO₂ This Week</h3>
                <h1 style='margin: 10px 0; font-size: 2.5em;'>{week_total:.1f} kg</h1>
                <p>Your carbon footprint</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            entries_this_week = len(this_week)
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb, #f5576c); color: white; 
                        padding: 25px; border-radius: 20px; text-align: center;'>
                <div style='font-size: 4em; margin-bottom: 10px;'>📝</div>
                <h3>Entries Logged</h3>
                <h1 style='margin: 10px 0; font-size: 3em;'>{entries_this_week}</h1>
                <p>Activities tracked</p>
            </div>
            """, unsafe_allow_html=True)

    def show_fun_tips(self):
        """Random fun eco tips"""
        tips = [
            {"emoji": "🚲", "text": "Bike rides = zero emissions + great exercise!"},
            {"emoji": "🌱", "text": "Plant-based meals can cut food emissions by 50%!"},
            {"emoji": "💡", "text": "LED bulbs use 75% less energy than old bulbs!"},
            {"emoji": "🚿", "text": "Shorter showers save water and energy!"},
            {"emoji": "♻️", "text": "Recycling one aluminum can saves enough energy to power a TV for 3 hours!"},
            {"emoji": "🌳", "text": "One tree absorbs 22kg of CO₂ per year!"},
            {"emoji": "🚇", "text": "Public transport can reduce your carbon footprint by 45%!"},
            {"emoji": "🔌", "text": "Unplugging devices saves energy even when they're off!"}
        ]
        
        tip = random.choice(tips)
        
        st.markdown("## 💡 Eco Tip of the Day")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #a8edea, #fed6e3); 
                    padding: 25px; border-radius: 20px; text-align: center;
                    border-left: 5px solid #4CAF50;'>
            <div style='font-size: 3em; margin-bottom: 15px;'>{tip['emoji']}</div>
            <h3 style='color: #2E7D32; margin: 0;'>{tip['text']}</h3>
        </div>
        """, unsafe_allow_html=True)

    def get_current_level(self, points):
        """Get current level based on points"""
        for i in range(len(self.levels) - 1, -1, -1):
            if points >= self.levels[i]['threshold']:
                return i
        return 0

    def check_new_achievements(self, username, rewards_data):
        """Check for new achievements and show celebrations"""
        co2_data = db_manager.get_user_co2_entries(username)
        if not co2_data:
            return
        
        current_achievements = set(rewards_data.get('achievements', []))
        new_achievements = []
        
        # Check achievements
        if len(co2_data) >= 1 and 'first_entry' not in current_achievements:
            new_achievements.append('first_entry')
        
        if len(co2_data) >= 7 and 'week_tracker' not in current_achievements:
            new_achievements.append('week_tracker')
        
        if len(co2_data) >= 20 and 'data_master' not in current_achievements:
            new_achievements.append('data_master')
        
        # Update if new achievements
        if new_achievements:
            all_achievements = list(current_achievements) + new_achievements
            new_points = sum(self.achievements[ach]['points'] for ach in new_achievements)
            total_points = rewards_data.get('total_points', 0) + new_points
            
            updated_rewards = {
                'total_points': total_points,
                'achievements': all_achievements,
            }
            
            db_manager.update_user_rewards(username, updated_rewards)
            
            # Celebration!
            for ach_id in new_achievements:
                ach = self.achievements[ach_id]
                st.balloons()
                st.success(f"🎉 **NEW ACHIEVEMENT!** {ach['icon']} {ach['name']} (+{ach['points']} points)")

# Global instance
fun_rewards = FunRewardSystem()

def show_rewards_dashboard(username):
    """Show the fun rewards dashboard"""
    fun_rewards.show_rewards_dashboard(username)