from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from flask_table import Table, Col


class Results(Table):
    id = Col('Id', show=False)
    title = Col('Recommendation List')

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/rating", methods=["GET", "POST"])
def rating():
    if request.method=="POST":
        return render_template('recommendation.html')
    return render_template('rating.html')


@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    if request.method == 'POST':
        movies = pd.read_csv('movies.csv')


        movies = pd.concat([movies, movies.genres.str.get_dummies(sep='|')], axis=1)
        

        
        categories = movies.drop(['title', 'genres', 'IMAX', 'movieId'], axis=1)

        preferences = []

        Action = request.form.get('Action')
        Adventure = request.form.get('Adventure')
        Animation = request.form.get('Animation')
        Children = request.form.get('Children')
        Comedy = request.form.get('Comedy')
        Crime = request.form.get('Crime')
        Documentary = request.form.get('Documentary')
        Drama = request.form.get('Drama')
        Fantasy = request.form.get('Fantasy')
        FilmNoir = request.form.get('FilmNoir')
        Horror = request.form.get('Horror')
        Musical = request.form.get('Musical')
        Mystery = request.form.get('Mystery')
        Romance = request.form.get('Romance')
        SciFi = request.form.get('SciFi')
        Thriller = request.form.get('Thriller')
        War = request.form.get('War')
        Western = request.form.get('Western')

        
        preferences.insert(0, int(Action))
        preferences.insert(1,int(Adventure))
        preferences.insert(2,int(Animation))
        preferences.insert(3,int(Children))
        preferences.insert(4,int(Comedy))
        preferences.insert(5,int(Crime))
        preferences.insert(6,int(Documentary))
        preferences.insert(7,int(Drama))
        preferences.insert(8,int(Fantasy))
        preferences.insert(9,int(FilmNoir))
        preferences.insert(10,int(Horror))
        preferences.insert(11,int(Musical))
        preferences.insert(12,int(Mystery))
        preferences.insert(13,int(Romance))
        preferences.insert(14,int(SciFi))
        preferences.insert(15,int(War))
        preferences.insert(16,int(Thriller))
        preferences.insert(17,int(Western))

        def get_score(a, b):
           return np.dot(a, b)

        def recommendations(X, n_recommendations):
            movies['score'] = get_score(categories, preferences)
            return movies.sort_values(by=['score'], ascending=False)['title'][:n_recommendations]

        output= recommendations(preferences, 20)
        table = Results(output)
        table.border = True
        return render_template('recommendation.html', table=table)

if __name__ == '__main__':
   app.run(debug = True)