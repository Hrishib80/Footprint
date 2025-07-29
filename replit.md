# CO₂ Tracker Application

## Overview

This is a Streamlit-based CO₂ emissions tracking application that allows users to register, login, and monitor their personal carbon footprint. The application provides authentication, data tracking, and dashboard visualization capabilities for individual users to log and analyze their CO₂ emissions from various activities.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**2025-07-29**: Completed migration from Replit Agent to Replit environment
- ✓ Fixed Streamlit compatibility issues (removed `st.confirm`, improved error handling)
- ✓ Created proper `.streamlit/config.toml` configuration for deployment
- ✓ Updated dependencies and resolved all LSP diagnostics
- ✓ Application successfully running on port 5000

**2025-07-29**: Added rewards and gamification features
- ✓ Created rewards.py with daily login streak tracking
- ✓ Added badge system (Weekly Champions, Fortniter, Habit Builder, Monthly Mavericks)
- ✓ Implemented global leaderboard ranking users by total CO₂ emissions
- ✓ Added personalized carbon footprint reduction suggestions to dashboard
- ✓ Integrated rewards page into main navigation

## System Architecture

The application follows a modular, component-based architecture built on Streamlit's web framework. It uses a file-based data storage approach with YAML serialization for both user authentication and emission data persistence. The architecture separates concerns into distinct modules: authentication management, data tracking, and dashboard visualization.

### Core Design Principles
- **Stateful session management**: Leverages Streamlit's session state for user authentication and navigation
- **File-based persistence**: Uses YAML files for data storage, avoiding database complexity
- **Modular component structure**: Separates authentication, tracking, and visualization logic
- **User-centric data isolation**: Each user's data is stored in separate files

## Key Components

### 1. Authentication System (`auth.py`)
- **Purpose**: Handles user registration and login functionality
- **Security**: Uses PBKDF2-SHA256 password hashing for secure credential storage
- **Data Storage**: Stores user credentials in `users.yaml` file
- **Validation**: Implements username (min 3 chars) and password (min 6 chars) validation

### 2. CO₂ Tracking Module (`co2_tracker.py`)
- **Purpose**: Manages emission data entry and storage for individual users
- **Data Structure**: Stores user emissions in separate YAML files per user
- **Features**: Supports adding, loading, and clearing emission entries
- **Interface**: Provides tabbed interface for different entry methods (Quick, Detailed, History)

### 3. Dashboard Component (`dashboard.py`)
- **Purpose**: Visualizes user emission data through charts and metrics
- **Dependencies**: Uses Plotly for interactive charts and Pandas for data manipulation
- **Features**: Key metrics display, time-series analysis, category breakdowns
- **Smart Suggestions**: Personalized reduction tips based on highest emission categories
- **Data Processing**: Converts YAML data to DataFrames for analysis

### 4. Rewards System (`rewards.py`)
- **Purpose**: Manages user engagement through gamification features
- **Login Tracking**: Records daily login streaks and awards badges
- **Badge System**: Four achievement levels (7, 14, 21, 30 day streaks)
- **Leaderboard**: Global ranking system based on total CO₂ emissions
- **User Motivation**: Progress tracking and achievement visualization

### 5. Main Application (`app.py`)
- **Purpose**: Orchestrates the entire application flow and navigation
- **Session Management**: Handles authentication state and page routing
- **Configuration**: Sets up Streamlit page config and initializes components
- **Navigation**: Provides sidebar-based navigation for authenticated users

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