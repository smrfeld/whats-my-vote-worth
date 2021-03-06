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

    # Reset population
    app.states.reset_state_populations_to_actual()

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

def fill_out_ret_dict_from_label(ret_dict : Dict[str,str], base_str : str, label : str):
    if label == "ENTIRE":
        fill_out_ret_dict_from_entire_us(ret_dict, base_str)
    else:
        try:
            st = get_st_from_label(label)
            fill_out_ret_dict_from_state(ret_dict, base_str, st)
        except:
            print("Error filling out ret_dict: %s from label: %s" % (base_str,label))

def fill_out_ret_dict_from_state(ret_dict : Dict[str,str], base_str : str, st : St):
    state = app.states.states[st]
    ret_dict[base_str + "state"] = get_label_from_st(st)
    ret_dict[base_str + "frac"] = state.get_frac_vote_str()
    ret_dict[base_str + "vote"] = state.get_no_electoral_votes_str()
    ret_dict[base_str + "pop"] = state.get_pop_str()

def fill_out_ret_dict_from_entire_us(ret_dict : Dict[str,str], base_str : str):
    ret_dict[base_str + "state"] = "Entire U.S."
    ret_dict[base_str + "frac"] = "-"
    ret_dict[base_str + "vote"] = "%d" % app.states.get_no_electoral_votes()
    ret_dict[base_str + "pop"] = convert_pop_to_str(app.states.get_total_us_population_actual())

@app.route("/move_people_and_reload", methods=["POST"])
def move_people_and_reload() -> Dict[str, str]:

    if "state_move_from" in request.form and "state_move_to" in request.form and "move_people_slider_name" in request.form:
        val_from = request.form["state_move_from"]
        val_to = request.form["state_move_to"]
        val_percent = request.form["move_people_slider_name"]

        if val_from == val_to:
            # No need to shift!
            pass
        else:
            try:
                move_people_value_int = int(val_percent)

                if val_from == "ENTIRE":
                    st_to = get_st_from_label(val_to)
                    app.states.shift_population_from_entire_us_to_state(st_to, move_people_value_int)

                elif val_to == "ENTIRE":
                    st_from = get_st_from_label(val_from)
                    app.states.shift_population_from_state_to_entire_us(st_from, move_people_value_int)

                else:
                    st_from = get_st_from_label(val_from)
                    st_to = get_st_from_label(val_to)
                    app.states.shift_population_from_state_to_state(st_from, st_to, move_people_value_int)
                
            except:
                print("Could not move people")
    
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
    ret_dict["biggest_vote_frac"] = convert_frac_vote_to_str(biggest_frac)
    ret_dict["biggest_vote_state"] = get_label_from_st(biggest_st)
    smallest_frac, smallest_st = app.states.get_smallest_vote_frac()
    ret_dict["smallest_vote_frac"] = convert_frac_vote_to_str(smallest_frac)
    ret_dict["smallest_vote_state"] = get_label_from_st(smallest_st)

    # Return left/right comparison
    lr = compare()
    ret_dict.update(lr)

    # Return move ones
    if "state_move_from" in request.form:
        fill_out_ret_dict_from_label(ret_dict, "move_left_", request.form["state_move_from"])

    if "state_move_to" in request.form:
        fill_out_ret_dict_from_label(ret_dict, "move_right_", request.form["state_move_to"])

    if "state_move_from" in request.form and "move_people_slider_name" in request.form:
        try:
            move_people_value_int = int(request.form["move_people_slider_name"])

            if request.form["state_move_from"] == "ENTIRE":
                pop_move = app.states.get_total_us_population_actual()
            else:
                st = get_st_from_label(request.form["state_move_from"])
                state = app.states.states[st]
                pop_move = state.pop_actual
        
            ret_dict["pop_moved"] = convert_pop_to_str(pop_move * move_people_value_int / 100.0)
        except:
            print("Could not get percent to move")

    return ret_dict

@app.route("/compare", methods=["POST"])
def compare() -> Dict[str, str]:

    ret_dict = {}

    # Left comparison
    if "compare_left" in request.form:
        fill_out_ret_dict_from_label(ret_dict, "compare_left_", request.form["compare_left"])

    # Right comparison
    if "compare_right" in request.form:
        fill_out_ret_dict_from_label(ret_dict, "compare_right_", request.form["compare_right"])

    # Relative
    if "compare_left" in request.form and "compare_right" in request.form:
        compare_left = request.form["compare_left"]
        compare_right = request.form["compare_right"]
        try:
            st_left = get_st_from_label(compare_left)
            st_right = get_st_from_label(compare_right)
            state_left = app.states.states[st_left]
            state_right = app.states.states[st_right]
            ret_dict["compare_rel"] = "%.1fx" % (state_left.frac_vote / state_right.frac_vote)
        except:
            print("Could not convert get comparison!")

    return ret_dict