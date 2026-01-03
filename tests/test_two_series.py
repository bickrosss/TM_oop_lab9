#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import pytest
from series_two_series import (
    calculate_series_1, 
    calculate_series_2,
    get_control_value_1,
    get_control_value_2
)


@pytest.mark.parametrize(
    "x, eps",
    [
        (0.35, 1e-7),
        (0.5, 1e-8),
        (0.2, 1e-6),
    ],
)
def test_calculate_series_1_accuracy(x: float, eps: float) -> None:
    """Тест точности вычисления первого ряда."""
    total_sum, total_count = calculate_series_1(x, eps, num_processes=4)
    control_value: float = get_control_value_1(x)
    error: float = abs(total_sum - control_value)

    assert error < eps, f"Ошибка {error} превышает eps={eps}"
    assert total_count > 0, f"Ряд не сошелся, учтено членов: {total_count}"


@pytest.mark.parametrize(
    "x, eps",
    [
        (2.0, 1e-7),
        (3.0, 1e-8),
        (1.5, 1e-6),
    ],
)
def test_calculate_series_2_accuracy(x: float, eps: float) -> None:
    """Тест точности вычисления второго ряда."""
    total_sum, total_count = calculate_series_2(x, eps, num_processes=4)
    control_value: float = get_control_value_2(x)
    error: float = abs(total_sum - control_value)

    assert error < eps, f"Ошибка {error} превышает eps={eps}"
    assert total_count > 0, f"Ряд не сошелся, учтено членов: {total_count}"


def test_control_values_known() -> None:
    """Тест контрольных значений для известных точек."""
    # Первый ряд
    x1: float = 0.35
    expected1: float = 0.5 * math.log((1 + x1) / (1 - x1))
    assert math.isclose(get_control_value_1(x1), expected1, rel_tol=1e-12)
    
    # Второй ряд
    x2: float = 2.0
    expected2: float = 0.5 * math.log((x2 + 1) / (x2 - 1))
    assert math.isclose(get_control_value_2(x2), expected2, rel_tol=1e-12)


def test_series_convergence() -> None:
    """Тест на сходимость рядов."""
    # Первый ряд
    x1 = 0.5
    sum1_coarse, _ = calculate_series_1(x1, 1e-4, num_processes=4)
    sum1_fine, _ = calculate_series_1(x1, 1e-8, num_processes=4)
    control1: float = get_control_value_1(x1)
    
    # Второй ряд
    x2 = 2.0
    sum2_coarse, _ = calculate_series_2(x2, 1e-4, num_processes=4)
    sum2_fine, _ = calculate_series_2(x2, 1e-8, num_processes=4)
    control2: float = get_control_value_2(x2)
    
    assert abs(sum1_fine - control1) < abs(sum1_coarse - control1)
    assert abs(sum2_fine - control2) < abs(sum2_coarse - control2)


def test_multiprocessing_effect() -> None:
    """Тест влияния количества процессов на результат."""
    x = 0.35
    eps = 1e-7
    
    # Первый ряд
    sum1_2proc, count1_2proc = calculate_series_1(x, eps, num_processes=2)
    sum1_4proc, count1_4proc = calculate_series_1(x, eps, num_processes=4)
    control1 = get_control_value_1(x)
    
    # Второй ряд
    x2 = 2.0
    sum2_2proc, count2_2proc = calculate_series_2(x2, eps, num_processes=2)
    sum2_4proc, count2_4proc = calculate_series_2(x2, eps, num_processes=4)
    control2 = get_control_value_2(x2)
    
    # Проверяем, что результаты совпадают независимо от количества процессов
    assert math.isclose(sum1_2proc, sum1_4proc, rel_tol=1e-10)
    assert math.isclose(sum2_2proc, sum2_4proc, rel_tol=1e-10)
