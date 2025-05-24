from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# Load movie data
with open('movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html', movie_list=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = similarity[index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended = [movies.iloc[i[0]].title for i in movie_list]
        return jsonify(recommended)
    except:
        return jsonify([])

@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('q', '').lower()
    suggestions = movies[movies['title'].str.lower().str.contains(query, na=False)]['title'].tolist()[:5]
    return jsonify(suggestions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)