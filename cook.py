
# Cooking ability
import ability
import time

class Recipe:
    def __init__(self, title, ingredients, instructions):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions


class Cooking(ability.Ability):
    def __init__(self, brain):
        print("Starting cooking routine...")

        super().__init__(brain)

        # LOAD RECIPE DATABASE
        # self.recipes = loadRecipeDatabase()

        self.recipes = [ 
                        Recipe('chicken burrito', 'Chicken, Beans', ['Get ingredients', 'Make burrito']), 
                        Recipe('Chicken fajitas', 'Chicken, Fajitas', ['Get ingredients', 'Make fajitas'])
                        ]

        self.brain = brain


    def start(self):
        # 1. Search recipe
        recipe = self.searchRecipe()

        # 2. Get all ingredients ready
        recipe = self.recipes[1]
        self.getIngredientsReady(recipe)

        # 3. Start cooking process
        #self.startCookingProcess(recipe)


        self.brain.speak("Ok. We're done cooking. Going back to sleep! Bye-bye!")


    def searchRecipe(self):
        found = False;
        while not found and not self.abort:
            self.brain.speak("Please tell me a recipe name:")

            recipeName = self.brain.listen()
            self.brain.speak("let's see what I can find for " + recipeName)

            # foundItems = self.recipeDatabase.search(name)
            foundItems = self.recipes; 

            for recipe in foundItems:
                self.brain.speak("How about {}?".format(recipe.title))

                answer = self.brain.listen()
                intent = self.brain.interpret(answer, ['yes', 'no'])

                if intent == 'yes':
                    found = True
                    break
                elif intent == 'unknown':
                    self.brain.reactOnIntent(intent)
                    self.brain.speak("I'll take that as a No")

            if not found:
                self.brain.speak("That's all I had for {}. Would you like to try something different?".format(recipeName))

                answer = self.brain.listen()
                intent = self.brain.interpret(answer, ['yes', 'no'])

                if intent == 'no':
                    self.checkAbort()

        return recipe


    def getIngredientsReady(self, recipe):
        if not self.abort:
            self.brain.speak("Let's get the ingredients ready. We will need {}.".format(recipe.ingredients))
            self.brain.speak("We'll get them one by one. ")

            print("Listing ingredients...")
            for ingredient in recipe.ingredients.split():
                self.brain.speak(ingredient)

                intent = 'Wait'
                while intent != 'yes' and not self.abort:
                    time.sleep(0.5)

                    self.brain.speak("Ready?")

                    answer = self.brain.listen()
                    intent = self.brain.interpret(answer, ['yes', 'no', 'abort'])

                    if intent == 'abort' and self.checkAbort():
                        return

if __name__ == '__main__':
    import brain

    brain = brain.Brain()

    cooking = Cooking(brain)
    cooking.start()