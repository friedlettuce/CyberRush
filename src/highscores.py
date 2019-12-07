import sqlite3


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


def initialDatabaseCreation():
    # Will run the initial database creation
    # Has error checking built in, so if a database already exists it will just pass
    try:
        createTable()
    except sqlite3.OperationalError:
        pass


def addNewPlayer(playername, playerscore):
    # Function will add a new players score to the table
    # Will need to pass in the playername and playerscore here
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("INSERT INTO highscores VALUES (:playerName, :playerScore)",
              {'playerName': playername, 'playerScore': playerscore})
    conn.commit()
    conn.close()


# Function will take in an index (page number) and return the next 5 scores
# Example, index 1 returns first 5, index 2 returns the next 5, etc
def return5Scores(index):
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("SELECT playerName, playerScore from highscores ORDER BY playerScore DESC",)
    scores = c.fetchall()

    for i in range(5, 0, -1):
        try:
            return [scores[index+offset] for offset in range(i)]
        except IndexError:
            pass
    return None


# Returns the average of all scores
def returnscoreavg():

    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute("SELECT playerName, playerScore from highscores ORDER BY playerScore DESC",)
    scores = c.fetchall()
    scoreavg = 0

    for score in scores:
        scoreavg += score[1]
    scoreavg = scoreavg / len(scores)
    return scoreavg
