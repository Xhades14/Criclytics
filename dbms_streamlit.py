import streamlit as st
import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root@DBMS',
    'database': 'criclytics'
}

# Function to execute queries or commands in the database
def execute_query(query, params=None, fetch_result=False):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_result:
                result = cursor.fetchall()
                return result
            connection.commit()
    finally:
        connection.close()

# Function to call a stored procedure
def call_stored_procedure(proc_name, params=()):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.callproc(proc_name, params)
            connection.commit()
    finally:
        connection.close()

# Function to call a SQL function and return its result
def call_sql_function(func_name, params=()):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT {func_name}(%s)", params)
            result = cursor.fetchone()
            return result[0] if result else None
    finally:
        connection.close()

# Title and description
st.title("Cricket Analytics Dashboard with SQL Integration")

# Dropdown to select operation
operation_type = st.selectbox(
    "Select operation",
    ["Team Performance", "Update Team Stats", "Best Bowler", "Player Search"]
)

# Team Performance Analysis (with 100+ matches)
if operation_type == "Team Performance":
    st.subheader("Team Performance Analysis (100+ Matches)")
    query = """
    SELECT teams.name AS Team, COUNT(matches.id) AS Matches_Played,
           SUM(CASE WHEN matches.winner_id = teams.id THEN 1 ELSE 0 END) AS Wins
    FROM matches
    JOIN teams ON teams.id IN (matches.team1_id, matches.team2_id)
    GROUP BY teams.id
    HAVING Matches_Played >= 100
    ORDER BY Wins DESC
    """
    connection = pymysql.connect(**db_config)
    data = pd.read_sql(query, connection)
    connection.close()
    st.dataframe(data)
    st.bar_chart(data.set_index("Team"))

# Option to call a stored procedure to update team statistics
elif operation_type == "Update Team Stats":
    st.subheader("Update Team Statistics")
    team_id = st.number_input("Enter Team ID", min_value=1)
    if st.button("Update Team Stats"):
        call_stored_procedure("update_team_stats", (team_id,))
        st.success("Stored procedure executed successfully!")

# Best Batsman and Bowler Dashboard
elif operation_type == "Best Bowler":
    st.subheader("Best Bowler in Recent Matches")


    # Query for best bowlers based on aggregated wickets from player_stats table
    bowler_query = """
    SELECT players.name AS Player, 
           IFNULL(SUM(player_stats.wickets_taken), 0) AS Total_Wickets
    FROM player_stats
    JOIN players ON players.id = player_stats.player_id
    GROUP BY player_stats.player_id
    HAVING Total_Wickets > 0  -- Only show bowlers with wickets taken
    ORDER BY Total_Wickets DESC
    LIMIT 10
    """

    # Database connection and query execution
    connection = pymysql.connect(**db_config)
    bowlers = pd.read_sql(bowler_query, connection)
    connection.close()

    st.subheader("Top 10 Bowlers by Wickets")
    st.dataframe(bowlers)

    # Plotting the bar chart for best bowlers
    fig, ax = plt.subplots()
    ax.bar(bowlers['Player'], bowlers['Total_Wickets'], color='blue')
    ax.set_xlabel('Player')
    ax.set_ylabel('Total Wickets')
    ax.set_title('Top 10 Best Bowlers by Wickets')
    ax.tick_params(axis='x', rotation=45)  # Rotate player names on x-axis for readability
    st.pyplot(fig)


# Player Search Feature
elif operation_type == "Player Search":
    st.subheader("Search for a Player")
    player_name = st.text_input("Enter Player Name")
    if player_name:
        search_query = """
        SELECT id, name, nationality
        FROM players
        WHERE name LIKE %s
        """
        connection = pymysql.connect(**db_config)
        players = pd.read_sql(search_query, connection, params=(f"%{player_name}%",))
        connection.close()
        
        if not players.empty:
            st.dataframe(players)
        else:
            st.warning("No players found with that name.")

# Matchup Analysis Feature
'''elif operation_type == "Matchup Analysis":
    st.subheader("Matchup Analysis: Player vs Player")
    player1_id = st.number_input("Enter Player 1 ID", min_value=1)
    player2_id = st.number_input("Enter Player 2 ID", min_value=1)
    
    if st.button("Analyze Matchup"):
        # Query to fetch player stats for both players
        matchup_query = """
        SELECT 
            p1.name AS Player1, p1.total_runs AS Player1_Runs, p1.total_wickets AS Player1_Wickets,
            p2.name AS Player2, p2.total_runs AS Player2_Runs, p2.total_wickets AS Player2_Wickets
        FROM players p1
        JOIN players p2 ON p1.id != p2.id
        WHERE p1.id = %s AND p2.id = %s
        """
        
        connection = pymysql.connect(**db_config)
        matchup_data = pd.read_sql(matchup_query, connection, params=(player1_id, player2_id))
        connection.close()

        if not matchup_data.empty:
            st.dataframe(matchup_data)
        else:
            st.warning("Matchup data not found for the selected players.")'''