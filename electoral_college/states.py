from .state import *

class States:

    def __init__(self):

        self.no_voting_house_seats = 435
        self.no_electoral_votes_actual = 538

        self.states = {}
        for st in St:
            self.states[st] = State.actual(st)

    def validate_no_reps_matches_actual(self):
        for state in self.states.values():
            state.validate_no_reps_matches_actual()

    def validate_no_electoral_votes_matches_actual(self):
        no_electoral_votes = self.get_no_electoral_votes()
        assert no_electoral_votes == self.no_electoral_votes_actual

    def get_no_electoral_votes(self) -> int:
        
        # Check no electoral college votes
        no_electoral_votes = sum([state.get_no_electoral_votes() for state in self.states.values()])
        
        # + 3 for DC
        no_electoral_votes += 3
        
        print("No electoral votes: %d" % no_electoral_votes)
        return no_electoral_votes

    def get_total_us_population(self) -> float:
        total_us_population = sum(self.states[state].pop for state in St)
        print("US population: %f" % total_us_population)
        return total_us_population

    def get_total_us_population_actual(self) -> float:
        total_us_population_actual = sum(self.states[state].pop_actual for state in St)
        print("US population actual: %f" % total_us_population_actual)
        return total_us_population_actual

    def calculate_state_vote_fracs(self):
        
        total_us_population = self.get_total_us_population()
        no_electoral_votes = self.get_no_electoral_votes()

        # Fraction
        for state in self.states.values():
            state.frac_electoral = state.get_no_electoral_votes() / no_electoral_votes
            state.frac_vote = state.frac_electoral * (total_us_population / state.pop)

            print("State: %20s frac electoral: %.5f frac vote: %.5f" % 
                (state.st, state.frac_electoral, state.frac_vote))

    def reset_state_populations_to_actual(self):
        for state in self.states.values():
            state.pop = state.pop_actual

    def shift_population_from_state(self, st : St, no_leave : float):
        assert (no_leave <= self.states[st].pop_actual)

        # Remove population from this state
        self.states[st].pop = self.states[st].pop_actual - no_leave

        # Calculate population fracs for all the other states
        total_other_population = sum([state.pop_actual for state in self.states.values() if state.st != st])
        for st_other, state_other in self.states.items():
            if st == st_other:
                continue # skip

            frac = state_other.pop_actual / total_other_population

            # Increment population of other states
            state_other.pop = state_other.pop_actual + frac * no_leave

        print("Populations after: %f million people leave: %s" % (no_leave, st))
        for state in self.states.values():
            print("%20s : %.5f -> %.5f" % (state.st, state.pop_actual, state.pop))

        # Validate nobody got lost!
        err = 0.01
        assert abs(self.get_total_us_population() - self.get_total_us_population_actual()) < err

    def assign_house_seats_theory(self):

        ideal = self.get_total_us_population() / self.no_voting_house_seats
        print("Ideal size: %f" % ideal)

        i_try = 0
        no_tries_max = 100

        no_voting_house_seats_assigned = 0
        while (no_voting_house_seats_assigned != self.no_voting_house_seats) and (i_try < no_tries_max):

            for st, state in self.states.items():
            
                state.no_reps_ideal = state.pop / ideal

            for st, state in self.states.items():

                # Minimum of 1
                if state.no_reps_ideal < 1:
                    state.no_reps_assigned = 1
                    continue

                lower = int(state.no_reps_ideal)
                upper = lower + 1
                harmonic_ave = harmonic_mean(lower, upper)

                if state.no_reps_ideal < harmonic_ave:
                    no_seats = lower
                elif state.no_reps_ideal > harmonic_ave:
                    no_seats = upper
                else:
                    raise ValueError("Something went wrong!")

                state.no_reps_assigned = no_seats
                # print("Rounded %f  UP  to %d based on harmonic mean %f" % (ideal_no, upper, harmonic_ave))

            no_voting_house_seats_assigned = sum([state.no_reps_assigned for state in self.states.values()])
            # print(no_voting_house_seats_assigned)

            if no_voting_house_seats_assigned == self.no_voting_house_seats:
                # Done!
                print("Adjusted ideal size: %f" % ideal)
                return

            else:
                # Adjust the ideal fraction!
                ideal_old = ideal

                if no_voting_house_seats_assigned > self.no_voting_house_seats:
                    # Tune up
                    ideal *= 1.0001
                elif no_voting_house_seats_assigned < self.no_voting_house_seats:
                    # Tune down
                    ideal *= 0.9999

                print("Try: %d assigned: %d Adjusted ideal: %f to %f" % (i_try,no_voting_house_seats_assigned,ideal_old,ideal))

                i_try += 1

    def assign_house_seats_priority(self):

        no_voting_house_seats_assigned = 0

        # Assign each state mandatory 1 delegate
        for state in self.states.values():
            state.no_reps_assigned = 1
            no_voting_house_seats_assigned += 1

        # Assign the remaining using priorities
        st_all = [st for st in St]
        while no_voting_house_seats_assigned < self.no_voting_house_seats:

            # Find the highest priority
            priorities = [self.states[st].get_priority() for st in st_all]
            idx = np.argmax(priorities)
            st_assign = st_all[idx]

            # print("Seat: %d state: %s priority: %f" % (no_voting_house_seats_assigned, st_assign, priorities[idx]))

            # Assign
            self.states[st_assign].no_reps_assigned += 1
            no_voting_house_seats_assigned += 1
