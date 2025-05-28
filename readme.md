# Criclytics - Cricket Analytics Database Management System

A comprehensive database management system for cricket analytics with a web-based dashboard built using Python, MySQL, and Streamlit.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributors](#contributors)

## 🏏 Overview

Criclytics is a DBMS project designed to store, manage, and analyze cricket match data. The system provides comprehensive cricket analytics through a relational database design that captures detailed ball-by-ball information, player statistics, team performance, and match outcomes.

## ✨ Features

### Database Features
- **Comprehensive Data Model**: Stores detailed cricket match data including ball-by-ball records
- **Player Management**: Track player statistics, performance metrics, and career data
- **Team Analytics**: Team performance analysis and historical data
- **Match Details**: Complete match information including venues, toss decisions, and outcomes
- **Statistical Analysis**: Advanced queries for cricket analytics

### Web Dashboard Features
- **Team Performance Analysis**: Analyze teams with 100+ matches
- **Best Bowler Statistics**: Top 10 bowlers by wickets taken
- **Player Search**: Search functionality for players
- **Interactive Visualizations**: Charts and graphs for data visualization
- **Real-time Data**: Live database connectivity

## 🗄️ Database Schema

The database consists of the following main tables:

- **`players`**: Player information and career statistics
- **`teams`**: Team details and metadata
- **`matches`**: Match information and outcomes
- **`innings`**: Innings-level data for each match
- **`overs`**: Over-by-over breakdown
- **`ball_by_ball`**: Detailed ball-by-ball records
- **`player_stats`**: Player performance statistics per inning
- **`venues`**: Cricket ground information
- **`series`**: Tournament and series data

For detailed schema, refer to [`Criclytics DBMS.sql`](Criclytics%20DBMS.sql).

## 🚀 Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Criclytics_DBMS_SE_Proj
   ```

2. **Install Python dependencies**
   ```bash
   pip install streamlit pymysql pandas matplotlib
   ```

3. **Set up MySQL database**
   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE criclytics;
   USE criclytics;
   SOURCE Criclytics\ DBMS.sql;
   ```

4. **Configure database connection**
   Update the database configuration in [`dbms_streamlit.py`](dbms_streamlit.py):
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'criclytics'
   }
   ```

5. **Load sample data (optional)**
   ```bash
   python dbms_proj.py
   ```

## 📖 Usage

### Running the Web Dashboard
```bash
streamlit run dbms_streamlit.py
```

The dashboard will be available at `http://localhost:8501`

### Available Operations
1. **Team Performance**: View teams with 100+ matches and their win statistics
2. **Update Team Stats**: Execute stored procedures to update team statistics
3. **Best Bowler**: Display top 10 bowlers by wickets taken
4. **Player Search**: Search for players by name

### Data Import
To import cricket match data from JSON files:
```bash
python dbms_proj.py
```

Ensure your JSON data files are in the specified directory path.

## 📁 Project Structure

```
Criclytics_DBMS_SE_Proj/
├── dbms_streamlit.py          # Main Streamlit dashboard application
├── dbms_proj.py               # Data import script for JSON files
├── Criclytics DBMS.sql        # Database schema and table definitions
├── Untitled.sql               # Additional SQL scripts
├── final_er.mwb               # MySQL Workbench ER diagram
├── DBMS_MINI_PROJECT_REPORT.pdf    # Project report
├── SE_Design_Doc_PES2UG22CS446_PES2UG22CS466.pdf  # Design document
└── WhatsApp Image 2024-11-07 at 15.53.28_8399a3ad.jpg  # Project image
```

## 🛠️ Technologies Used

- **Backend**: Python 3.x
- **Database**: MySQL 8.0
- **Web Framework**: Streamlit
- **Database Connectivity**: PyMySQL
- **Data Analysis**: Pandas
- **Visualization**: Matplotlib
- **Database Design**: MySQL Workbench

## 🔍 Key Queries

### Team Performance Analysis
```sql
SELECT teams.name AS Team, COUNT(matches.id) AS Matches_Played,
       SUM(CASE WHEN matches.winner_id = teams.id THEN 1 ELSE 0 END) AS Wins
FROM matches
JOIN teams ON teams.id IN (matches.team1_id, matches.team2_id)
GROUP BY teams.id
HAVING Matches_Played >= 100
ORDER BY Wins DESC
```

### Top Bowlers by Wickets
```sql
SELECT players.name AS Player, 
       IFNULL(SUM(player_stats.wickets_taken), 0) AS Total_Wickets
FROM player_stats
JOIN players ON players.id = player_stats.player_id
GROUP BY player_stats.player_id
HAVING Total_Wickets > 0
ORDER BY Total_Wickets DESC
LIMIT 10
```

## 📊 Features Demonstrated

- **Complex SQL Queries**: Advanced JOIN operations and aggregations
- **Data Visualization**: Interactive charts using Matplotlib
- **Web Interface**: User-friendly Streamlit dashboard
- **Database Design**: Normalized relational database schema
- **Data Import**: Automated JSON data processing
- **Error Handling**: Robust database connection management

## 🤝 Contributors

- **PES2UG22CS446**
- **PES2UG22CS466**

## 📄 Documentation

For detailed project documentation, refer to:
- [Project Report](DBMS_MINI_PROJECT_REPORT.pdf)
- [Design Document](SE_Design_Doc_PES2UG22CS446_PES2UG22CS466.pdf)

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL server is running
   - Check database credentials in configuration

2. **Import Data Issues**
   - Ensure JSON files are in the correct format
   - Verify file path in [`dbms_proj.py`](dbms_proj.py)

3. **Streamlit Port Issues**
   - Use `streamlit run dbms_streamlit.py --server.port 8502` for alternative port

## 📝 License

This project is developed as part of academic coursework for Database Management Systems.

---

For any questions or issues, please refer to the project documentation or contact the contributors.