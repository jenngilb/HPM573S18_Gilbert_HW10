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

SupportMarkov.print_comparative_outcomes(simOutputs_none, simOutputs_anticoag)
