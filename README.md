# Foodle! 
## Contributors and Contribution Statement
Conor McCaulley
    1. Built the generation models
    2. Integrated the selected generation model into the flask web app.

Gracie Ge
    1. Build the scrapers which scraped the recipes we used for generation model training and for the recipe search function of the web app. 
    2. Build the flask web app framework and design ad well as the recipe search functionality within the web app.


## Getting Started
Download the entire repository from this site and make sure you have flask and tensorflow installed on your machine.
To install flask, use the command line and enter `pip install Flask`. For Tensorflow to work on M1 Macs, you'll need to go through a few extra steps. 

## Running our webapp
Open the downloaded folder in VS code (or any other code editor of your choice). Navigate to the folder named "flaskyy" by typing `cd (Where you downloaded the repo folder to)/pic16b-food-recommendations/flaskyy`. Alternatively, you can just open a terminal window through the code editor. In this case, entering `cd flaskyy` directly brings you to the flaskyy directory. 

Next, enter the following lines into your terminal:
`export FLASK_ENV=development`
`flask run`

Now you can access the webapp locally! Paste http://127.0.0.1:5000/ into your browser.

Its functions should be pretty simple: navigate to either of the two menu links to find a recipe by entering ingredients, or generate a completely new recipe by entering the length of the recipe you'd like to generate. Note that if you use the recipe generator function, you might be getting a recipe with things that are neither cookable nor edible.

## Searching for a recipe
Here's a demonstration on how the searching function works. Click on `find a recipe` in the menu bar, enter desired ingredients, and click `submit`.

![finder.png](/flaskyy/finder.png)

In this example, I entered "almond milk sugar". The recipe finder will return a random recipe that contains all three ingredients that I entered. 
Here's how it works: we have scraped different world cuisine recipes from allrecipes.com into a csv file (you can check it out at newrecipes.csv), which is then converted into a database `xfoodz.db`. Once a user enters ingredients, our function will query the database for a recipe that matches all the ingredients entered by the user.

## Generating a new recipe
To generate a new recipe, first click on 'generate a new recipe' to navigate to the generator page. A text entry box will appear on the screen, pleses input the legth in characters of the recipe that you with to generate and hit the submit button. The flask application will send the recipe length to the generator model that we have built which will then return the generated recipe. Keep in mind that this process is computationally expensive and may take some time to run. Do not reload the page during this process. The recipe will automatically be displayed on the page when it is finished generating. 

## Limitations
1. If a user enters nonsense, the app will not show an error message. 
2. While the recipe searcher provides users with an extensive variety of different recipes to try, it doesn't take into account the fact that someone might only have ingredients x, y, and z-the returned recipe only **includes** the specified ingredients, but it almost always also contains other ingredients. 
3. The web app can be very sluggish when trying to generate a new recipe due to the computational load of character by character generation. There is not a loading bar or other such device to alert the user that the webpage is functioning normally and thus the user may think that the webpage is frozen and attempt to reload the page which will not fix the problem. 
