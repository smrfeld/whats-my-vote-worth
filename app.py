from electoral_college import *
from flask import Flask, flash, render_template, request, redirect, jsonify, url_for
from colour import Color

from typing import Dict

class StatesFlask(Flask):
    
    def __init__(self, name : str):
        super().__init__(name)

        self.states = States()

app = StatesFlask(__name__)

# Logging
app.states.log.setLevel(logging.ERROR)

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
    return render_template('index.html')

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')

@app.route("/get_list_of_states", methods=["POST"])
def get_list_of_states() -> str:

    # Sort states
    names = [get_label_from_st(st) for st in St]
    names.sort()

    # Options
    ret = ""
    for name in names:
        ret += '<option value="%s">%s</option>' % (name,name)

    return ret

@app.route("/get_list_of_states_and_entire_us", methods=["POST"])
def get_list_of_states_and_entire_us() -> str:
    ret = get_list_of_states()
    label = "Entire U.S."
    value = "ENTIRE"
    ret = ('<option value="%s">%s</option>' % (value, label)) + ret

    return ret

@app.route("/reload", methods=["POST"])
def reload() -> Dict[str, str]:
    move_people_value = request.form["move_people_slider_name"]

    try:
        move_people_value_int = int(move_people_value)

        pop_actual = app.states.states[St.CALIFORNIA].pop_actual
        pop_move = (move_people_value_int / 100.0) * pop_actual
        app.states.shift_population_from_state(St.CALIFORNIA, pop_move)
    except:
        print("Move people value not an integer?")
    
    # Assign house seats
    try:
        app.states.assign_house_seats_priority()
    except:
        print("Could not assign house seats by priority method")

    # Check no electoral college votes
    try:
        app.states.calculate_state_vote_fracs()
    except:
        print("Could not calculate electoral college votes")
    
    ret_dict = {}

    # Return colors
    ret_dict["colors"] = {}
    for state in app.states.states.values():
        ret_dict["colors"]["#"+state.abbrev] = get_hex_from_vote_frac(state.frac_vote)

    # Return vote frac
    ret_dict["vote_fracs"] = {}
    for state in app.states.states.values():
        ret_dict["vote_fracs"]["#"+state.abbrev] = (get_label_from_st(state.st), state.frac_vote)

    # Return biggest/smallest vote frac
    biggest_frac, biggest_st = app.states.get_biggest_vote_frac()
    ret_dict["biggest_vote_frac"] = biggest_frac
    ret_dict["biggest_vote_state"] = get_label_from_st(biggest_st)
    smallest_frac, smallest_st = app.states.get_smallest_vote_frac()
    ret_dict["smallest_vote_frac"] = smallest_frac
    ret_dict["smallest_vote_state"] = get_label_from_st(smallest_st)

    # Return left comparison
    print(request.form)
    if "compare_left" in request.form:
        compare_left = request.form["compare_left"]
        try:
            st = get_st_from_label(compare_left)
            state = app.states.states[st]
            ret_dict["compare_left_frac"] = state.frac_vote
            ret_dict["compare_left_votes"] = state.get_no_electoral_votes()
            ret_dict["compare_left_pop"] = state.pop
        except:
            print("Could not convert left selection to state!")

    if "compare_right" in request.form:
        compare_right = request.form["compare_right"]
        try:
            st = get_st_from_label(compare_right)
            state = app.states.states[st]
            ret_dict["compare_right_frac"] = state.frac_vote
            ret_dict["compare_right_votes"] = state.get_no_electoral_votes()
            ret_dict["compare_right_pop"] = state.pop
        except:
            print("Could not convert right selection to state!")

    return ret_dict