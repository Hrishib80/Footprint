import streamlit as st
import yaml
import os
from datetime import datetime, date, timedelta
from co2_tracker import CO2Tracker
import pandas as pd

class RewardsManager:
    def __init__(self):
        self.rewards_dir = "user_data"
        self.co2_tracker = CO2Tracker()
        if not os.path.exists(self.rewards_dir):
            os.makedirs(self.rewards_dir)
    
    def get_user_rewards_file(self, username):
        """Get the rewards file path for a specific user"""
        return os.path.join(self.rewards_dir, f"{username}_rewards.yaml")
    
    def load_user_rewards(self, username):
        """Load rewards data for a specific user"""
        file_path = self.get_user_rewards_file(username)
        if not os.path.exists(file_path):
            return {
                "login_streak": 0,
                "last_login": None,
                "total_logins": 0,
                "badges": {
                    "Habit Builder": 0,    # 21 day streak
                    "Fortniter": 0,        # 14 day streak
                    "Weekly Champions": 0,  # 7 day streak
                    "Monthly Mavericks": 0  # 30 day streak
                }
            }
        
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data if data else self.get_default_rewards()
    
    def get_default_rewards(self):
        """Get default rewards structure"""
        return {
            "login_streak": 0,
            "last_login": None,
            "total_logins": 0,
            "badges": {
                "Habit Builder": 0,
                "Fortniter": 0,
                "Weekly Champions": 0,
                "Monthly Mavericks": 0
            }
        }
    
    def save_user_rewards(self, username, data):
        """Save rewards data for a specific user"""
        file_path = self.get_user_rewards_file(username)
        with open(file_path, "w") as f:
            yaml.dump(data, f)
    
    def update_daily_login(self, username):
        """Update user's daily login streak"""
        rewards_data = self.load_user_rewards(username)
        today = date.today().isoformat()
        last_login = rewards_data.get("last_login")
        
        # If first login or different day
        if not last_login or last_login != today:
            # Check if consecutive day
            if last_login:
                last_date = datetime.fromisoformat(last_login).date()
                yesterday = date.today() - timedelta(days=1)
                
                if last_date == yesterday:
                    # Consecutive login
                    rewards_data["login_streak"] += 1
                elif last_date == date.today():
                    # Same day, no update needed
                    return rewards_data
                else:
                    # Streak broken
                    rewards_data["login_streak"] = 1
            else:
                # First login
                rewards_data["login_streak"] = 1
            
            rewards_data["last_login"] = today
            rewards_data["total_logins"] += 1
            
            # Check for badge achievements
            self.check_and_award_badges(rewards_data)
            
            self.save_user_rewards(username, rewards_data)
        
        return rewards_data
    
    def check_and_award_badges(self, rewards_data):
        """Check and award badges based on current streak"""
        current_streak = rewards_data["login_streak"]
        
        # Award badges based on streak milestones
        if current_streak >= 30 and current_streak % 30 == 0:
            rewards_data["badges"]["Monthly Mavericks"] += 1
        elif current_streak >= 21 and current_streak % 21 == 0:
            rewards_data["badges"]["Habit Builder"] += 1
        elif current_streak >= 14 and current_streak % 14 == 0:
            rewards_data["badges"]["Fortniter"] += 1
        elif current_streak >= 7 and current_streak % 7 == 0:
            rewards_data["badges"]["Weekly Champions"] += 1
    
    def get_leaderboard(self):
        """Generate leaderboard based on total CO2 emissions"""
        leaderboard = []
        
        # Get all users from user_data directory
        if not os.path.exists(self.rewards_dir):
            return []
        
        for filename in os.listdir(self.rewards_dir):
            if filename.endswith("_co2_data.yaml"):
                username = filename.replace("_co2_data.yaml", "")
                user_data = self.co2_tracker.load_user_data(username)
                
                if user_data:
                    total_emissions = sum(entry.get('co2_amount', 0) for entry in user_data)/len(user_data)
                    leaderboard.append({
                        "username": username,
                        "total_emissions": total_emissions,
                        "entries_count": len(user_data)
                    })
        
        # Sort by total emissions (ascending - lower is better)
        leaderboard.sort(key=lambda x: x['total_emissions'])
        
        # Add rankings
        for i, user in enumerate(leaderboard):
            user["rank"] = i + 1
            if i == 0:
                user["medal"] = "🥇 Gold"
            elif i == 1:
                user["medal"] = "🥈 Silver"
            elif i == 2:
                user["medal"] = "🥉 Bronze"
            else:
                user["medal"] = ""
        
        return leaderboard
    
    def show_rewards_page(self, username):
        """Display the rewards and leaderboard page"""
        st.title("🏆 Rewards & Achievements")
        
        # Update daily login
        rewards_data = self.update_daily_login(username)
        
        # Display user's achievements
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Your Streak")
            st.metric("Current Login Streak", f"{rewards_data['login_streak']} days")
            st.metric("Total Logins", rewards_data['total_logins'])
            
            if rewards_data['last_login']:
                st.write(f"Last Login: {rewards_data['last_login']}")
        
        with col2:
            st.subheader("🏅 Your Badges")
            badges = rewards_data['badges']
            
            for badge_name, count in badges.items():
                if badge_name == "Weekly Champions":
                    emoji = "🌟"
                    desc = "7-day streak"
                elif badge_name == "Fortniter":
                    emoji = "⚡"
                    desc = "14-day streak"
                elif badge_name == "Habit Builder":
                    emoji = "💪"
                    desc = "21-day streak"
                elif badge_name == "Monthly Mavericks":
                    emoji = "👑"
                    desc = "30-day streak"
                else:
                    emoji = "🏅"
                    desc = ""
                
                st.write(f"{emoji} **{badge_name}** ({desc}): {count}")
        
        st.markdown("---")
        
        # Leaderboard section
        st.subheader("🏆 Global Leaderboard")
        st.markdown("*Rankings based on average CO₂ emissions per day")
        
        leaderboard = self.get_leaderboard()
        
        if leaderboard:
            # Find current user's position
            user_position = None
            for user in leaderboard:
                if user['username'] == username:
                    user_position = user
                    break
            
            # Display top 10
            st.write("**Top 10 Eco-Warriors:**")
            for i, user in enumerate(leaderboard[:10]):
                if user['username'] == username:
                    # Highlight current user
                    st.markdown(f"**→ {user['rank']}. {user['medal']} {user['username']} - {user['total_emissions']:.2f} kg CO₂/day ({user['entries_count']} entries) ←**")
                else:
                    st.write(f"{user['rank']}. {user['medal']} {user['username']} - {user['total_emissions']:.2f} kg CO₂/day ({user['entries_count']} entries)")
            
            # Show user's position if not in top 10
            if user_position and user_position['rank'] > 10:
                st.markdown("---")
                st.write("**Your Position:**")
                st.markdown(f"**→ {user_position['rank']}. {user_position['medal']} {user_position['username']} - {user_position['total_emissions']:.2f} kg CO₂/day ({user_position['entries_count']} entries) ←**")
        else:
            st.info("No leaderboard data available yet. Start tracking CO₂ emissions to appear on the leaderboard!")
        
        # Progress towards next badge
        st.markdown("---")
        st.subheader("🎯 Next Achievement")
        current_streak = rewards_data['login_streak']
        
        if current_streak < 7:
            days_needed = 7 - current_streak
            st.progress(current_streak / 7)
            st.write(f"🌟 {days_needed} more days for Weekly Champions badge!")
        elif current_streak < 14:
            days_needed = 14 - current_streak
            st.progress(current_streak / 14)
            st.write(f"⚡ {days_needed} more days for Fortniter badge!")
        elif current_streak < 21:
            days_needed = 21 - current_streak
            st.progress(current_streak / 21)
            st.write(f"💪 {days_needed} more days for Habit Builder badge!")
        elif current_streak < 30:
            days_needed = 30 - current_streak
            st.progress(current_streak / 30)
            st.write(f"👑 {days_needed} more days for Monthly Mavericks badge!")
        else:
            st.success("🎉 You're on a amazing streak! Keep it up for more Monthly Mavericks badges!")
