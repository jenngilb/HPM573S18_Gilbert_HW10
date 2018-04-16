import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov


# simulating no therapy
# create a cohort
cohort_none = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)
# simulate the cohort
simOutputs_none = cohort_none.simulate()

# simulating anticoagulation therapy
# create a cohort
cohort_anticoag = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.ANTICOAG)
# simulate the cohort
simOutputs_anticoag = cohort_anticoag.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_none, simOutputs_anticoag)

# print the estimates for the mean survival time and mean time to Stroke
SupportMarkov.print_outcomes(simOutputs_none, "No Therapy:")
SupportMarkov.print_outcomes(simOutputs_anticoag, "Anticoagulation Therapy:")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_none, simOutputs_anticoag)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_none, simOutputs_anticoag)

