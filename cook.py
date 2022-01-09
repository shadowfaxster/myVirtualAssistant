
# Cooking ability
import ability
import time
from recipeDatabase import RecipeDatabase

class Cooking(ability.Ability):
    def __init__(self, brain):
        print("Starting cooking routine...")

        super().__init__(brain)

        # LOAD RECIPE DATABASE
        # self.recipes = loadRecipeDatabase()

        self.recipes = RecipeDatabase()

        self.brain = brain


    def start(self):
        # 1. Search recipe
        recipe = self.searchRecipe()

        # 2. Get all ingredients ready
        self.getIngredientsReady(recipe)

        # 3. Start cooking process
        self.guideCooking(recipe)


    def searchRecipe(self):
        found = False;
        while not found and not self.abort:
            self.brain.speak("Please tell me your choice for main ingredients for the recipe")
            mainIngredients = self.brain.listen()
            
            # # Avoid list
            self.brain.speak("List any ingredients you would like to avoid")
            avoidIngredients = self.brain.listen()

            self.brain.speak("let's see what I can find with " + mainIngredients)

            foundItems = self.recipes.search(mainIngredients, avoidIngredients); 

            if len(foundItems) == 0:
                self.brain.speak("Could not find anything with " + mainIngredients)
                continue

            for recipe in foundItems:
                self.brain.speak("How about {}?".format(recipe[0]))

                answer = self.brain.listen()
                intent = self.brain.interpret(answer, ['yes', 'no', 'abort'])

                if intent == 'yes':
                    found = True
                    break

                elif intent == 'abort' and self.checkAbort():
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
        if self.abort:
            return 

        self.brain.speak("Let's get the ingredients ready. We will need {}.".format(recipe[1]))
        self.brain.speak("We'll get them one by one. ")

        print("Listing ingredients...")
        for ingredient in recipe[1]:
            self.brain.speak(ingredient)

            intent = 'Wait'
            while intent != 'yes' and not self.abort:
                time.sleep(0.5)

                self.brain.speak("Ready?")

                answer = self.brain.listen()
                intent = self.brain.interpret(answer, ['yes', 'no', 'abort'])

                if intent == 'abort' and self.checkAbort():
                    return


    def guideCooking(self, recipe):
        if self.abort:
            return

        self.brain.speak("Let's start cooking. When you're ready for the next step, say next.")

        for instruction in recipe[2]:
            if self.abort:
                return

            self.brain.speak(instruction)

            next = False
            while not next and not self.abort: 
                answer = self.brain.listen()
                intent = self.brain.interpret(answer, ['next', 'abort'])

                if intent == 'abort':
                    self.checkAbort()

                if intent == 'next':
                    next = True


if __name__ == '__main__':
    import brain

    brain = brain.Brain()

    cooking = Cooking(brain)
    cooking.start()