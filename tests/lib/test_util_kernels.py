from __future__ import absolute_import

import unittest

from stratified_bayesian_optimization.lib.util_kernels import (
    find_define_kernel_from_array,
    find_kernel_constructor,
)
from stratified_bayesian_optimization.lib.constant import (
    MATERN52_NAME,
    TASKS_KERNEL_NAME,
)
from stratified_bayesian_optimization.kernels.matern52 import Matern52
from stratified_bayesian_optimization.kernels.tasks_kernel import TasksKernel


class TestUtilKernels(unittest.TestCase):

    def test_find_define_kernel_from_array(self):
        assert Matern52.define_kernel_from_array == find_define_kernel_from_array(MATERN52_NAME)
        assert TasksKernel.define_kernel_from_array == find_define_kernel_from_array(
            TASKS_KERNEL_NAME)
        with self.assertRaises(NameError):
            find_define_kernel_from_array('a')

    def test_find_kernel_constructor(self):
        assert find_kernel_constructor(MATERN52_NAME) == Matern52
        assert find_kernel_constructor(TASKS_KERNEL_NAME) == TasksKernel

        with self.assertRaises(NameError):
            find_kernel_constructor('a')
