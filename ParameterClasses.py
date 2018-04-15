from enum import Enum
import InputData as Data


class HealthStats(Enum):
    """ health states of patients with HIV """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEATH = 3


class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    ANTICOAG = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.WELL

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.NONE:
            self._prob_matrix = Data.TRANS_MATRIX
        else:
            self._prob_matrix = calculate_prob_matrix_anticoag()

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]


def calculate_prob_matrix_anticoag():
    """ :returns transition probability matrix under anticoagulation use"""

    # create an empty matrix populated with zeroes
    prob_matrix = []
    for s in HealthStats:
        prob_matrix.append([0] * len(HealthStats))

    # for all health states
    for s in HealthStats:
        # if the current state is post-stroke
        if s == HealthStats.POST_STROKE:
            # post-stoke to stroke
            prob_matrix[s.value][HealthStats.STROKE.value]\
                = Data.RR_STROKE*Data.TRANS_MATRIX[s.value][HealthStats.STROKE.value]
            # post-stroke to death
            prob_matrix[s.value][HealthStats.DEATH.value] \
                = Data.RR_STROKE * Data .RR_BLEEDING * Data.TRANS_MATRIX[s.value][HealthStats.DEATH.value]
            # staying in post-stroke
            prob_matrix[s.value][s.value]\
                = 1 -prob_matrix[s.value][HealthStats.STROKE.value] -prob_matrix[s.value][HealthStats.DEATH.value]
        else:
            prob_matrix[s.value] = Data.TRANS_MATRIX[s.value]

    return prob_matrix
