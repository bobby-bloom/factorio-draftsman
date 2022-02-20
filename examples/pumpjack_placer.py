# pumpjack_placer.py

"""
Creates a copy of the massive overlapping pumpjack blueprint found here:
https://factorioprints.com/view/-LbygJLCDgaBJqsMPqUJ
Can be expanded as much as you dare.
"""

from factoriotools.blueprint import Blueprint


def main():
    blueprint = Blueprint()
    blueprint.set_label("Huge Pumpjacks")
    blueprint.set_icons("pumpjack")

    dim = 64
    for y in range(dim):
        for x in range(dim):
            blueprint.add_entity("pumpjack", position = [x, y])

    print(blueprint.to_string())


if __name__ == "__main__":
    main()