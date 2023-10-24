from src.wrappers.OsipiBase import OsipiBase
from src.original.OGC_AmsterdamUMC.LSQ_fitting import flat_neg_log_prior, fit_bayesian
import numpy as np

class OGC_AmsterdamUMC_Bayesian_biexp(OsipiBase):
    """
    Bayesian Bi-exponential fitting algorithm by Oliver Gurney-Champion, Amsterdam UMC
    """

    # I'm thinking that we define default attributes for each submission like this
    # And in __init__, we can call the OsipiBase control functions to check whether
    # the user inputs fulfil the requirements

    # Some basic stuff that identifies the algorithm
    id_author = "Oliver Gurney Champion, Amsterdam UMC"
    id_algorithm_type = "Bi-exponential fit"
    id_return_parameters = "f, D*, D, S0"
    id_units = "seconds per milli metre squared or milliseconds per micro metre squared"

    # Algorithm requirements
    required_bvalues = 4
    required_thresholds = [0,
                           0]  # Interval from "at least" to "at most", in case submissions allow a custom number of thresholds
    required_bounds = False
    required_bounds_optional = True  # Bounds may not be required but are optional
    required_initial_guess = False
    required_initial_guess_optional = True
    accepted_dimensions = 1  # Not sure how to define this for the number of accepted dimensions. Perhaps like the thresholds, at least and at most?

    def __init__(self, bvalues=None, bounds=([0, 0, 0.005, 0.7],[0.005, 0.7, 0.2, 1.3]), initial_guess=None, fitS0=True, thresholds=None):
        """
            Everything this algorithm requires should be implemented here.
            Number of segmentation thresholds, bounds, etc.

            Our OsipiBase object could contain functions that compare the inputs with
            the requirements.
        """
        super(OGC_AmsterdamUMC_Bayesian_biexp, self).__init__(bvalues, bounds,initial_guess,fitS0)
        if bounds is None:
            self.bounds=([0, 0, 0.005, 0.7],[0.005, 1.0, 0.2, 1.3])
        else:
            self.bounds=bounds
        self.neg_log_prior=flat_neg_log_prior([self.bounds[0][0],self.bounds[1][0]],[self.bounds[0][1],self.bounds[1][1]],[self.bounds[0][2],self.bounds[1][2]],[self.bounds[0][3],self.bounds[1][3]])
        self.OGC_algorithm = fit_bayesian
        if initial_guess is None:
            self.initial_guess = [0.001, 0.001, 0.01, 1]
        else:
            self.initial_guess = initial_guess
        self.fitS0=fitS0

    def ivim_fit(self, signals, bvalues=None):
        """Perform the IVIM fit

        Args:
            signals (array-like)
            bvalues (array-like, optional): b-values for the signals. If None, self.bvalues will be used. Default is None.

        Returns:
            _type_: _description_
        """
        bvalues=np.array(bvalues)
        fit_results = self.OGC_algorithm(bvalues, signals, self.neg_log_prior, x0=self.initial_guess, fitS0=self.fitS0)

        D = fit_results[0]
        f = fit_results[1]
        Dstar = fit_results[2]

        return f, Dstar, D