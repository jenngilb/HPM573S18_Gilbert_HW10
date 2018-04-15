import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov


# simulating mono therapy
# create a cohort
cohort_mono = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)
# simulate the cohort
simOutputs_mono = cohort_mono.simulate()

# simulating combination therapy
# create a cohort
cohort_combo = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.ANTICOAG)
# simulate the cohort
simOutputs_combo = cohort_combo.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_mono, simOutputs_combo)

# print the estimates for the mean survival time and mean time to AIDS
SupportMarkov.print_outcomes(simOutputs_mono, "Hmwk q2: No Therapy:")
SupportMarkov.print_outcomes(simOutputs_combo, "Hmwk q2: Anticoagulation Therapy:")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_mono, simOutputs_combo)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_mono, simOutputs_combo)
