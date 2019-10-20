import sqlite3

# Note: only run this function once to initially create the
# Database on a new machine, dont run it a second time
def createTable():
    # Creates a database and connection
    # With c as our cursor
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()

    # Creates the table
    # Maybe also add a date for when they achieved the score?
    c.execute("""CREATE TABLE highscores (
              playerName text,
              playerScore integer
              )""")
    conn.commit()
    conn.close()
# Function will populate the table with placeholders for testing
# Purposes until we integrate the highscores into the actual game
def populateWithPlaceholders():
    # Will input three placeholders
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    # NOTE: need to pass in the players name and score into this function
    # to successfully implement this
    playername = "Placeholder 1"
    playerscore = 100
    c.execute("INSERT INTO highscores VALUES (:playerName, :playerScore)",
              {'playerName': playername, 'playerScore': playerscore})
    playername = "Placeholder 2"
    playerscore = 150
    c.execute("INSERT INTO highscores VALUES (:playerName, :playerScore)",
              {'playerName': playername, 'playerScore': playerscore})
    playername = "Placeholder 3"
    playerscore = 15
    c.execute("INSERT INTO highscores VALUES (:playerName, :playerScore)",
              {'playerName': playername, 'playerScore': playerscore})
    conn.commit()
    conn.close()

def initialDatabaseCreation():
    # Will run the initial database creation by calling the two above functions
    createTable()
    populateWithPlaceholders()

def addNewPlayer(playername, playerscore):
    # Function will add a new players score to the table
    # Will need to pass in the playername and playerscore here
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("INSERT INTO highscores VALUES (:playerName, :playerScore)",
              {'playerName': playername, 'playerScore': playerscore})
    conn.commit()
    conn.close()


def deletePlayer(playername):
    # Function will remove a player from the highscores list
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("DELETE from highscores where playerName =?", (playername,))   # may not work need to test when up and running
    conn.commit()
    conn.close()

def resetHighscores():
    # Function will remove all entries in the highscores list
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("Delete from highscores;",)   # Need to test if this deletes all entries
    conn.commit()
    conn.close()

def displayScores():
    # We will first select the entries in descending order
    # Based on score (higher scores shown first)
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("SELECT playerName, playerScore from highscores ORDER BY playerScore DESC")

    # do we need to a commit here? Need to test
    conn.commit()

    # Rows will contain each sorted entry on every line
    rows = c.fetchall()
    conn.close()


    # For now we will just print to console
    # Until I can figure out how to display it to the pygame application
    for row in rows:
        print(row)
