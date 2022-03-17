# Foodle! 
## Contributors:
Conor McCaulley

Gracie Ge

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
![finder.png](/flaskyy/finder.png)

In this example, I entered "almond milk sugar". The recipe finder will return a random recipe that contains all three ingredients that I entered. 
