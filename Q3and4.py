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

SupportMarkov.report_CEA_CBA(simOutputs_none, simOutputs_anticoag)

print("")
print("Question 4")
print("")
print("I recommend adopting this anticoagulation drug when people are willing to pay ~$23K and above")
