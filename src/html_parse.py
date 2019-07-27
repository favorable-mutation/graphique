#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup

chart = {}

with open("test/fixtures/the-winters-tale.html", "r") as script:

    script_soup = BeautifulSoup(script, "html.parser")
    act = 0
    scene = 0

    for divider in script_soup.find_all("h3"):
        neighbor = divider.next_sibling.next_sibling
        if neighbor.name == "h3":
            act += 1
            scene = 0
        else:
            scene +=1
            # this duplicates iteration because it's called once per scene, but
            # searches through the entire <p> element containing all of the next
            # scenes as well

            # solution: walk through the parent node such that we just add a new
            # cond branch for the tag we're looking at to be a character name
            for tag in neighbor.find_all(name = "a", attrs={"name": re.compile("speech")}):
                print(tag.contents[0].contents[0])

            """
    for tag in script_soup.find_all():
        character = tag.contents[0].contents[0]
        print(tag.next_sibling.next_sibling.contents[1])
        """

        """
        if chart.get(character, []):
            character.n
            chart[character].append()
        else:
            chart[character] = []
        """
