#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 17:11:14 2019

@author: Joseph Hall
"""
from math import sqrt
import sys
from typing import Tuple
from typing_extensions import Self

directions = {"north":-1, "south":1, "east":1, "west":-1}

class SearchMap:
    """An object with a map and a path"""
    def __init__(self, search_map: list[str] = [], path: list[str] = []) -> None:
        self.search_map = search_map
        self.curr_pos = []
        self.path = path
        self.start = self.__start()
        self.goal = self.__goal()
        self.__drawPath()
        self.cost = self.__cost()
        self.heuristic = self.__heuristic()
        self.heuristicAndCost = self.cost + self.heuristic

    def __str__(self):
        s = ""
        for m in self.search_map:
            s += f'{m.strip()}\n'
        s += f'{self.path}\n'
        s += f'Current position: {self.curr_pos}'
        return s
        
    def __drawPath(self) -> None:
        pos = self.start
        if pos == [-1]:
            return
        for p in self.path:
            if(p=="north" or p=="south"):
                pos[0] += directions[p]
            else:
                pos[1] += directions[p]
            line = self.search_map[pos[0]]
            self.search_map[pos[0]] = line[0:pos[1]] + '.' + line[pos[1]+1:len(line)]
        self.curr_pos = pos
        
    def __start(self) -> list[int]:
        """
        Finds the coridinants of the start position
        RETURNS: the x,y cordinants as a list OR a list containing -1 if the start cannot be found
        """
        pos = 0
        for line in self.search_map:
            if(line.find('S')!=-1):
                return [pos,line.find('S')]
            pos += 1
        return [-1]

    def __goal(self) -> list[int]:
        """
        Finds the coridinants of the goal position
        RETURNS: the x,y cordinants as a list OR a list containing -1 if the start cannot be found
        """
        pos = 0
        for line in self.search_map:
            if(line.find('G')!=-1):
                return [pos,line.find('G')]
            pos += 1
        return [-1]

    def __cost(self) -> int:
        """Calculates the cost of the current path for a given map."""
        return len(self.path)

    def __heuristic(self) -> int:
        """Calculates the heuristic value of a given maps path."""
        if len(self.goal) != 2 or len(self.curr_pos) != 2:
            return 0
        goal_pos = self.goal
        curr_pos = self.curr_pos
        # √((posX-goalX)^2 + (posY-goalY)^2)
        x_value = (curr_pos[0]-goal_pos[0]) * (curr_pos[0]-goal_pos[0])
        y_value = (curr_pos[1]-goal_pos[1]) * (curr_pos[1]-goal_pos[1])
        return sqrt(x_value+y_value)

    def readMap(self,map_name: str) -> Self:
        """Read in a map from a text file"""
        m = open(map_name,'r')
        self.search_map = [line.strip() for line in m]
        self.start = self.__start()
        self.goal = self.__goal()
        self.__drawPath()
        self.cost = self.__cost()
        self.heuristic = self.__heuristic()
        self.heuristicAndCost = self.cost + self.heuristic
        return self

    def buildMap(self,width: int,height: int,start: list[int],end: list[int],land_pos: list[list[int]]) -> Self:
        # check if given values are valid 
        if not width or width <= 2:
            raise ValueError('Width must be a value greater than 2')
        if not height or height <= 2:
            raise ValueError('Height must be a value greater than 2')
        if not start or len(start) != 2:
            raise ValueError('Start must be an array with containing with only x,y values')
        if not end or len(end) != 2:
            raise ValueError('End must be an array with containing with only x,y values')
        # build blank map
        m = []
        for y in range(height):
            if y == 0 or y == height-1:
                d = '-' * (width-2)
                m.append(f'+{d}+')
            else:
                s = ' ' * (width-2)
                m.append(f'|{s}|')
        # add in start, goal and land
        m[start[1]] = f'{m[start[1]][0:start[0]]}S{m[start[1]][start[0]+1:width]}'
        m[end[1]] = f'{m[end[1]][0:end[0]]}G{m[end[1]][end[0]+1:width]}'
        for l in land_pos:
            m[l[1]] = f'{m[l[1]][0:l[0]]}X{m[l[1]][l[0]+1:width]}'
        # set object variables
        self.search_map = m
        self.start = self.__start()
        self.goal = self.__goal()
        self.__drawPath()
        self.cost = self.__cost()
        self.heuristic = self.__heuristic()
        self.heuristicAndCost = self.cost + self.heuristic
        return self

def expand(s_map: SearchMap,visted_positions: list[list[int]]) -> list[SearchMap]:
    """Finds all valid new paths for a given map and returns them in a list."""
    maps = []
    pos = s_map.curr_pos
    # check north
    if pos[0]-1>0 and [pos[0]-1,pos[1]] not in visted_positions and (s_map.search_map[pos[0]-1][pos[1]]==' ' or s_map.search_map[pos[0]-1][pos[1]]=='G'):
        new_path = s_map.path.copy()
        new_path.append("north")
        maps.append(SearchMap(s_map.search_map.copy(),new_path))
    # check south
    if pos[0]+1<len(s_map.search_map) and [pos[0]+1,pos[1]] not in visted_positions and (s_map.search_map[pos[0]+1][pos[1]]==' ' or s_map.search_map[pos[0]+1][pos[1]]=='G'):
        new_path = s_map.path.copy()
        new_path.append("south")
        maps.append(SearchMap(s_map.search_map.copy(),new_path))
    # check west
    if pos[1]-1>0 and [pos[0],pos[1]-1] not in visted_positions and (s_map.search_map[pos[0]][pos[1]-1]==' ' or s_map.search_map[pos[0]][pos[1]-1]=='G'):
        new_path = s_map.path.copy()
        new_path.append("west")
        maps.append(SearchMap(s_map.search_map.copy(),new_path))
    # check east
    if pos[1]+1<len(s_map.search_map[pos[0]]) and [pos[0],pos[1]+1] not in visted_positions and (s_map.search_map[pos[0]][pos[1]+1]==' ' or s_map.search_map[pos[0]][pos[1]+1]=='G'):
        new_path = s_map.path.copy()
        new_path.append("east")
        maps.append(SearchMap(s_map.search_map.copy(),new_path))
    return maps

def validateMap(s_map: SearchMap) -> Tuple[bool,str]:
    """
    Checks whether a given map is valid or not.
    RETURNS: A boolean and a string indicating if the map is valid.
    """
    # check corners 
    if s_map.search_map[0][0] != '+' or s_map.search_map[0][len(s_map.search_map[0])-1] != '+':
        return False,"The corners must be a '+' character"
    elif s_map.search_map[len(s_map.search_map)-1][0] != '+' or s_map.search_map[len(s_map.search_map)-1][len(s_map.search_map[0])-1] != '+':
        print('bottom')
        return False,"The corners must be a '+' character"
    # check edges
    for i in range(len(s_map.search_map)):
        if i == 0 or i == len(s_map.search_map)-1:
            for m in s_map.search_map[i][1:len(s_map.search_map[i])-1]:
                if m != '-':
                    return False,"The top edges must consist of '-' characters"
        else:
            if s_map.search_map[i][0] != '|' or s_map.search_map[i][len(s_map.search_map[i])-1] != '|':
                return False,"The corner edges must consist of '|' characters."
    # check start and goal points exist
    if s_map.start == [-1] or s_map.goal == [-1]:
        return False,"A start ('S') and a goal ('G') must be included in the map."
    return True,"The map is valid."

def findPath(debug: bool,s_map: SearchMap,search_type: str) -> SearchMap:
    """
    Searchs a given map for a valid path using a specfied algorithm.
    RETURNS: A map object with a complete path OR None if a valid path cannot be found.
    """
    if search_type not in ["a-star", "best-first", "breadth-first", "depth-first"]:
        raise ValueError(f"Search type {search_type} is not a valid search type.")
        return

    is_valid,message = validateMap(s_map) 
    if not is_valid:
        raise ValueError(message)

    maps = [s_map]
    visted_positions = [s_map.start]
    goal_pos = s_map.goal
    num_expansions = 0
    
    while len(maps) > 0:
        if(debug):
            print(maps[0])
            print(f"Number of expansions: {str(num_expansions)}")
            print(f"Path Length: {len(maps[0].path)}")
        
        num_expansions += 1
        for m in expand(maps.pop(0),visted_positions):
            if(goal_pos==m.curr_pos):
                # add goal back to map
                goal_line = m.search_map[goal_pos[0]]
                goal_line = goal_line[0:goal_pos[1]] + 'G' +  goal_line[goal_pos[1]+1:len(goal_line)]
                m.search_map[goal_pos[0]] = goal_line

                print(m)
                print(f"Number of expansions: {str(num_expansions)}")
                print(f"Path Length: {len(m.path)}")
                return m

            if(search_type in ["a-star", "best-first", "breadth-first"]):
                maps.append(m)
            elif(search_type=="depth-first"):
                maps = [m] + maps
            visted_positions.append(m.curr_pos)
        
        if(search_type=="a-star"):
            maps = sorted(maps,key=lambda x: x.heuristicAndCost,reverse=False)
        elif(search_type=="best-first"):
            maps = sorted(maps,key=lambda x: x.heuristic)       

    return None     

def main() -> None:
    # alogrithms = ["a-star", "best-first", "breadth-first", "depth-first"]
    try:
        if len(sys.argv) == 4:
            search_map = SearchMap().readMap(str(sys.argv[2]))
            findPath(True,search_map,str(sys.argv[3]))
        elif len(sys.argv) == 3:
            search_map = SearchMap().readMap(str(sys.argv[1]))
            findPath(False,search_map,str(sys.argv[2]))
        else:
            search_map = SearchMap().readMap("../Maps/map3.txt")
            findPath(False,search_map,"a-star")
    except ValueError as ve:
        print(ve)

if __name__ == "__main__":  
    main()