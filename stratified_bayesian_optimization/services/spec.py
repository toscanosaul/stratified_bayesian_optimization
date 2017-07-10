from __future__ import absolute_import

from stratified_bayesian_optimization.initializers.log import SBOLog
from stratified_bayesian_optimization.entities.run_spec import RunSpecEntity
from stratified_bayesian_optimization.lib.constant import DEFAULT_RANDOM_SEED

logger = SBOLog(__name__)


class SpecService(object):
    @classmethod
    def generate_dict_spec(cls, problem_name, dim_x, bounds_domain_x, training_name, type_kernel,
                           dimensions, bounds_domain=None, number_points_each_dimension=None,
                           choose_noise=True, method_optimization='SBO', type_bounds=None,
                           n_training=10, points=None, noise=False, n_samples=0,
                           random_seed=DEFAULT_RANDOM_SEED, parallel=True,
                           name_model='gp_fitting_gaussian', mle=True, thinning=0, n_burning=0,
                           max_steps_out=1, training_data=None):
        """
        Generate dict that represents run spec.

        :param problem_name: (str)
        :param dim_x: int
        :param bounds_domain_x: [(float, float)]
        :param training_name: (str) Prefix for the file of the training data
        :param type_kernel: [str] Must be in possible_kernels. If it's a product of kernels it
            should be a list as: [PRODUCT_KERNELS_SEPARABLE, NAME_1_KERNEL, NAME_2_KERNEL].
            If we want to use a scaled NAME_1_KERNEL, the parameter must be
            [SCALED_KERNEL, NAME_1_KERNEL].
        :param dimensions: [int]. It has only the n_tasks for the task_kernels, and for the
            PRODUCT_KERNELS_SEPARABLE contains the dimensions of every kernel in the product, and
            the total dimension of the product_kernels_separable too in the first entry.
        :param bounds_domain: [([float, float] or [float])], the first case is when the bounds are
            lower or upper bound of the respective entry; in the second case, it's list of finite
            points representing the domain of that entry.
        :param number_points_each_dimension: [int] number of points in each dimension for the
            discretization of the domain of x.
        :param choose_noise: boolean
        :param method_optimization: (str) Options: 'SBO', 'KG'
        :param type_bounds: [0 or 1], 0 if the bounds are lower or upper bound of the respective
            entry, 1 if the bounds are all the finite options for that entry.
        :param n_training: (int) number of training points
        :param points: [[float]], the objective function is evaluated on these points to generate
            the training data.
        :param noise: boolean, true if the evaluations are noisy
        :param n_samples: (int),  If noise is true, we take n_samples of the function to estimate
            its value.
        :param random_seed: (int)
        :param parallel: (boolean) Train in parallel if it's True.
        :param name_model: str
        :param mle: (boolean) If true, fits the GP by MLE.
        :param thinning: (int)
        :param n_burning: (int) Number of burnings samples for the MCMC.
        :param max_steps_out: (int)  Maximum number of steps out for the stepping out  or
                doubling procedure in slice sampling.
        :param training_data: {'points': [[float]], 'evaluations': [float],
            'var_noise': [float] or None}

        :return: dict
        """

        if bounds_domain is None:
            bounds_domain = [[bound[0], bound[1]] for bound in bounds_domain_x]

        if number_points_each_dimension is None:
            number_points_each_dimension = [10] * dim_x

        if type_bounds is None:
            type_bounds = [0] * len(bounds_domain)

        if points is None:
            points = []

        if training_data is None:
            training_data = []

        return {
            'problem_name': problem_name,
            'dim_x': dim_x,
            'choose_noise': choose_noise,
            'bounds_domain_x': bounds_domain_x,
            'number_points_each_dimension': number_points_each_dimension,
            'method_optimization': method_optimization,
            'training_name': training_name,
            'bounds_domain': bounds_domain,
            'n_training': n_training,
            'points': points,
            'noise': noise,
            'n_samples': n_samples,
            'random_seed': random_seed,
            'parallel': parallel,
            'type_bounds': type_bounds,
            'type_kernel': type_kernel,
            'dimensions': dimensions,
            'name_model': name_model,
            'mle': mle,
            'thinning': thinning,
            'n_burning': n_burning,
            'max_steps_out': max_steps_out,
            'training_data': training_data,
        }

    # TODO - generate a list of runspecentities over different parameters

    @classmethod
    def generate_dict_multiple_spec(cls, n_specs, problem_names, dim_xs, bounds_domain_xs,
                                    training_names, type_kernels, dimensionss, bounds_domains=None,
                                    number_points_each_dimensions=None, choose_noises=None,
                                    method_optimizations=None, type_boundss=None, n_trainings=None,
                                    pointss=None, noises=None, n_sampless=None, random_seeds=None,
                                    parallels=None, name_models=None, mles=None, thinnings=None,
                                    n_burnings=None, max_steps_outs=None, training_datas=None):
        """
        Generate dict that represents multiple run specs

        :param n_specs: (int) number of specifications
        :param problem_names: [str]
        :param dim_xs: [int]
        :param bounds_domain_xs: [[(float, float)]]
        :param training_names: ([str]) Prefix for the file of the training data
        :param type_kernels: [[str]] Must be in possible_kernels. If it's a product of kernels it
            should be a list as: [PRODUCT_KERNELS_SEPARABLE, NAME_1_KERNEL, NAME_2_KERNEL].
            If we want to use a scaled NAME_1_KERNEL, the parameter must be
            [SCALED_KERNEL, NAME_1_KERNEL].
        :param dimensionss: [[int]]. It has only the n_tasks for the task_kernels, and for the
            PRODUCT_KERNELS_SEPARABLE contains the dimensions of every kernel in the product, and
            the total dimension of the product_kernels_separable too in the first entry.
        :param bounds_domains: [[([float, float] or [float])]], the first case is when the bounds
            are lower or upper bound of the respective entry; in the second case, it's list of
            finite points representing the domain of that entry.
        :param number_points_each_dimensions: [[int]] number of points in each dimension for the
            discretization of the domain of x.
        :param choose_noises: [boolean]
        :param method_optimizations: [(str)] Options: 'SBO', 'KG'
        :param type_boundss: [[0 or 1]], 0 if the bounds are lower or upper bound of the respective
            entry, 1 if the bounds are all the finite options for that entry.
        :param n_trainings: ([int]) number of training points
        :param pointss: [[[float]]], the objective function is evaluated on these points to generate
            the training data.
        :param noises: [boolean], true if the evaluations are noisy
        :param n_sampless: ([int]),  If noise is true, we take n_samples of the function to estimate
            its value.
        :param random_seeds: ([int])
        :param parallels: ([boolean]) Train in parallel if it's True.
        :param name_models: [str]
        :param mles: ([boolean]) If true, fits the GP by MLE.
        :param thinnings: [int]
        :param n_burnings: ([int]) Number of burnings samples for the MCMC.
        :param max_steps_outs: ([int])  Maximum number of steps out for the stepping out  or
                doubling procedure in slice sampling.
        :param training_datas: [{'points': [[float]], 'evaluations': [float],
            'var_noise': [float] or None}]

        :return: dict
        """

        if name_models is None:
            name_models = ['gp_fitting_gaussian']

        if mles is None:
            mles = [True]

        if thinnings is None:
            thinnings = [0]

        if n_burnings is None:
            n_burnings = [0]

        if max_steps_outs is None:
            max_steps_outs = [1]

        if training_datas is None:
            training_datas = [[]]

        if choose_noises is None:
            choose_noises = [True]

        if method_optimizations is None:
            method_optimizations = ['SBO']

        if n_trainings is None:
            n_trainings = [10]

        if noises is None:
            noises = [False]

        if n_sampless is None:
            n_sampless = [0]

        if parallels is None:
            parallels = [True]

        if random_seeds is None:
            random_seeds = [DEFAULT_RANDOM_SEED]

        if bounds_domains is None:
            bounds_domains = []
            for bounds_domain_x in bounds_domain_xs:
                bounds_domains.append([[bound[0], bound[1]] for bound in bounds_domain_x])

        if number_points_each_dimensions is None:
            number_points_each_dimensions = []
            for dim_x in dim_xs:
                number_points_each_dimensions.append(dim_x * [10])

        if len(choose_noises) != n_specs:
            choose_noises = n_specs * choose_noises

        if len(method_optimizations) != n_specs:
            method_optimizations = n_specs * method_optimizations

        if type_boundss is None:
            type_boundss = []
            for bounds_domain in bounds_domains:
                type_boundss.append(len(bounds_domain) * [0])

        if len(n_trainings) != n_specs:
            n_trainings = n_specs * n_trainings

        if pointss is None:
            pointss = n_specs * [[]]

        if len(noises) != n_specs:
            noises = n_specs * noises

        if len(n_sampless) != n_specs:
            n_sampless = n_specs * n_sampless

        if len(random_seeds) != n_specs:
            random_seeds = n_specs * random_seeds

        if len(parallels) != n_specs:
            parallels = n_specs * parallels

        if len(type_kernels) != n_specs:
            type_kernels = n_specs * type_kernels

        if len(dimensionss) != n_specs:
            dimensionss = n_specs * dimensionss

        if len(name_models) != n_specs:
            name_models = n_specs * name_models

        if len(mles) != n_specs:
            mles = n_specs * mles

        if len(thinnings) != n_specs:
            thinnings = n_specs * thinnings

        if len(n_burnings) != n_specs:
            n_burnings = n_specs * n_burnings

        if len(max_steps_outs) != n_specs:
            max_steps_outs = n_specs * max_steps_outs

        if len(training_datas) != n_specs:
            training_datas = n_specs * training_datas

        return {
            'problem_names': problem_names,
            'dim_xs': dim_xs,
            'bounds_domain_xs': bounds_domain_xs,
            'training_names': training_names,
            'bounds_domains': bounds_domains,
            'number_points_each_dimensions': number_points_each_dimensions,
            'choose_noises': choose_noises,
            'method_optimizations': method_optimizations,
            'type_boundss': type_boundss,
            'n_trainings': n_trainings,
            'pointss': pointss,
            'noises': noises,
            'n_sampless': n_sampless,
            'random_seeds': random_seeds,
            'parallels': parallels,
            'type_kernels': type_kernels,
            'dimensionss': dimensionss,
            'name_models': name_models,
            'mles': mles,
            'thinnings': thinnings,
            'n_burnings': n_burnings,
            'max_steps_outs': max_steps_outs,
            'training_datas': training_datas
        }

    @classmethod
    def generate_specs(cls, n_specs, multiple_spec):
        """
        Generate a list of RunSpecEntities.

        :param n_specs: (int) Number of specifications
        :param multiple_spec: MultipleSpecEntity

        :return: [RunSpecEntity]
        """

        problem_names = multiple_spec.problem_names
        method_optimizations = multiple_spec.method_optimizations
        dim_xs = multiple_spec.dim_xs
        choose_noises = multiple_spec.choose_noises
        bounds_domain_xs = multiple_spec.bounds_domain_xs
        number_points_each_dimensions = multiple_spec.number_points_each_dimensions

        training_names = multiple_spec.training_names
        bounds_domains = multiple_spec.bounds_domains
        type_boundss = multiple_spec.type_boundss
        n_trainings = multiple_spec.n_trainings

        type_kernels = multiple_spec.type_kernels
        dimensionss = multiple_spec.dimensionss

        name_models = multiple_spec.name_models
        if name_models is None:
            name_models = n_specs * ['gp_fitting_gaussian']

        mles = multiple_spec.mles
        if mles is None:
            mles = n_specs * [True]

        thinnings = multiple_spec.thinnings
        if thinnings is None:
            thinnings = n_specs * [0]

        n_burnings = multiple_spec.n_burnings
        if n_burnings is None:
            n_burnings = n_specs * [0]

        max_steps_outs = multiple_spec.max_steps_outs
        if max_steps_outs is None:
            max_steps_outs = n_specs * [1]

        training_datas = multiple_spec.training_datas
        if training_datas is None:
            training_datas = [n_specs * []]

        pointss = multiple_spec.pointss
        if pointss is None:
            pointss = [n_specs * []]

        noises = multiple_spec.noises
        if noises is None:
            noises = n_specs * [False]

        n_sampless = multiple_spec.n_sampless
        if n_sampless is None:
            n_sampless = n_specs * [0]

        random_seeds = multiple_spec.random_seeds
        if random_seeds is None:
            random_seeds = n_specs * [DEFAULT_RANDOM_SEED]

        parallels = multiple_spec.parallels
        if parallels is None:
            parallels = n_specs * [True]

        run_spec = []

        for problem_name, method_optimization, dim_x, choose_noise, bounds_domain_x, \
            number_points_each_dimension, training_name, bounds_domain, type_bounds, n_training, \
            points, noise, n_samples, random_seed, parallel, type_kernel, dimensions, name_model, \
            mle, thinning, n_burning, max_steps_out, training_data in \
                zip(problem_names, method_optimizations, dim_xs, choose_noises, bounds_domain_xs,
                    number_points_each_dimensions, training_names, bounds_domains, type_boundss,
                    n_trainings, pointss, noises, n_sampless, random_seeds, parallels, type_kernels,
                    dimensionss, name_models, mles, thinnings, n_burnings, max_steps_outs,
                    training_datas):

            parameters_entity = {
                'problem_name': problem_name,
                'method_optimization': method_optimization,
                'dim_x': dim_x,
                'choose_noise': choose_noise,
                'bounds_domain_x': bounds_domain_x,
                'number_points_each_dimension': number_points_each_dimension,
                'training_name': training_name,
                'bounds_domain': bounds_domain,
                'type_bounds': type_bounds,
                'n_training': n_training,
                'points': points,
                'noise': noise,
                'n_samples': n_samples,
                'random_seed': random_seed,
                'parallel': parallel,
                'type_kernel': type_kernel,
                'dimensions': dimensions,
                'name_model': name_model,
                'mle': mle,
                'thinning': thinning,
                'n_burning': n_burning,
                'max_steps_out': max_steps_out,
                'training_data': training_data,
            }

            run_spec.append(RunSpecEntity(parameters_entity))

        return run_spec
