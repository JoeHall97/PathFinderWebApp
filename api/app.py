from flask import Flask
from flask import request
import PathFinder
import sys
from PathFinder import SearchMap

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"

@app.route("/findpath", methods=['POST'])
def find_path():
    path = []
    try:
        map_width = int(request.headers['mapWidth'])
        map_height = int(request.headers['mapHeight'])
        start = [int(request.headers['startX']),int(request.headers['startY'])]
        end = [int(request.headers['endX']),int(request.headers['endY'])]
        land_positions = list(map(int,request.headers['landpos'].split(',')))
        algo = request.headers['searchalgo']
        m = SearchMap().buildMap(map_width,map_height,start,end,land_positions)
        path = PathFinder.findPath(True,m,algo).path
    except ValueError as ve:
        print(ve)
    return path