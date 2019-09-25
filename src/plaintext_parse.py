import json
import re
import string

from flask import Flask, render_template


ACT_BREAK = re.compile("^\s*act\s+\S+")
ACTOR_MOVEMENTS = re.compile("(enter|exit|exeunt|re-enter)")
ACTOR_NAMES = re.compile("\\b[A-Z]+\\b")
SCENE_BREAK = re.compile("^\s*scene\s+\S+")


def exeunt(current_characters, changed_characters):
    return []


def exit(current_characters, changed_characters):
    for character in changed_characters:
        current_characters.remove(character)
    return current_characters


def enter(current_characters, changed_characters):
    for character in changed_characters:
        current_characters.append(character)
    return current_characters


MOVEMENT_FUNCS = {"enter": enter, "re-enter": enter, "exit": exit, "exeunt": exeunt}

app = Flask(__name__)


def parse_plaintext_script(path):
    output = {}
    french_scene = 1
    current_characters = []
    with open(path, "r") as script:
        for line in script:
            if is_change(ACT_BREAK, line):
                current_act = get_change(ACT_BREAK, line)
                output[current_act] = {}
            elif is_change(SCENE_BREAK, line):
                current_scene = get_change(SCENE_BREAK, line)
                output[current_act][current_scene] = {}
                french_scene = 1
            elif is_change(ACTOR_MOVEMENTS, line):
                changed_characters = [
                    word.strip(string.punctuation)
                    for word in line.strip().split(" ")
                    if re.match(ACTOR_NAMES, word)
                ]
                movement = get_change(ACTOR_MOVEMENTS, line)
                current_characters = handle_movement(
                    movement, current_characters, changed_characters
                )
                if any(current_characters):
                    output[current_act][current_scene][str(french_scene)] = current_characters[:]
                french_scene += 1
    return output


def handle_movement(movement, current_characters, changed_characters):
    movement = movement.lower()
    return MOVEMENT_FUNCS[movement](current_characters, changed_characters)


def is_change(pattern, line):
    return re.match(pattern, line.lower())


def get_change(pattern, line):
    return re.findall(pattern, line.lower().strip())[0]


output = parse_plaintext_script("test/fixtures/the-winters-tale.txt")
print(json.dumps(output, indent=4))


@app.route("/")
def render_table():
    return render_template("index.html", data=output)
