import random # to generate random numbers and random elements from a list
import sqlite3 # database

conn = sqlite3.connect('game_scores.db') #creates
cursor = conn.cursor() # creates a cursor

# this is required for the first run only. this creates a table with the name game_score in the db
# cursor.execute("""CREATE TABLE game_scores (
#                 name test,
#                 difficulty text,
#                 score integer
#                 )""")

def add_score(score): #add the Scores class to the db
    with conn:
        cursor.execute("INSERT INTO game_scores VALUES (:name , :difficulty, :score)",
        {'name': score.name, 'difficulty': score.difficulty, 'score': score.score})
    conn.commit()

def get_all_scores(): # returns all the scores as a list
    cursor.execute("SELECT * FROM game_scores")
    return cursor.fetchall()

def game(game_type):
    print("###### " + game_type + " game ######")

    name = input("Enter Your Name: ")
    levels = ["easy","medium","hard"] # each level
    score = 0 #score for a single game
    game_level = { #contains the operations for each level and operand range
        "easy" : [" + ",10],
        "medium" : [" + ", " - ",50],
        "hard" : [" + ", " - ", " * ",100]
    }


    # quick play 
    if game_type == "quick":
        number_questions = 5
        difficulty = random.choice(levels) # selects a random level from the levels list
    # custom play    
    elif game_type == "custom":
        while True:
            difficulty = input("Enter the preffered Difficulty [easy, medium , hard] ? ").lower()
            if difficulty in levels:
                break
            else: print("Unexpected Input! Try Again")
        while True:
            try:    
                number_questions = int(input("Enter the Number of Questions"))
                break
            except : # to get rid of the possibiltiy of entering other than a int
                print("Unexpected Input! Try Again")


    operations = game_level[difficulty]
    operands_range = operations.pop() # return the last item of the list while removin the item fro the list
    for _ in range(number_questions):
        operation = random.choice(operations) # choose the random operation
        num1 = random.randint(0,operands_range) # randome numbers in the range of operand range
        num2 = random.randint(0,operands_range)
        answer = real_answer(num1, num2, operation)
        try:
            user_input = int(input((str(num1) + operation + str(num2) + " ? " )))
        except :
            user_input = None # if pressed enter without answering the question
        if user_input == answer:
            score += 1
            print("[Correct]",("Answer "+ str(answer)))
        else:
            print("[Incorrect]",("Answer "+ str(answer)))

    score = Scores(name,difficulty,score,number_questions)
    add_score(score) # add the score to the db



def real_answer(num1, num2, operation): # function to check the real answer for the question
    if operation == " + ":
        return  num1 + num2
    elif operation == " - ":
        return num1 - num2
    elif operation == " * ":
        return num1 * num2

#score class
class Scores:
    def __init__(self,name,difficulty,score,n_question):
        self.name = name
        self.difficulty = difficulty
        self.score = float(score/ n_question) * 100
        

#main
while True:
    print ("""
    ############# Game Menu #############
        1.Quick game
        2.Custom game
        3.Display past game details
        4.Exit
    #####################################
    """)

    choice = int(input("Enter your option : "))
    if choice == 4:
        break # exits the game
    elif choice == 3:
        print()
        print ("###### Game Scores ######")
        for x in get_all_scores():
            print(" | ".join(str(y) for y in x))
        print("##########################")
        print ("Number of Games Played : " + str(len(get_all_scores())))
    elif choice == 2:
        print()
        game("custom")
    elif choice == 1:
        print()
        game("quick")
    else :
        print()
        print("Unexpected Input! Try Again!")
