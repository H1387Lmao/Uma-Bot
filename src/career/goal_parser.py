# EXAMPLE FILE:
# 
# Mejiro McQueen,F1500=3/R01ArimaKinen=8/F3000=9
# 
from pathlib import Path
import sys

current_dir=Path(__file__).parent
goals_path=current_dir/"goals.txt"

def parse_line(ln, line, FanGoal, RaceGoal, GradeGoal):

    goal = []
    #print(line.split(","))
    uma, goalstr = line.split(",")
    error=0
    goals = goalstr.split("/")
    for g in goals:
        gid = g[0] # F for fanGoal, R for RaceGoal
        try:
#            print(g[1:])
            required, turn = g[1:].split("=")
        
            if gid == "F":
                goal.append(
                    FanGoal(int(required), int(turn))
                )
            elif gid=="G":
                goal.append(
                    GradeGoal(int(required[1]), int(required[1:3]), int(required[3:5]), int(turn))
                )
            else:
                goal.append(
                    RaceGoal(int(required[:2]), required[2:], int(turn))
                )
        except Exception as E:
            print("Error at line:", ln)
            print(E)
            error=1
    if error: sys.exit()
    return uma, goal

def parse_goals(R,F,G):
    goals={}
    t = goals_path.read_text()
    for ln, line in enumerate(t.split("\n")):
        data=line.strip()
        if not data: continue
        uma, goal = parse_line(ln, data,F,R,G)
        goals[uma]=goal

        #print(f"parsed {uma}'s goal data!")
    return goals
    
