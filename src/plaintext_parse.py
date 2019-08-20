import re
import json

from flask import Flask, render_template


ACT_BREAK = re.compile("^\s*act\s+\S+")
ACTOR_MOVEMENTS = re.compile("(enter|exit|exeunt|re-enter)")
ACTOR_NAMES = re.compile("[A-Z]+")
SCENE_BREAK = re.compile("^\s*scene\s+\S+")

app = Flask(__name__)


def parse_plaintext_script(path):
    output = {}
    french_scene = 1
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
                actors = [word for word in line.strip().split(" ") if re.match(ACTOR_NAMES, word)]
                output[current_act][current_scene][str(french_scene)] = actors
                french_scene += 1
    return output


def is_change(pattern, line):
    return re.match(pattern, line.lower())


def get_change(pattern, line):
    return re.findall(pattern, line.lower().strip())[0]


output = parse_plaintext_script("test/fixtures/the-winters-tale.txt")
print(json.dumps(output, indent=4))


@app.route("/")
def render_table():
    return render_template("index.html", data=output)
