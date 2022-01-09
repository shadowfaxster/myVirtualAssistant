import ast
import pandas as pd
import re

def processing_receipes():
    cooking_df = pd.read_csv(r'./1K_dataset.csv', index_col=0)

    for column in ['title', 'ingredients', 'directions', 'NER']:
      cooking_df[column] = cooking_df[column].str.lower()

    set_of_shortcuts = set()
    for line in cooking_df['ingredients'].tolist():
        set_of_shortcuts.update(re.findall("\s([a-z]+\.)", line))
    #print(set_of_shortcuts)

    set_of_shortcuts = {'tbsp.': 'tablespoons', 
                        'lb.': 'pound', 
                        'lbs.': 'pounds', 
                        'lg.': 'lenght', 
                        'veg.': 'vegetarian food', 
                        'c.': 'cups', 
                        'sm.': 'small', 
                        'tsp.': 'teaspoon', 
                        'qts.': 'quarts', 
                        'pkg.': 'package', 
                        'doz.': 'dozen', 
                        'sq.': 'square', 
                        'oz.': 'fluid', 
                        'gal.': 'gallon', 
                        'pt.': 'pint', 
                        'qt.': 'quart '}

    for i in range(0, len(cooking_df)):
      for shortcut in set_of_shortcuts.keys():
        if shortcut in cooking_df['ingredients'].iloc[i]:
          cooking_df['ingredients'].iloc[i] = cooking_df['ingredients'].iloc[i].replace(shortcut, set_of_shortcuts[shortcut])

    for column in ['ingredients', 'directions', 'NER']:
        cooking_df[column] = cooking_df[column].apply(lambda elem: ast.literal_eval(elem))
    
    cooking_df.head(5)

    return cooking_df


def get_receipes_given_ingredients(ingredients: list, cooking_df: pd.DataFrame) -> list:
    possible_receipes = list()
    for i in range(0, cooking_df.shape[0]):
        ok = 0

        for ingredient in ingredients:
            if ingredient not in cooking_df['NER'].iloc[i]:
                ok = 1
                break

        if ok == 0:
            possible_receipes.append((cooking_df['title'].iloc[i], cooking_df['ingredients'].iloc[i], cooking_df['directions'].iloc[i]))

    return possible_receipes


def get_receipes_that_contains_this_but_not_that(to_be: list, 
                                                 not_to_be:list, cooking_df: pd.DataFrame) -> list:
    possible_receipes = list()
    for i in range(0, cooking_df.shape[0]):
        ok = 0

        for ingredient in to_be:
            if ingredient not in cooking_df['NER'].iloc[i]:
                ok = 1
                break

        if ok == 0:
            for ingredient in not_to_be:
                if ingredient in cooking_df['NER'].iloc[i]:
                    ok = 1
                    break

        if ok == 0:
            possible_receipes.append((cooking_df['title'].iloc[i], cooking_df['ingredients'].iloc[i], cooking_df['directions'].iloc[i]))

    return possible_receipes


class RecipeDatabase:
    def __init__(self):
        self.cooking_df = processing_receipes()

    def get_cooking_df(self):
        return self.cooking_df

    def search(self, include, exclude):
        include = include.split()
        exclude = exclude.split()

        return get_receipes_that_contains_this_but_not_that(include, exclude, self.cooking_df)

if __name__ == '__main__':
    cooking_df = RecipeDatabase().get_cooking_df()

    print(get_receipes_given_ingredients(['chicken'], cooking_df)[0])
