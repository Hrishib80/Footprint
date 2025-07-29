import streamlit as st
from datetime import datetime, timedelta
from co2_tracker import CO2Tracker
from database import db_manager

class RewardSystem:
    def __init__(self):
        self.co2_tracker = CO2Tracker()
        
    def load_user_rewards(self, username):
        """Load rewards data for a specific user from database"""
        return db_manager.get_user_rewards(username)
    
    def save_user_rewards(self, username, rewards_data):
        """Save rewards data for a specific user to database"""
        return db_manager.save_user_rewards(username, rewards_data)
    
    def calculate_level(self, points):
        """Calculate user level based on points"""
        if points < 100:
            return 1
        elif points < 300:
            return 2
        elif points < 600:
            return 3
        elif points < 1000:
            return 4
        elif points < 1500:
            return 5
        else:
            return min(10, 5 + (points - 1500) // 500)
    
    def check_achievements(self, username):
        """Check and award new achievements"""
        co2_data = self.co2_tracker.load_user_data(username)
        rewards_data = self.load_user_rewards(username)
        
        new_achievements = []
        total_entries = len(co2_data)
        
        if not co2_data:
            return rewards_data, new_achievements
        
        # Calculate total emissions and weekly trends
        total_emissions = sum(entry['co2_amount'] for entry in co2_data)
        
        # Sort data by date
        sorted_data = sorted(co2_data, key=lambda x: x['date'])
        
        # Achievement: First Entry
        if total_entries >= 1 and "first_entry" not in rewards_data.get("achievements", []):
            new_achievements.append({
                "id": "first_entry", 
                "name": "🌱 Getting Started", 
                "description": "Added your first CO₂ entry",
                "points": 50
            })
        
        # Achievement: Consistent Tracker
        if total_entries >= 7 and "consistent_tracker" not in rewards_data.get("achievements", []):
            new_achievements.append({
                "id": "consistent_tracker", 
                "name": "📊 Consistent Tracker", 
                "description": "Logged 7 CO₂ entries",
                "points": 100
            })
        
        # Achievement: Eco Warrior
        if total_entries >= 30 and "eco_warrior" not in rewards_data.get("achievements", []):
            new_achievements.append({
                "id": "eco_warrior", 
                "name": "🌍 Eco Warrior", 
                "description": "Logged 30 CO₂ entries",
                "points": 200
            })
        
        # Achievement: Low Carbon Day
        low_carbon_days = [entry for entry in co2_data if entry['co2_amount'] < 5.0]
        if len(low_carbon_days) >= 5 and "low_carbon" not in rewards_data.get("achievements", []):
            new_achievements.append({
                "id": "low_carbon", 
                "name": "🍃 Low Carbon Champion", 
                "description": "Had 5 days with less than 5kg CO₂",
                "points": 150
            })
        
        # Achievement: Category Master
        categories_used = set(entry['category'] for entry in co2_data)
        if len(categories_used) >= 4 and "category_master" not in rewards_data.get("achievements", []):
            new_achievements.append({
                "id": "category_master", 
                "name": "🏆 Category Master", 
                "description": "Tracked emissions in 4+ categories",
                "points": 120
            })
        
        # Update rewards data
        if "achievements" not in rewards_data:
            rewards_data["achievements"] = []
        
        for achievement in new_achievements:
            rewards_data["achievements"].append(achievement["id"])
            rewards_data["total_points"] = rewards_data.get("total_points", 0) + achievement["points"]
        
        rewards_data["level"] = self.calculate_level(rewards_data.get("total_points", 0))
        
        return rewards_data, new_achievements
    
    def check_weekly_improvement(self, username):
        """Check for weekly CO₂ reduction improvements"""
        co2_data = self.co2_tracker.load_user_data(username)
        rewards_data = self.load_user_rewards(username)
        
        if len(co2_data) < 14:  # Need at least 2 weeks of data
            return rewards_data, None
        
        # Group data by weeks
        from collections import defaultdict
        weekly_emissions = defaultdict(float)
        
        for entry in co2_data:
            entry_date = datetime.fromisoformat(entry['date'])
            week_start = entry_date - timedelta(days=entry_date.weekday())
            week_key = week_start.strftime('%Y-%W')
            weekly_emissions[week_key] += entry['co2_amount']
        
        # Get last two weeks
        weeks = sorted(weekly_emissions.keys())
        if len(weeks) >= 2:
            current_week = weekly_emissions[weeks[-1]]
            previous_week = weekly_emissions[weeks[-2]]
            
            if current_week < previous_week:
                reduction_percent = ((previous_week - current_week) / previous_week) * 100
                
                # Award points for improvement
                improvement_points = int(reduction_percent * 2)  # 2 points per percent improvement
                rewards_data["total_points"] = rewards_data.get("total_points", 0) + improvement_points
                
                # Check if it's their best week
                best_reduction = rewards_data.get("best_week", {}).get("reduction", 0)
                if reduction_percent > best_reduction:
                    rewards_data["best_week"] = {
                        "week": weeks[-1],
                        "reduction": reduction_percent
                    }
                
                return rewards_data, {
                    "type": "improvement",
                    "reduction_percent": reduction_percent,
                    "points_earned": improvement_points
                }
        
        return rewards_data, None
    
    def show_rewards_dashboard(self, username):
        """Display the rewards dashboard"""
        st.title("🏆 Rewards & Achievements")
        
        # Update achievements first
        rewards_data, new_achievements = self.check_achievements(username)
        rewards_data, improvement = self.check_weekly_improvement(username)
        
        # Save updated rewards
        self.save_user_rewards(username, rewards_data)
        
        # Show new achievements if any
        if new_achievements:
            for achievement in new_achievements:
                st.success(f"🎉 New Achievement Unlocked: {achievement['name']} (+{achievement['points']} points)")
        
        if improvement:
            st.success(f"🌟 Weekly Improvement: {improvement['reduction_percent']:.1f}% reduction (+{improvement['points_earned']} points)")
        
        # User stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Level", f"Level {rewards_data.get('level', 1)}")
        
        with col2:
            st.metric("Total Points", f"{rewards_data.get('total_points', 0):,}")
        
        with col3:
            st.metric("Achievements", len(rewards_data.get('achievements', [])))
        
        with col4:
            next_level_points = (rewards_data.get('level', 1) * 200) + 100
            current_points = rewards_data.get('total_points', 0)
            points_needed = max(0, next_level_points - current_points)
            st.metric("Points to Next Level", points_needed)
        
        # Progress bar to next level
        if points_needed > 0:
            progress = current_points / next_level_points
            st.progress(progress, text=f"Progress to Level {rewards_data.get('level', 1) + 1}")
        
        # Achievements section
        st.subheader("🏅 Your Achievements")
        
        all_possible_achievements = [
            {"id": "first_entry", "name": "🌱 Getting Started", "description": "Added your first CO₂ entry"},
            {"id": "consistent_tracker", "name": "📊 Consistent Tracker", "description": "Logged 7 CO₂ entries"},
            {"id": "eco_warrior", "name": "🌍 Eco Warrior", "description": "Logged 30 CO₂ entries"},
            {"id": "low_carbon", "name": "🍃 Low Carbon Champion", "description": "Had 5 days with less than 5kg CO₂"},
            {"id": "category_master", "name": "🏆 Category Master", "description": "Tracked emissions in 4+ categories"},
        ]
        
        user_achievements = rewards_data.get('achievements', [])
        
        achievement_cols = st.columns(3)
        for i, achievement in enumerate(all_possible_achievements):
            with achievement_cols[i % 3]:
                if achievement['id'] in user_achievements:
                    st.success(f"**{achievement['name']}**\n\n{achievement['description']}")
                else:
                    st.info(f"**{achievement['name']}** (Locked)\n\n{achievement['description']}")
        
        # Best performance
        st.subheader("📈 Your Best Performance")
        
        best_week = rewards_data.get('best_week', {})
        if best_week.get('reduction', 0) > 0:
            st.success(f"🌟 **Best Weekly Reduction:** {best_week['reduction']:.1f}% (Week {best_week['week']})")
        else:
            st.info("💡 Track for at least 2 weeks to see your improvement stats!")
        
        # Tips for earning more points
        st.subheader("💡 How to Earn More Points")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("""
            **Daily Actions:**
            - Log daily activities: +10 points
            - Keep CO₂ under 5kg/day: +20 points
            - Use public transport: +15 points
            - Choose vegetarian meals: +10 points
            """)
        
        with tips_col2:
            st.markdown("""
            **Weekly Goals:**
            - Reduce emissions vs last week: +2 points per %
            - Track all 7 days: +50 bonus points
            - Try 3+ transport types: +30 points
            - Mix of all categories: +25 points
            """)