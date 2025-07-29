# CO₂ Tracker Application

## Overview

This is a Streamlit-based CO₂ emissions tracking application that allows users to register, login, and monitor their personal carbon footprint. The application provides authentication, data tracking, and dashboard visualization capabilities for individual users to log and analyze their CO₂ emissions from various activities.

## User Preferences

Preferred communication style: Simple, everyday language.
UI Design: Greenish color theme with modern dashboard styling.
Features: Enhanced forms with detailed attributes, reward system for carbon footprint improvements.

## System Architecture

The application follows a modular, component-based architecture built on Streamlit's web framework. It uses a file-based data storage approach with YAML serialization for both user authentication and emission data persistence. The architecture separates concerns into distinct modules: authentication management, data tracking, and dashboard visualization.

### Core Design Principles
- **Stateful session management**: Leverages Streamlit's session state for user authentication and navigation
- **File-based persistence**: Uses YAML files for data storage, avoiding database complexity
- **Modular component structure**: Separates authentication, tracking, and visualization logic
- **User-centric data isolation**: Each user's data is stored in separate files

## Key Components

### 1. Authentication System (`auth.py`)
- **Purpose**: Handles user registration and login functionality with modern tabbed interface
- **Security**: Uses PBKDF2-SHA256 password hashing for secure credential storage
- **Data Storage**: Stores user credentials in `users.yaml` file
- **Validation**: Implements username (min 3 chars) and password (min 6 chars) validation
- **UI**: Clean tabs for login/signup with enhanced form validation

### 2. CO₂ Tracking Module (`co2_tracker.py`)
- **Purpose**: Manages emission data entry and storage with category-specific tracking
- **Data Structure**: Stores user emissions in PostgreSQL database with detailed attributes
- **Categories**: Separate trackers for Transportation, Diet, Electricity, and Other Activities
- **Interface**: Provides dedicated tabs for each emission category with customized inputs
- **Transportation**: Tracks vehicles, distance, passengers, fuel efficiency, traffic conditions
- **Diet**: Food tracking with preparation methods, origin, waste percentages, dietary preferences  
- **Electricity**: Energy usage with source types, appliances, efficiency ratings, renewable mix
- **Other Activities**: Shopping, work, entertainment with sustainability choices and necessity levels
- **Enhanced Attributes**: Category-specific attributes with real-time CO₂ calculations

### 3. Dashboard Component (`dashboard.py`)
- **Purpose**: Visualizes user emission data through modern charts and metrics
- **Dependencies**: Uses Plotly for interactive charts and Pandas for data manipulation
- **Features**: Color-coded metrics cards, time-series analysis, category breakdowns
- **Styling**: Green gradient headers, modern metric cards with conditional coloring
- **Data Processing**: Converts YAML data to DataFrames for analysis

### 4. Fun Reward System (`rewards_new.py`)
- **Purpose**: Gamified, visual reward system to motivate eco-friendly behavior
- **Design**: Colorful achievement badges with animations and celebratory effects
- **Features**: Level progression with emoji-based names, achievement collection grid
- **Visual Elements**: Gradient backgrounds, animated badges, progress bars, weekly impact cards
- **Achievements**: Simplified achievement system with fun icons and immediate feedback
- **Analytics**: Weekly performance grading with emoji indicators and trend analysis
- **Motivation**: Daily eco tips and motivational messages with visual appeal

### 5. Main Application (`app.py`)
- **Purpose**: Orchestrates the entire application flow and navigation
- **Session Management**: Handles authentication state and page routing
- **Configuration**: Sets up Streamlit page config with green theme
- **Navigation**: Provides sidebar-based navigation including new Rewards section
- **Theme**: Consistent green color scheme throughout the application

## Data Flow

1. **Authentication Flow**:
   - User accesses application → Authentication check
   - New users: Registration → Password hashing → Store in `users.yaml`
   - Existing users: Login verification → Session state update

2. **Data Entry Flow**:
   - Authenticated user → CO₂ Tracker interface
   - User inputs emission data → Validation → Storage in user-specific YAML file
   - Data structure: `user_data/{username}_co2_data.yaml`

3. **Visualization Flow**:
   - Dashboard access → Load user data from YAML
   - Data transformation (YAML → Pandas DataFrame)
   - Chart generation using Plotly
   - Metrics calculation and display

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework and UI components
- **Plotly**: Interactive charting and visualization library
- **Pandas**: Data manipulation and analysis

### Security & Data
- **passlib**: Password hashing (PBKDF2-SHA256 algorithm)
- **PyYAML**: YAML file parsing and serialization

### Python Standard Library
- **os**: File system operations
- **datetime**: Date and time handling

## Deployment Strategy

The application is designed for simple deployment scenarios:

### File Storage Structure
```
project_root/
├── app.py (main application)
├── auth.py (authentication module)
├── co2_tracker.py (tracking module)
├── dashboard.py (visualization module)
├── users.yaml (user credentials - created at runtime)
└── user_data/ (created at runtime)
    ├── {username}_co2_data.yaml
    └── ...
```

### Runtime Requirements
- **Data Persistence**: File-based storage requires write permissions
- **Session State**: Relies on Streamlit's built-in session management
- **Security**: Password hashing happens server-side, credentials stored locally

### Scalability Considerations
- Current architecture suitable for small to medium user bases
- File-based storage may require migration to database for larger deployments
- Single-instance deployment model (no distributed architecture)

The application prioritizes simplicity and ease of deployment over enterprise-scale features, making it ideal for personal use or small team environments.