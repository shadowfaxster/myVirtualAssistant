import pandas as pd
import csv
import time
def remy_interactions():
    with open("1K_dataset.csv") as db:
        reader = csv.DictReader(db)
        dictionary = {}

        for row in reader:
            title = row[1]
            ingredients = row[2]
            directions = row[3]
            #link = row[4]
            #source = row[5]
            NER = row[6]
            food_details = tuple(ingredients, directions, NER)
            food_information = {title:food_details}
            dictionary.update(food_details)
        user_input = input()
        if user_input == "Hey Remy":
            print("Hello there! What do you want today in the menu?")
            user_input = ()
            if user_input in dictionary:
                print("Great! Let's start cooking!")
                time.sleep(2)
                print("You will need these ingredients: ", ingredients)
                time.sleep(2)
                print("Do you have all of these?")
                user_input = ()
                if user_input == "Yes":
                    print("Great, I'll show you the steps")
                    time.sleep(2)
                    print(directions)
                else:
                    print("Ok, we'll find another food that has exactly the ingredients you have at hand")
                    time.sleep(2)
                    print("What ingredients do you have right now?")
                    user_input = input()
                    if user_input in dictionary[food_details]:
                        print("I've got something for you. What about this?")
                        time.sleep(1)
                        print(title, "which has the following ingredients", ingredients)
            else:
                print("Sorry, could not find that 😔")
        else:
            print("You have to say Hey Remy for starting the app")