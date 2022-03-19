from flask import Flask, render_template, request, g, current_app
import sqlite3
import pandas as pd
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
        likey += f"R.ingredients LIKE '%{ig}%' AND "
        #took me the entire afternoon to figure the above line out. :')
        #so that our program returns recipes that include any or all of the ingredients the user specifies. 
    conn = sqlite3.connect("xfoodz.db")
    query = \
    f"""
    SELECT * FROM recipes R
    WHERE {likey[:-4]} 
    """
    df = pd.read_sql_query(query, conn)
    return df   
"""
def generate(n):
    new = random.choice(n)
    return new
"""

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
                               ingredients=ingredients,
                               title = title,
                               ingrz = ingrlist,
                               steps = steplist,
                               category = category)
@app.route('/generator/', methods=['POST', 'GET'])
def generator():
    #load in our saved model
    model=tf.keras.models.load_model('recipe_gen_model.h5')

    #load in our chars variable from the chars.pkl file
    #this contains all chars avalible from the training data
    chars= pickle.load(open('chars.pkl', 'rb'))

    #load in X from the pickled file, this variable contains the 
    #first 50 possible starting seeds. One will be randomly selected. 
    X=pickle.load(open('X_50.pkl', 'rb'))

    #load in the lines file. this file contains all of the lines which
    #are used as predictor information by the model
    lines=pickle.load(open('lines.pkl', 'rb'))

    #if the method is get, render the generator template to collect the users
    #preferance of generation length
    if request.method == 'GET':
        return render_template('generator.html')
    #if the method is post, generate a new recipe using the user selected
    #length and then remove the start char 'Æ' before displaying it to the user
    else:
        gen_length = request.form['gen_length']

        new_recipe=generate_string(gen_length, model,X,chars,lines)
        new_recipe=new_recipe.replace('Æ', '')

        return render_template('generator.html', new_recipe=new_recipe, length= gen_length)

def sample(preds, temp):
    '''
    This function takes the prediction list and samples it randomly 
    acording to the temperature provided. 

    @params 
    preds-the list of predictions
    temp-the temperature (how random you want the prediction to be)
    '''
    # format the model predictions
    preds = np.asarray(preds).astype("float64")
    
    # construct normalized Boltzman with temp
    probs = np.exp(preds/temp)
    probs = probs / probs.sum()
    
    # sample from Boltzman
    samp = np.random.multinomial(1, probs, 1)
    return np.argmax(samp)


def generate_string(gen_length, model, X, chars,lines): 
    '''
    This function generates a string based on the read in length,
    model, seed variables, avalible chars, and predictor lines. 
    
    @params
    gen_length(int): the length of the string to be generated
    model: the pretrained generation model
    X(list): the list of possible seeds
    chars(list): the list of all used chars from the training data
    lines(list): the list of all predictor lines
    '''
    #saves the various read in arguments to their variables
    temp=.1
    seed_index = 0
    max_len=20
    X=X
    gen_length=int(gen_length)
    
    
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
