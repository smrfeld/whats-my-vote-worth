import numpy as np

from enum import Enum

class St(Enum):
    CALIFORNIA = 1
    TEXAS = 2
    FLORIDA = 3
    NEW_YORK = 4
    PENNSYLVANIA = 5
    ILLINOIS = 6
    OHIO = 7
    GEORGIA = 8
    NORTH_CAROLINA = 9
    MICHIGAN = 10
    NEW_JERSEY = 11
    VIRGINIA = 12
    WASHINGTON = 13
    ARIZONA = 14
    MASSACHUSETTS = 15
    TENNESSEE = 16
    INDIANA = 17
    MISSOURI = 18
    MARYLAND = 19
    WISCONSION = 20
    COLORADO = 21
    MINNESOTA = 22
    SOUTH_CAROLINA = 23
    ALABAMA = 24
    LOUISIANA = 25
    KENTUCKY = 26
    OREGON = 27
    OKLAHOMA = 28
    CONNECTICUT = 29
    UTAH = 30
    IOWA = 31
    NEVADA = 32
    ARKANSAS = 33
    MISSISSIPPI = 34
    KANSAS = 35
    NEW_MEXICO = 36
    NEBRASKA = 37
    WEST_VIRGINIA = 38
    IDAHO = 39
    HAWAII = 40
    NEW_HAMPSHIRE = 41
    MAINE = 42
    MONTANA = 43
    RHODE_ISLAND = 44
    DELAWARE = 45
    SOUTH_DEKOTA = 46
    NORTH_DEKOTA = 47
    ALASKA = 48
    DISTRICT_OF_COLUMBIA = 49
    VERMONT = 50
    WYOMING = 51

def get_label_from_st(st : St) -> str:

    name = str(st)
    name = name.lower()
    name = name[3:]
    
    # Capitalize west virginia -> West Virginia
    words = name.split('_')
    name = ' '.join([n.capitalize() if n != "of" else n for n in words])

    return name

def get_st_from_label(label : str) -> St:
    words = label.split()
    name = '_'.join(words)
    name.capitalize()

    return St[name]

def arithmetic_mean(n : float, m : float) -> float:
    return (n + m) / 2.0

def harmonic_mean(n : float, m : float) -> float:
    return 1.0 / arithmetic_mean(1.0/n, 1.0/m)

def geometric_mean(n : float, m : float) -> float:
    return np.sqrt(n * m)

class State:
    
    def __init__(self, 
        st: St, 
        pop_actual: float, 
        no_voting_reps_actual: int, 
        no_nonvoting_reps_actual: int, 
        abbrev: str
        ):
        self.st : St = st
        self.abbrev : str = abbrev

        self.pop : float = pop_actual
        self.pop_actual : float = pop_actual

        self.no_voting_reps : int = no_voting_reps_actual
        self.no_voting_reps_actual : int = no_voting_reps_actual
        self.no_nonvoting_reps : int = no_nonvoting_reps_actual
        self.no_nonvoting_reps_actual : int = no_nonvoting_reps_actual

        self.no_voting_reps_assigned : int = 0
        self.no_nonvoting_reps_assigned : int = 0
        
        self.frac_vote : float = 0.0
        self.frac_electoral : float = 0.0

    def get_no_electoral_votes(self):
        return self.no_voting_reps_assigned + self.no_nonvoting_reps_assigned + 2

    def get_priority(self):
        harmonic_ave = geometric_mean(self.no_voting_reps_assigned,self.no_voting_reps_assigned+1)
        multiplier = 1.0 / harmonic_ave
        return self.pop * multiplier

    def validate_no_reps_matches_actual(self):
        # Validate that they match the expected
        if self.no_voting_reps_assigned != self.no_voting_reps_actual:
            raise ValueError("State: %s no. voting reps assigned: %d does not match the actual no. reps: %d" % 
                (self.st, self.no_voting_reps_assigned, self.no_voting_reps_actual))
        if self.no_nonvoting_reps_assigned != self.no_nonvoting_reps_actual:
            raise ValueError("State: %s no. nonvoting reps assigned: %d does not match the actual no. reps: %d" % 
                (self.st, self.no_nonvoting_reps_assigned, self.no_nonvoting_reps_actual))

    @classmethod
    def actual(cls, st: St):

        # Population source
        # https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-08.pdf
        # No reps - https://en.wikipedia.org/wiki/United_States_congressional_apportionment

        if st == St.CALIFORNIA:
            pop_actual = 37.341989
            no_voting_reps_actual = 53
            no_nonvoting_reps_actual = 0
            abbrev = "CA"
        elif st == St.TEXAS:
            pop_actual = 25.268418
            no_voting_reps_actual = 36
            no_nonvoting_reps_actual = 0
            abbrev = "TX"
        elif st == St.FLORIDA:
            pop_actual = 18.900773	
            no_voting_reps_actual = 27
            no_nonvoting_reps_actual = 0
            abbrev = "FL"
        elif st == St.NEW_YORK:
            pop_actual = 19.421055
            no_voting_reps_actual = 27
            no_nonvoting_reps_actual = 0
            abbrev = "NY"
        elif st == St.PENNSYLVANIA:
            pop_actual = 12.734905
            no_voting_reps_actual = 18
            no_nonvoting_reps_actual = 0
            abbrev = "PA"
        elif st == St.ILLINOIS:
            pop_actual = 12.864380
            no_voting_reps_actual = 18
            no_nonvoting_reps_actual = 0
            abbrev = "IL"
        elif st == St.OHIO:
            pop_actual = 11.568495
            no_voting_reps_actual = 16
            no_nonvoting_reps_actual = 0
            abbrev = "OH"
        elif st == St.GEORGIA:
            pop_actual = 9.727566
            no_voting_reps_actual = 14
            no_nonvoting_reps_actual = 0
            abbrev = "GA"
        elif st == St.NORTH_CAROLINA:
            pop_actual = 9.565781
            no_voting_reps_actual = 13
            no_nonvoting_reps_actual = 0
            abbrev = "NC"
        elif st == St.MICHIGAN:
            pop_actual = 9.911626
            no_voting_reps_actual = 14
            no_nonvoting_reps_actual = 0
            abbrev = "MI"
        elif st == St.NEW_JERSEY:
            pop_actual = 8.807501
            no_voting_reps_actual = 12
            no_nonvoting_reps_actual = 0
            abbrev = "NJ"
        elif st == St.VIRGINIA:
            pop_actual = 8.037736
            no_voting_reps_actual = 11
            no_nonvoting_reps_actual = 0
            abbrev = "VA"
        elif st == St.WASHINGTON:
            pop_actual = 6.753369	
            no_voting_reps_actual = 10
            no_nonvoting_reps_actual = 0
            abbrev = "WA"
        elif st == St.ARIZONA:
            pop_actual = 6.412700
            no_voting_reps_actual = 9 
            no_nonvoting_reps_actual = 0
            abbrev = "AZ"
        elif st == St.MASSACHUSETTS:
            pop_actual = 6.559644
            no_voting_reps_actual = 9
            no_nonvoting_reps_actual = 0
            abbrev = "MA"
        elif st == St.TENNESSEE:
            pop_actual = 6.375431
            no_voting_reps_actual = 9
            no_nonvoting_reps_actual = 0
            abbrev = "TN"
        elif st == St.INDIANA:
            pop_actual = 6.501582
            no_voting_reps_actual = 9
            no_nonvoting_reps_actual = 0
            abbrev = "IN"
        elif st == St.MISSOURI:
            pop_actual = 6.011478
            no_voting_reps_actual = 8
            no_nonvoting_reps_actual = 0
            abbrev = "MO"
        elif st == St.MARYLAND:
            pop_actual = 5.789929	
            no_voting_reps_actual = 8
            no_nonvoting_reps_actual = 0
            abbrev = "MD"
        elif st == St.WISCONSION:
            pop_actual = 5.698230
            no_voting_reps_actual = 8
            no_nonvoting_reps_actual = 0
            abbrev = "WI"
        elif st == St.COLORADO:
            pop_actual = 5.044930
            no_voting_reps_actual = 7
            no_nonvoting_reps_actual = 0
            abbrev = "CO"
        elif st == St.MINNESOTA:
            pop_actual = 5.314879
            no_voting_reps_actual = 8
            no_nonvoting_reps_actual = 0
            abbrev = "MN"
        elif st == St.SOUTH_CAROLINA:
            pop_actual = 4.645975
            no_voting_reps_actual = 7
            no_nonvoting_reps_actual = 0
            abbrev = "SC"
        elif st == St.ALABAMA:
            pop_actual = 4.802982
            no_voting_reps_actual = 7
            no_nonvoting_reps_actual = 0
            abbrev = "AL"
        elif st == St.LOUISIANA:
            pop_actual = 4.553962
            no_voting_reps_actual = 6
            no_nonvoting_reps_actual = 0
            abbrev = "LA"
        elif st == St.KENTUCKY:
            pop_actual = 4.350606
            no_voting_reps_actual = 6
            no_nonvoting_reps_actual = 0
            abbrev = "KY"
        elif st == St.OREGON:
            pop_actual = 3.848606
            no_voting_reps_actual = 5
            no_nonvoting_reps_actual = 0
            abbrev = "OR"
        elif st == St.OKLAHOMA:
            pop_actual = 3.764882
            no_voting_reps_actual = 5
            no_nonvoting_reps_actual = 0
            abbrev = "OK"
        elif st == St.CONNECTICUT:
            pop_actual = 3.581628
            no_voting_reps_actual = 5
            no_nonvoting_reps_actual = 0
            abbrev = "CT"
        elif st == St.UTAH:
            pop_actual = 2.770765
            no_voting_reps_actual = 4
            no_nonvoting_reps_actual = 0
            abbrev = "UT"
        elif st == St.IOWA:
            pop_actual = 3.053787
            no_voting_reps_actual = 4
            no_nonvoting_reps_actual = 0
            abbrev = "IA"
        elif st == St.NEVADA:
            pop_actual = 2.709432
            no_voting_reps_actual = 4
            no_nonvoting_reps_actual = 0
            abbrev = "NV"
        elif st == St.ARKANSAS:
            pop_actual = 2.926229
            no_voting_reps_actual = 4
            no_nonvoting_reps_actual = 0
            abbrev = "AR"
        elif st == St.MISSISSIPPI:
            pop_actual = 2.978240	
            no_voting_reps_actual = 4
            no_nonvoting_reps_actual = 0
            abbrev = "MS"
        elif st == St.KANSAS:
            pop_actual = 2.863813	
            no_voting_reps_actual = 4
            no_nonvoting_reps_actual = 0
            abbrev = "KS"
        elif st == St.NEW_MEXICO:
            pop_actual = 2.067273
            no_voting_reps_actual = 3
            no_nonvoting_reps_actual = 0
            abbrev = "NM"
        elif st == St.NEBRASKA:
            pop_actual = 1.831825
            no_voting_reps_actual = 3
            no_nonvoting_reps_actual = 0
            abbrev = "NE"
        elif st == St.WEST_VIRGINIA:
            pop_actual = 1.859815
            no_voting_reps_actual = 3
            no_nonvoting_reps_actual = 0
            abbrev ="WV"
        elif st == St.IDAHO:
            pop_actual = 1.573499
            no_voting_reps_actual = 2
            no_nonvoting_reps_actual = 0
            abbrev = "ID"
        elif st == St.HAWAII:
            pop_actual = 1.366862
            no_voting_reps_actual = 2
            no_nonvoting_reps_actual = 0
            abbrev = "HI"
        elif st == St.NEW_HAMPSHIRE:
            pop_actual = 1.321445
            no_voting_reps_actual = 2
            no_nonvoting_reps_actual = 0
            abbrev = "NH"
        elif st == St.MAINE:
            pop_actual = 1.333074
            no_voting_reps_actual = 2
            no_nonvoting_reps_actual = 0
            abbrev = "ME"
        elif st == St.MONTANA:
            pop_actual = 0.994416
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "MT"
        elif st == St.RHODE_ISLAND:
            pop_actual = 1.055247
            no_voting_reps_actual = 2
            no_nonvoting_reps_actual = 0
            abbrev = "RI"
        elif st == St.DELAWARE:
            pop_actual = 0.900877
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "DE"
        elif st == St.SOUTH_DEKOTA:
            pop_actual = 0.819761
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "SD"
        elif st == St.NORTH_DEKOTA:
            pop_actual = 0.675905
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "ND"
        elif st == St.ALASKA:
            pop_actual = 0.721523
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "AK"
        elif st == St.VERMONT:
            pop_actual = 0.630337
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "VT"
        elif st == St.WYOMING:
            pop_actual = 0.568300	
            no_voting_reps_actual = 1
            no_nonvoting_reps_actual = 0
            abbrev = "WY"
        elif st == St.DISTRICT_OF_COLUMBIA:
            pop_actual = 0.601723
            no_voting_reps_actual = 0
            no_nonvoting_reps_actual = 1
            abbrev = "DC"

        else:
            raise ValueError("State not recognized: %s" % st)

        return cls(st, pop_actual, no_voting_reps_actual, no_nonvoting_reps_actual, abbrev)
