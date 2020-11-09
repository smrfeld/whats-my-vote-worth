from .state import State, St, harmonic_mean
import logging
import numpy as np
from typing import Tuple

class States:

    def __init__(self):

        self.no_voting_house_seats = 435
        self.no_electoral_votes_actual = 538

        self.states = {}
        for st in St:
            self.states[st] = State.actual(st)

        # Logging
        handlerPrint = logging.StreamHandler()
        handlerPrint.setLevel(logging.DEBUG)
        self.log = logging.getLogger("states")
        self.log.addHandler(handlerPrint)
        self.log.setLevel(logging.DEBUG)

    def validate_no_reps_matches_actual(self):
        for state in self.states.values():
            state.validate_no_reps_matches_actual()

    def validate_no_electoral_votes_matches_actual(self):
        no_electoral_votes = self.get_no_electoral_votes()
        assert no_electoral_votes == self.no_electoral_votes_actual

    def get_biggest_vote_frac(self) -> Tuple[int,St]:
        st_all = [st for st in St]
        vote_fracs = [self.states[st].frac_vote for st in st_all]
        idx = np.argmax(vote_fracs)
        return (vote_fracs[idx], st_all[idx])

    def get_smallest_vote_frac(self) -> Tuple[int,St]:
        st_all = [st for st in St]
        vote_fracs = [self.states[st].frac_vote for st in st_all]
        idx = np.argmin(vote_fracs)
        return (vote_fracs[idx], st_all[idx])

    def get_no_electoral_votes(self) -> int:
        
        # Check no electoral college votes
        no_electoral_votes = sum([state.get_no_electoral_votes() for state in self.states.values()])
                
        self.log.debug("No electoral votes: %d" % no_electoral_votes)
        return no_electoral_votes

    def get_total_us_population(self) -> float:
        total_us_population = sum(self.states[state].pop for state in St)
        self.log.debug("US population: %f" % total_us_population)
        return total_us_population

    def get_total_us_population_excluding_DC(self) -> float:
        total_us_population_excluding_DC = sum(self.states[st].pop for st in St if st != St.DISTRICT_OF_COLUMBIA)
        self.log.debug("US population excluding DC: %f" % total_us_population_excluding_DC)
        return total_us_population_excluding_DC

    def get_total_us_population_actual(self) -> float:
        total_us_population_actual = sum(self.states[state].pop_actual for state in St)
        self.log.debug("US population actual: %f" % total_us_population_actual)
        return total_us_population_actual

    def get_total_us_population_excluding_DC_actual(self) -> float:
        total_us_population_excluding_DC_actual = sum(self.states[st].pop_actual for st in St if st != St.DISTRICT_OF_COLUMBIA)
        self.log.debug("US population excluding DC actual: %f" % total_us_population_excluding_DC_actual)
        return total_us_population_excluding_DC_actual

    def calculate_state_vote_fracs(self):
        
        total_us_population = self.get_total_us_population()
        no_electoral_votes = self.get_no_electoral_votes()

        # Fraction
        self.log.debug("----- State vote fracs -----")
        for state in self.states.values():
            state.frac_electoral = state.get_no_electoral_votes() / no_electoral_votes
            state.frac_vote = state.frac_electoral * (total_us_population / state.pop)

            self.log.debug("State: %25s frac electoral: %.5f frac vote: %.5f" % 
                (state.st, state.frac_electoral, state.frac_vote))
        self.log.debug("----------")

    def reset_state_populations_to_actual(self):
        for state in self.states.values():
            state.pop = state.pop_actual

    def shift_population_from_state_to_entire_us(self, st_from : St, percent : int):
        assert (percent >= 0)
        assert (percent <= 100)

        # No people to remove
        state_from = self.states[st_from]
        no_leave = state_from.pop_actual * percent / 100.0

        # Remove population from this state
        state_from.pop = state_from.pop_actual - no_leave

        # Calculate population fracs for all the other states
        total_other_population = sum([state.pop_actual for state in self.states.values() if state.st != st_from])
        for st_other, state_other in self.states.items():
            if st_from == st_other:
                continue # skip

            frac = state_other.pop_actual / total_other_population

            # Increment population of other states
            state_other.pop = state_other.pop_actual + frac * no_leave

        self.log.debug("----------")
        self.log.debug("Populations after: %f million people move from: %s to entire US" % (no_leave, st_from))
        for state in self.states.values():
            self.log.debug("%20s : %.5f -> %.5f" % (state.st, state.pop_actual, state.pop))
        self.log.debug("----------")

        # Validate nobody got lost!
        err = 0.01
        assert abs(self.get_total_us_population() - self.get_total_us_population_actual()) < err

    def shift_population_from_entire_us_to_state(self, st_to : St, percent : int):
        assert (percent >= 0)
        assert (percent <= 100)

        total_other_population = sum([state.pop_actual for state in self.states.values() if state.st != st_to])
        no_leave = total_other_population * percent / 100.0

        # Add population to this state
        state_to = self.states[st_to]
        state_to.pop = state_to.pop_actual + no_leave

        # Calculate population fracs for all the other states
        for st_other, state_other in self.states.items():
            if st_to == st_other:
                continue # skip

            frac = state_other.pop_actual / total_other_population

            # Increment population of other states
            state_other.pop = state_other.pop_actual - frac * no_leave

        self.log.debug("----------")
        self.log.debug("Populations after: %f million people move from entire US to: %s" % (no_leave, st_to))
        for state in self.states.values():
            self.log.debug("%20s : %.5f -> %.5f" % (state.st, state.pop_actual, state.pop))
        self.log.debug("----------")

        # Validate nobody got lost!
        err = 0.01
        assert abs(self.get_total_us_population() - self.get_total_us_population_actual()) < err

    def shift_population_from_state_to_state(self, st_from : St, st_to : St, percent : int):
        assert (percent >= 0)
        assert (percent <= 100)

        state_from = self.states[st_from]
        state_to = self.states[st_to]

        # No people to remove
        no_leave = state_from.pop_actual * percent / 100.0

        # Remove population from this state
        state_from.pop = state_from.pop_actual - no_leave
        state_to.pop = state_to.pop_actual + no_leave

        self.log.debug("----------")
        self.log.debug("Populations after: %f million people move from: %s to: %s" % (no_leave, st_from, st_to))
        self.log.debug("%20s : %.5f -> %.5f" % (state_from.st, state_from.pop_actual, state_from.pop))
        self.log.debug("%20s : %.5f -> %.5f" % (state_to.st, state_to.pop_actual, state_to.pop))
        self.log.debug("----------")

        # Validate nobody got lost!
        err = 0.01
        assert abs(self.get_total_us_population() - self.get_total_us_population_actual()) < err

    def assign_house_seats_theory(self):

        ideal = self.get_total_us_population_excluding_DC() / self.no_voting_house_seats
        self.log.debug("Ideal size: %f" % ideal)

        i_try = 0
        no_tries_max = 100

        no_voting_house_seats_assigned = 0
        while (no_voting_house_seats_assigned != self.no_voting_house_seats) and (i_try < no_tries_max):

            for state in self.states.values():

                if state.st == St.DISTRICT_OF_COLUMBIA:
                    state.no_nonvoting_reps_assigned = 1
                    state.no_voting_reps_assigned = 0
                    continue

                # All other states only have voting reps
                state.no_nonvoting_reps_assigned = 0

                # Ideal
                no_reps_ideal = state.pop / ideal

                # Minimum of 1
                if no_reps_ideal < 1:
                    state.no_voting_reps_assigned = 1
                    continue

                lower = int(no_reps_ideal)
                upper = lower + 1
                harmonic_ave = harmonic_mean(lower, upper)

                if no_reps_ideal < harmonic_ave:
                    no_seats = lower
                elif no_reps_ideal > harmonic_ave:
                    no_seats = upper
                else:
                    self.log.error("Something went wrong!")
                    continue

                state.no_voting_reps_assigned = no_seats
                # self.log.debug("Rounded %f  UP  to %d based on harmonic mean %f" % (ideal_no, upper, harmonic_ave))

            no_voting_house_seats_assigned = sum([state.no_voting_reps_assigned for state in self.states.values()])
            # self.log.debug(no_voting_house_seats_assigned)

            if no_voting_house_seats_assigned == self.no_voting_house_seats:
                # Done!
                self.log.debug("Adjusted ideal size: %f" % ideal)
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

                self.log.debug("Try: %d assigned: %d Adjusted ideal: %f to %f" % (
                    i_try,
                    no_voting_house_seats_assigned,
                    ideal_old,
                    ideal))

                i_try += 1

    def assign_house_seats_priority(self):

        no_voting_house_seats_assigned = 0

        # Assign each state mandatory 1 delegate
        for state in self.states.values():
            if state.st == St.DISTRICT_OF_COLUMBIA:
                state.no_voting_reps_assigned = 0
                state.no_nonvoting_reps_assigned = 1
            else:
                state.no_voting_reps_assigned = 1
                state.no_nonvoting_reps_assigned = 0
                no_voting_house_seats_assigned += 1

        # Assign the remaining using priorities
        st_all = [st for st in St if st != St.DISTRICT_OF_COLUMBIA]
        while no_voting_house_seats_assigned < self.no_voting_house_seats:

            # Find the highest priority
            priorities = [self.states[st].get_priority() for st in st_all]
            idx = np.argmax(priorities)
            st_assign = st_all[idx]

            # self.log.debug("Seat: %d state: %s priority: %f" % (no_voting_house_seats_assigned, st_assign, priorities[idx]))

            # Assign
            self.states[st_assign].no_voting_reps_assigned += 1
            no_voting_house_seats_assigned += 1
