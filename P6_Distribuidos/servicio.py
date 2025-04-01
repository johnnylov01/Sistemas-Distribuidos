from flask import Flask, jsonify
import random
app = Flask(__name__)
canciones=[{"titulo":"Hotel California", "artista":"Eagles"},
           {"titulo":"Bohemian Rhapsody", "artista":"Queen"},
           {"titulo":"Stairway to Heaven", "artista":"Led Zeppelin"},
           {"titulo":"Imagine", "artista":"John Lennon"},
           {"titulo":"Hey Jude", "artista":"The Beatles"},
           {"titulo":"Smells Like Teen Spirit", "artista":"Nirvana"},
           {"titulo":"Billie Jean", "artista":"Michael Jackson"},
           {"titulo":"Knockin' on heaven's door", "artista":"Bob Dylan"},
           {"titulo":"Superstition", "artista":"Stevie Wonder"},
           {"titulo":"I Want to Break Free", "artista":"Queen"},
           {"titulo":"Sweet Child o' Mine", "artista":"Guns N' Roses"},
           {"titulo":"Back in Black", "artista":"AC/DC"},
           {"titulo":"Born to Run", "artista":"Bruce Springsteen"},
           {"titulo":"Like a Rolling Stone", "artista":"Bob Dylan"},
           {"titulo":"Wonderwall", "artista":"Oasis"},
           {"titulo":"Rolling in the Deep", "artista":"Adele"},
           {"titulo":"Uptown Funk", "artista":"Mark Ronson ft. Bruno Mars"}]
@app.route("/recomendacion")
def recomendacion():
    cancion = random.choice(canciones)
    return jsonify(cancion)
@app.route("/recomendacion/<artista>")
def obtener_cancion_por_artista(artista):
    resultado = [c for c in canciones if c["artista"].lower() == artista.lower()]
    
    if resultado:
        return jsonify(random.choice(resultado))
    else:
        return jsonify({"error": "No se encontraron canciones de ese artista"}), 404

if __name__ == "__main__":
    app.run(debug=True)