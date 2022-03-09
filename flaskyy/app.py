from flask import Flask, render_template, request, g, current_app
import sqlite3
import pandas as pd
import random
import numpy as np
import pickle
import tensorflow as tf
from scipy.special import softmax

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
    if 'xfoodz' not in g:
        g.xfoodz = sqlite3.connect(
            current_app.config['xfoodz.db'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.xfoodz.row_factory = sqlite3.Row
    g.xfoodz.execute('''CREATE TABLE IF NOT EXISTS recipes(title TEXT, ingredients TEXT, instructions TEXT, category TEXT)''')
    return g.xfoodz

def close_db(e=None):
    db = g.pop('xfoodz', None)
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
    conn = sqlite3.connect("xfoodz.db")
    query = \
    f"""
    SELECT * FROM recipes R
    WHERE {likey[:-3]} 
    """
    df = pd.read_sql_query(query, conn)
    return df   

def generate(n):
    new = random.choice(n)
    return new


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
        newingrz = ingrz.split(" ,")
        ingrlist=[]
        for i in newingrz:
            ingrlist.append(i.replace(' ,','\n'))
        steps = newr['recipe'].iloc[0]
        newsteps = steps.split(". ")
        steplist=[]
        for k in newsteps:
            steplist.append(k.replace('. ','\n'))
        category = newr['category'].iloc[0]
        return render_template('finder.html', 
                               ingredients=True,
                               title = title,
                               ingrz = ingrlist,
                               steps = steplist,
                               category = category)
@app.route('/generator/', methods=['POST', 'GET'])
def generator():
    #load in our saved model
    model=tf.keras.models.load_model('recipe_gen_model.h5')

    #load in our chars variable from the chars.pkl file
    chars= pickle.load(open('chars.pkl', 'rb'))

    X=pickle.load(open('X.pkl', 'rb'))

    lines=pickle.load(open('lines.pkl', 'rb'))


    if request.method == 'GET':
        return render_template('generator.html')
    else:
        gen_legth = request.form['gen_legth']

        new_recipe=generate_string(gen_legth, model,X,chars,lines)

        return render_template('generator.html', new_recipe=new_recipe, legth= gen_legth)



def generate_string(gen_length, model, X, chars,lines): 
    temp=.1
    seed_index = random.randint(0, 50)
    max_len=20
    X=X

    # sequence of integer indices for generated text
    gen_seq = np.zeros((max_len + gen_length, 110))
    
    # first part of the generated indices actually corresponds to the real text
    seed = X[seed_index]
    gen_seq[0:max_len] = seed
    
    # character version
    gen_text = lines[seed_index]
 
    for i in range(0, gen_length):
  
        window = gen_seq[i: i + max_len]

        preds = model.predict(np.array([window]))[0]
        preds = softmax(preds)
        next_index = sample(preds, temp)
        
        # add sampled index to the current output
        gen_seq[max_len + i, next_index] = True
        
        # create the string version
        next_char = chars[next_index]
        gen_text += next_char
    
    # only return the string version because that's what we care about
    return(gen_text)


    def sample(preds, temp):
        # format the model predictions
        preds = np.asarray(preds).astype("float64")
        
        # construct normalized Boltzman with temp
        probs = np.exp(preds/temp)
        probs = probs / probs.sum()
        
        # sample from Boltzman
        samp = np.random.multinomial(1, probs, 1)
        return np.argmax(samp)