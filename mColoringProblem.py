import random

import plotly.express as px
import json

# countries
countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Falkland Islands", "Guyana", "Paraguay",
             "Peru", "Suriname", "Uruguay", "Venezuela"]

# colors
colors = ["blue", "green", "red", "yellow"]

# store neighbors
neighbors = {}


# method to load neighbors.json
def load_neighbours():
    # open and return neighbors from json file
    with open("neighbors.json", "r") as jsonFile:
        # return dict
        return json.load(jsonFile)


# check whether coloring the country is safe
def is_safe(colored_map, country, color):
    # iterate through all neighbors of given country
    for neighbor in neighbors[country]:
        # get color of neighbor if exists in colored_map
        color_of_neighbor = colored_map.get(neighbor, "")

        # then control if colors are the same
        if color_of_neighbor == color:
            # if it is then return false
            return False
    # if there is a not restriction to paint this country to that color
    # return true
    return True


# paint the map using backtracking search algorithm
def paint_the_map(colored_map, country_index, color_index):
    # if index is reached the end of the countries that means all map has been colored correctly
    if country_index == len(countries):
        return True

    # if there is no color exists for current map then return false
    if color_index == len(colors):
        return False

    # get country
    country = countries[country_index]

    # get color
    color = colors[color_index]

    # control is safe to paint
    if is_safe(colored_map, country, color):
        # pair country with color
        colored_map[country] = color

        # proceed to next country
        if paint_the_map(colored_map, country_index + 1, 0):
            # if there is a solution found then return true
            return True
        else:
            # else change the color of the current country
            return paint_the_map(colored_map, country_index, color_index + 1)

    # if it is not safe
    else:
        # try to paint country with next color
        return paint_the_map(colored_map, country_index, color_index + 1)


# colormap should be a dictionary having countries as keys and colors as values
def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names", locations=countries, color=colormap,
                        color_discrete_sequence=[colormap[c] for c in countries], scope="south america")
    fig.show()


# implemented main method
if __name__ == "__main__":
    # load neighbors
    neighbors = load_neighbours()

    # colored map dict to store country - color pairs
    final_map = {}

    # store is map colored
    is_colored = paint_the_map(colored_map=final_map, country_index=0, color_index=random.randint(0, len(colors) - 1))

    # if it is colored then it means a solution has been found
    print("A solution has been found!" if is_colored else "A solution does not exist for this map!")

    # if a solution found then return final map and plot the map
    if is_colored:
        print(f"Final map: {final_map}")
        plot_choropleth(colormap=final_map)
