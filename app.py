import flask
import json
import jsonschema
from flask import *

app = flask.Flask(__name__)

characters = list()


@app.before_first_request
def loadCharacters():
    global characters

    characters = json.load(open('characters.txt', encoding="UTF-8"))


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', characters=characters)


@app.route('/character', methods=['GET'])
def character():
    if 'nev' not in request.args:
        return "Hiba!"
    else:
        nev = request.args['nev']

    for character in characters:
        if character["nev"] == nev:
            return render_template('character.html', character=character)

    return "Nincs ilyen nevű karakter!"


@app.route('/addCharacter', methods=['POST'])
def addCharacter():
    schema = {
        "type": "object",
        "properties": {
            "nev": {"type": "string"},
            "ritkasasg": {"type": "number"},
            "elem": {"type": "string"},
            "fegyver": {"type": "string"},
            "specialitas": {"type": "string"},
        },
    }

    character = {
        "nev": request.form["nev"],
        "ritkasag": int(request.form["ritkasag"]),
        "elem": request.form["elem"],
        "fegyver": request.form["fegyver"],
        "specialitas": request.form["specialitas"]
    }

    try:
        jsonschema.validate(instance=character, schema=schema)
    except:
        return 'A karakter adatai nem megfelelők!'
    else:
        global characters
        characters.append(character)

        with open("characters.txt", "w", encoding="utf-8") as file:
            file.write(json.dumps(characters, indent=2, ensure_ascii=False))

    return redirect("/")


if __name__ == "__main__":
    app.run()
