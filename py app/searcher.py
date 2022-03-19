#垃圾
import pandas as pd
import sqlite3

from flask import current_app, g
#from flask.cli import with_appcontext

#from flask import Blueprint, g, render_template, url_for, abort

#The following code helps us connect to our database foodz.db
def get_db():
    if 'foodz' not in g:
        g.foodz = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.foodz.row_factory = sqlite3.Row
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
    SELECT * FROM nicerecipes R
    WHERE {likey[:-3]} 
    """
    df = pd.read_sql_query(query, conn)
    return df   