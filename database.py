import os
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
# Add SSL configuration for PostgreSQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# CO2 Entry model
class CO2Entry(Base):
    __tablename__ = "co2_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)  # ISO format date string
    activity = Column(String, nullable=False)
    category = Column(String, nullable=False)
    co2_amount = Column(Float, nullable=False)
    quantity = Column(Float)
    distance = Column(Float)
    duration = Column(Float)
    participants = Column(Integer)
    location = Column(String)
    weather = Column(String)
    purpose = Column(String)
    efficiency = Column(String)
    notes = Column(Text)
    entry_type = Column(String, default="quick")
    attributes = Column(JSON)  # Store additional attributes as JSON
    timestamp = Column(DateTime, default=datetime.utcnow)

# Rewards model
class UserRewards(Base):
    __tablename__ = "user_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    badges = Column(JSON, default=list)  # List of badge IDs
    achievements = Column(JSON, default=list)  # List of achievement IDs
    streak_days = Column(Integer, default=0)
    last_entry_date = Column(String)  # ISO format date string
    monthly_goals = Column(JSON, default=dict)  # Monthly goal tracking
    best_week = Column(JSON, default=dict)  # Best week performance
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.create_tables()
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Close a database session"""
        session.close()
    
    # User management
    def create_user(self, username, password_hash):
        """Create a new user"""
        session = self.get_session()
        try:
            user = User(username=username, password_hash=password_hash)
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            self.close_session(session)
    
    def get_user(self, username):
        """Get user by username"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            return user
        finally:
            self.close_session(session)
    
    def get_all_users(self):
        """Get all users as dictionary (for compatibility with YAML format)"""
        session = self.get_session()
        try:
            users = session.query(User).all()
            user_dict = {}
            for user in users:
                user_dict[user.username] = {
                    'password': user.password_hash,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
            return user_dict
        finally:
            self.close_session(session)
    
    # CO2 Entry management
    def add_co2_entry(self, username, entry_data):
        """Add a CO2 entry for a user"""
        session = self.get_session()
        try:
            # Convert entry_data to database model
            entry = CO2Entry(
                username=username,
                date=entry_data.get('date'),
                activity=entry_data.get('activity'),
                category=entry_data.get('category'),
                co2_amount=entry_data.get('co2_amount'),
                quantity=entry_data.get('quantity'),
                distance=entry_data.get('distance'),
                duration=entry_data.get('duration'),
                participants=entry_data.get('participants'),
                location=entry_data.get('location'),
                weather=entry_data.get('weather'),
                purpose=entry_data.get('purpose'),
                efficiency=entry_data.get('efficiency'),
                notes=entry_data.get('notes'),
                entry_type=entry_data.get('entry_type', 'quick'),
                attributes=entry_data.get('attributes'),
                timestamp=datetime.fromisoformat(entry_data.get('timestamp')) if entry_data.get('timestamp') else datetime.utcnow()
            )
            session.add(entry)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            self.close_session(session)
    
    def get_user_co2_entries(self, username):
        """Get all CO2 entries for a user"""
        session = self.get_session()
        try:
            entries = session.query(CO2Entry).filter(CO2Entry.username == username).all()
            entry_list = []
            for entry in entries:
                entry_dict = {
                    'id': entry.id,
                    'date': entry.date,
                    'activity': entry.activity,
                    'category': entry.category,
                    'co2_amount': entry.co2_amount,
                    'quantity': entry.quantity,
                    'distance': entry.distance,
                    'duration': entry.duration,
                    'participants': entry.participants,
                    'location': entry.location,
                    'weather': entry.weather,
                    'purpose': entry.purpose,
                    'efficiency': entry.efficiency,
                    'notes': entry.notes,
                    'entry_type': entry.entry_type,
                    'attributes': entry.attributes,
                    'timestamp': entry.timestamp.isoformat() if entry.timestamp else None
                }
                # Filter out None values for cleaner data
                entry_dict = {k: v for k, v in entry_dict.items() if v is not None}
                entry_list.append(entry_dict)
            return entry_list
        finally:
            self.close_session(session)
    
    def delete_co2_entry(self, entry_id, username):
        """Delete a CO2 entry by ID and username"""
        session = self.get_session()
        try:
            entry = session.query(CO2Entry).filter(
                CO2Entry.id == entry_id,
                CO2Entry.username == username
            ).first()
            if entry:
                session.delete(entry)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            self.close_session(session)
    
    def clear_user_co2_entries(self, username):
        """Clear all CO2 entries for a user"""
        session = self.get_session()
        try:
            session.query(CO2Entry).filter(CO2Entry.username == username).delete()
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            self.close_session(session)
    
    # Rewards management
    def get_user_rewards(self, username):
        """Get rewards data for a user"""
        session = self.get_session()
        try:
            rewards = session.query(UserRewards).filter(UserRewards.username == username).first()
            if rewards:
                return {
                    'total_points': rewards.total_points,
                    'level': rewards.level,
                    'badges': rewards.badges or [],
                    'achievements': rewards.achievements or [],
                    'streak_days': rewards.streak_days,
                    'last_entry_date': rewards.last_entry_date,
                    'monthly_goals': rewards.monthly_goals or {},
                    'best_week': rewards.best_week or {}
                }
            else:
                # Return default rewards structure
                return {
                    "total_points": 0,
                    "level": 1,
                    "badges": [],
                    "achievements": [],
                    "streak_days": 0,
                    "last_entry_date": None,
                    "monthly_goals": {},
                    "best_week": {"week": None, "reduction": 0}
                }
        finally:
            self.close_session(session)
    
    def save_user_rewards(self, username, rewards_data):
        """Save rewards data for a user"""
        session = self.get_session()
        try:
            rewards = session.query(UserRewards).filter(UserRewards.username == username).first()
            if rewards:
                # Update existing rewards
                rewards.total_points = rewards_data.get('total_points', 0)
                rewards.level = rewards_data.get('level', 1)
                rewards.badges = rewards_data.get('badges', [])
                rewards.achievements = rewards_data.get('achievements', [])
                rewards.streak_days = rewards_data.get('streak_days', 0)
                rewards.last_entry_date = rewards_data.get('last_entry_date')
                rewards.monthly_goals = rewards_data.get('monthly_goals', {})
                rewards.best_week = rewards_data.get('best_week', {})
                rewards.updated_at = datetime.utcnow()
            else:
                # Create new rewards record
                rewards = UserRewards(
                    username=username,
                    total_points=rewards_data.get('total_points', 0),
                    level=rewards_data.get('level', 1),
                    badges=rewards_data.get('badges', []),
                    achievements=rewards_data.get('achievements', []),
                    streak_days=rewards_data.get('streak_days', 0),
                    last_entry_date=rewards_data.get('last_entry_date'),
                    monthly_goals=rewards_data.get('monthly_goals', {}),
                    best_week=rewards_data.get('best_week', {})
                )
                session.add(rewards)
            
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            self.close_session(session)

# Global database manager instance
db_manager = DatabaseManager()