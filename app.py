from electoral_college import *
from flask import Flask, flash, render_template, request, redirect, jsonify, url_for
from colour import Color

from typing import Dict

class StatesFlask(Flask):
    
    def __init__(self, name : str):
        super().__init__(name)

        self.states = States()

app = StatesFlask(__name__)

def get_hex(red : int, green : int, blue : int) -> str:
    return '#%02x%02x%02x' % (red, green, blue)

def get_hex_from_vote_frac(frac_vote : float) -> str:
    frac_min = 0.8
    frac_max = 1.2
    frac = (frac_vote - frac_min) / (frac_max - frac_min)

    # 0 - 1
    frac = min(frac, 1)
    frac = max(frac, 0)

    # Red to blue
    no_cols = 20
    colors = list(Color("blue").range_to(Color("green"),no_cols))
    
    '''
    no_cols = 19
    colors = list(Color("blue").range_to(Color("#07A40E"),10))
    colors += list(Color("#07A40E").range_to(Color("red"),10))[1:]
    '''
    idx = int(frac * no_cols)
    idx = min(idx, no_cols-1)
    color = colors[idx]

    return color.hex

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', move_people_value=0)

@app.route("/get_list_of_states", methods=["POST"])
def get_list_of_states() -> str:

    # Sort states
    names = [get_label_from_st(st) for st in St]
    names.sort()

    # Options
    ret = ""
    for name in names:
        ret += '<option>%s</option>' % (name)

    return ret

@app.route("/move_people", methods=["POST"])
def move_people() -> Dict[str, str]:
    # print(request.args)
    # move_people_value = request.args.get('move_people_value')

    move_people_value = request.form["move_people_slider_name"]
    print(move_people_value)

    try:
        move_people_value_int = int(move_people_value)

        pop_actual = app.states.states[St.CALIFORNIA].pop_actual
        pop_move = (move_people_value_int / 100.0) * pop_actual
        app.states.shift_population_from_state(St.CALIFORNIA, pop_move)

        # Assign house seats
        app.states.assign_house_seats_priority()

        # Check no electoral college votes
        app.states.calculate_state_vote_fracs()
    
    except:
        print("Move people value not an integer?")

    ret_dict = {}
    for state in app.states.states.values():
        ret_dict["#"+state.abbrev] = get_hex_from_vote_frac(state.frac_vote)

    print(ret_dict)
    return ret_dict