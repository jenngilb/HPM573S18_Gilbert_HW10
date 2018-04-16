import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create and cohort
cohortNoTherapy = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.NONE)

simOutputs_none = cohortNoTherapy.simulate()


# create and cohort
cohortAnticoagTherapy = MarkovCls.Cohort(
    id=1,
    therapy=P.Therapies.ANTICOAG)

simOutputs_anticoag = cohortAnticoagTherapy.simulate()

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs_anticoag, 'No treatment:')

# print outcomes (means and CIs)
SupportMarkov.print_outcomes(simOutputs_anticoag, 'Anticoagulation treatment:')
