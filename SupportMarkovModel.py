import InputData as Settings
import scr.FormatFunctions as F
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs
import scr.StatisticalClasses as Stat
import scr.EconEvalClasses as Econ


def print_outcomes(simOutput, therapy_name):
    """ prints the outcomes of a simulated cohort
    :param simOutput: output of a simulated cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and confidence interval text of patient survival time
    survival_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_survival_times().get_mean(),
        interval=simOutput.get_sumStat_survival_times().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of time to stroke
    strokes_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_count_strokes().get_mean(),
        interval=simOutput.get_sumStat_count_strokes().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_cost().get_mean(),
        interval=simOutput.get_sumStat_discounted_cost().get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)

    # mean and confidence interval text of discounted total utility
    utility_mean_CI_text = F.format_estimate_interval(
        estimate=simOutput.get_sumStat_discounted_utility().get_mean(),
        interval=simOutput.get_sumStat_discounted_utility().get_t_CI(alpha=Settings.ALPHA),
        deci=2)

    # print outcomes
    print(therapy_name)
    print("  Estimate of mean and {:.{prec}%} confidence interval of survival time:".format(1 - Settings.ALPHA, prec=0),
          survival_mean_CI_text)
    print("  Estimate of mean and {:.{prec}%} confidence interval of time to stroke:".format(1 - Settings.ALPHA, prec=0),
          strokes_mean_CI_text)
    print("")
    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          utility_mean_CI_text)
    print("")

def draw_survival_curves_and_histograms(simOutputs_none, simOutputs_anticoag):
        """ draws the survival curves and the histograms of time until death
        :param simOutputs_none: output of a cohort simulated under no therapy
        :param simOutputs_anticoag: output of a cohort simulated under anticoagulation therapy
        """

        # get survival curves of both treatments
        survival_curves = [
            simOutputs_none.get_survival_curve(),
            simOutputs_anticoag.get_survival_curve()
        ]

        # graph survival curve
        PathCls.graph_sample_paths(
            sample_paths=survival_curves,
            title='Survival curve',
            x_label='Simulation time step (year)',
            y_label='Number of alive patients',
            legends=['No Therapy', 'Anticoagulation Therapy']
        )

        # histograms of survival times
        set_of_survival_times = [
            simOutputs_none.get_survival_times(),
            simOutputs_anticoag.get_survival_times()
        ]

        # graph histograms
        Figs.graph_histograms(
            data_sets=set_of_survival_times,
            title='Histogram of patient survival time',
            x_label='Survival time (year)',
            y_label='Counts',
            bin_width=1,
            legend=['No Therapy', 'Anticoagulation Therapy'],
            transparency=0.6
        )

def print_comparative_outcomes(simOutputs_none, simOutputs_anticoag):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param simOutputs_none: output of a cohort simulated under mono therapy
    :param simOutputs_anticoag: output of a cohort simulated under combination therapy
    """

    # increase in survival time under combination therapy with respect to mono therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in survival time',
        x=simOutputs_anticoag.get_survival_times(),
        y_ref=simOutputs_none.get_survival_times())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_survival_time.get_mean(),
        interval=increase_survival_time.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in survival time "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
           estimate_CI)

    # increase in discounted total cost under combination therapy with respect to mono therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_anticoag.get_costs(),
        y_ref=simOutputs_none.get_costs())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_cost.get_mean(),
        interval=increase_discounted_cost.get_t_CI(alpha=Settings.ALPHA),
        deci=0,
        form=F.FormatNumber.CURRENCY)
    print("Average increase in discounted cost "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

    # increase in discounted total utility under combination therapy with respect to mono therapy
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in discounted cost',
        x=simOutputs_anticoag.get_utilities(),
        y_ref=simOutputs_none.get_utilities())

    # estimate and CI
    estimate_CI = F.format_estimate_interval(
        estimate=increase_discounted_utility.get_mean(),
        interval=increase_discounted_utility.get_t_CI(alpha=Settings.ALPHA),
        deci=2)
    print("Average increase in discounted utility "
          "and {:.{prec}%} confidence interval:".format(1 - Settings.ALPHA, prec=0),
          estimate_CI)

def report_CEA_CBA(simOutputs_none, simOutputs_anticoag):
    """ performs cost-effectiveness analysis
    :param simOutputs_none: output of a cohort simulated under mono therapy
    :param simOutputs_anticoag: output of a cohort simulated under combination therapy
        """

    # define two strategies
    no_therapy_strategy = Econ.Strategy(
        name='No Therapy',
        cost_obs=simOutputs_none.get_costs(),
        effect_obs=simOutputs_none.get_utilities()
     )
    anticoag_therapy_strategy = Econ.Strategy(
        name='Combination Therapy',
        cost_obs=simOutputs_anticoag.get_costs(),
        effect_obs=simOutputs_anticoag.get_utilities()
    )

    # CEA
    CEA = Econ.CEA(
        strategies=[no_therapy_strategy, anticoag_therapy_strategy],
        if_paired=False
        )
    # show the CE plane
    CEA.show_CE_plane(
        title='Cost-Effectiveness Analysis',
        x_label='Additional discounted utility',
        y_label='Additional discounted cost',
        show_names=True,
        show_clouds=True,
        show_legend=True,
        figure_size=6,
        transparency=0.3
    )
    # report the CE table
    CEA.build_CE_table(
        interval=Econ.Interval.CONFIDENCE,
        alpha=Settings.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2,
    )

    # CBA
    NBA = Econ.CBA(
        strategies=[no_therapy_strategy, anticoag_therapy_strategy],
        if_paired=False
        )
    # show the net monetary benefit figure
    NBA.graph_deltaNMB_lines(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval=Econ.Interval.CONFIDENCE,
        show_legend=True,
        figure_size=6
    )
