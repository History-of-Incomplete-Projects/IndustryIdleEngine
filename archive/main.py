import argparse, sys

from engine.map import Oslo
from engine.collect import Collect
from engine.sql import create_all, add_object

from engine.building import construct_buildings

from app.cutie import app
# designed for 1334x969 dimensions

parser = argparse.ArgumentParser()
parser.add_argument('--newmap', default=False)
args = parser.parse_args()


if __name__ == "__main__":
    create_all()

    # add_object(Oslo())
    # Collect(new_map=args.newmap)

    # app()

    construct_buildings()