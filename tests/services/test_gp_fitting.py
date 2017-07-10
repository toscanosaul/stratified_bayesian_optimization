import unittest

from doubles import expect
import numpy.testing as npt

import numpy as np

from stratified_bayesian_optimization.services.gp_fitting import GPFittingService
from stratified_bayesian_optimization.models.gp_fitting_gaussian import GPFittingGaussian
from stratified_bayesian_optimization.util.json_file import JSONFile
from stratified_bayesian_optimization.lib.constant import (
    MATERN52_NAME,
    PRODUCT_KERNELS_SEPARABLE,
    TASKS_KERNEL_NAME,
    SCALED_KERNEL,
)


class TestGpFitting(unittest.TestCase):

    def setUp(self):
        self.problem_name = 'test_problem'
        self.type_kernel = [PRODUCT_KERNELS_SEPARABLE, TASKS_KERNEL_NAME, MATERN52_NAME]
        self.trainining_name = 'training'

    def test_get_filename(self):
        name = GPFittingService._get_filename(GPFittingGaussian, self.problem_name,
                                              self.type_kernel, self.trainining_name)
        file = 'gp_GPFittingGaussian_test_problem_Product_of_kernels_with_separable_domain_Tasks_' \
               'Kernel_Matern52_training.json'
        assert name == file

    def test_get_gp(self):
        name_model = 'gp_fitting_gaussian'
        dimensions = [1]
        bounds = [[-10, 10]]
        n_training = 30
        points_ = list(np.linspace(-10, 10, n_training))
        points = [[point] for point in points_]

        expect(JSONFile).read.and_return(None)
        gp = GPFittingService.get_gp(name_model, self.problem_name, [SCALED_KERNEL, MATERN52_NAME],
                                     dimensions, bounds, type_bounds=[0], n_training=n_training,
                                     noise=False, points=points, mle=True, random_seed=1)
        model = gp.serialize()

        data = {
            'points': points,
            'var_noise': [],
            'evaluations': points_,
        }

        assert model == {
            'type_kernel': [SCALED_KERNEL, MATERN52_NAME],
            'training_data': data,
            'data': data,
            'dimensions': [1],
            'kernel_values': model['kernel_values'],
            'mean_value': model['mean_value'],
            'var_noise_value': [1e-10],
            'thinning': 0,
            'bounds_domain': bounds,
            'n_burning': 0,
            'max_steps_out': 1,
        }

        estimation = gp.compute_posterior_parameters(np.array([[1.4], [2.4], [0], [-9.9], [8.5],
                                                               [points_[3]]]))

        points_2 = np.array([[1.4], [2.4], [0], [-9.9], [8.5], [points_[3]]]).reshape(6)
        npt.assert_almost_equal(estimation['mean'], points_2, decimal=4)
        npt.assert_almost_equal(estimation['cov'], np.zeros((6, 6)))

    def test_get_gp_cached(self):
        name_model = 'gp_fitting_gaussian'
        dimensions = [1]
        bounds = [[-10, 10]]
        n_training = 30
        points_ = list(np.linspace(-10, 10, n_training))
        points = [[point] for point in points_]

        gp = GPFittingService.get_gp(name_model, self.problem_name, [SCALED_KERNEL, MATERN52_NAME],
                                     dimensions, bounds, type_bounds=[0], n_training=n_training,
                                     noise=False, points=points, mle=True, random_seed=1)

        model = gp.serialize()

        assert model == {
            'type_kernel': [SCALED_KERNEL, MATERN52_NAME],
            'training_data': model['training_data'],
            'data': model['data'],
            'dimensions': [1],
            'kernel_values': model['kernel_values'],
            'mean_value': model['mean_value'],
            'var_noise_value': [1e-10],
            'thinning': 0,
            'bounds_domain': bounds,
            'n_burning': 0,
            'max_steps_out': 1,
        }

    def test_from_dict(self):
        name_model = 'gp_fitting_gaussian'
        dimensions = [1]
        bounds = [[-10, 10]]
        n_training = 30
        points_ = list(np.linspace(-10, 10, n_training))
        points = [[point] for point in points_]

        gp = GPFittingService.get_gp(name_model, self.problem_name, [SCALED_KERNEL, MATERN52_NAME],
                                     dimensions, bounds, type_bounds=[0], n_training=n_training,
                                     noise=False, points=points, mle=True, random_seed=1)

        model = gp.serialize()

        spec = {
            'name_model': name_model,
            'problem_name': self.problem_name,
            'type_kernel': [SCALED_KERNEL, MATERN52_NAME],
            'dimensions': dimensions,
            'bounds_domain': bounds,
            'type_bounds': [0],
            'n_training': n_training,
            'noise': False,
            'points': points,
            'mle': True,
            'random_seed': 1
        }

        gp_2 = GPFittingService.from_dict(spec)

        model_2 = gp_2.serialize()

        assert model == model_2
