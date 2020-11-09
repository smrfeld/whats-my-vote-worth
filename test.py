from electoral_college import *

states = States()
total_us_population = states.get_total_us_population()

# Assign house seats
states.assign_house_seats_priority()

# Validate
states.validate_no_reps_matches_actual()

# Check no electoral college votes
states.validate_no_electoral_votes_matches_actual()

# Fraction
states.calculate_state_vote_fracs()

# Shift population
states.shift_population_from_state_to_entire_us(St.CALIFORNIA, 33)

# Assign house seats
states.assign_house_seats_priority()

# Check no electoral college votes
states.calculate_state_vote_fracs()