from flask import Flask, render_template, request, g, current_app
import sqlite3
import pandas as pd

app = Flask(__name__)

#from .searcher import searcher
#idk why but if we put searcher and app separately and try to use the 
#above line of code, there will be an importerror
@app.route('/')
def main():
    return render_template('main.html')
  #  return "hi there"

#retrieve database to use in our webapp
def get_db():
    if 'foodz' not in g:
        g.foodz = sqlite3.connect(
            current_app.config['foodz.db'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.foodz.row_factory = sqlite3.Row
    g.foodz.execute('''CREATE TABLE IF NOT EXISTS recipes(title TEXT, ingredients TEXT, instructions TEXT)''')
    return g.foodz

def close_db(e=None):
    db = g.pop('foodz', None)
    if db is not None:
        db.close()

def searcher(ingredientz):
    #our searcher function
    ingrs = ingredientz.split() 
    #splits the ingredients the user enters into a list
    likey = ""
    for ig in ingrs:
        likey += f"R.ingredients LIKE '%{ig}%' OR "
        #took me the entire afternoon to figure the above line out. :')
        #so that our program returns recipes that include any or all of the ingredients the user specifies. 
    conn = sqlite3.connect("foodz.db")
    query = \
    f"""
    SELECT * FROM recipes R
    WHERE {likey[:-3]} 
    """
    df = pd.read_sql_query(query, conn)
    return df   
@app.route('/finder/', methods=['POST', 'GET'])
def finder():
    if request.method == 'GET':
        return render_template('finder.html')
    else:
        #input_ingredients = request.form['ingredients'].split(',')
        ingredients = request.form['ingredients']
        recipe = searcher(ingredients)
        newr = recipe.sample(n=1)
        #select a random row from the dataframe
        title = newr['title'].iloc[0]
        #i tried to_string, but the output ended up being truncated.
        ingrz = newr['ingredients'].iloc[0]
        steps = newr['recipe'].iloc[0]
        return render_template('finder.html', 
                               ingredients=True,
                               title = title,
                               ingrz = ingrz,
                               steps = steps)