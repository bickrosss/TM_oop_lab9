#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from multiprocessing import Manager, Process
from typing import Tuple, Callable


class SeriesProcess(Process):

    def __init__(
        self, 
        x: float, 
        eps: float, 
        start_idx: int, 
        step: int, 
        results: dict, 
        pos: int,
        term_func: Callable[[float, int], float]
    ) -> None:
        super().__init__()
        self.x: float = x
        self.eps: float = eps
        self.start_idx: int = start_idx
        self.step: int = step
        self.results: dict = results
        self.pos: int = pos
        self.term_func = term_func

    def run(self) -> None:
        partial_sum: float = 0.0
        count: int = 0

        n: int = self.start_idx
        prev_term: float = float('inf')
        
        while True:
            term: float = self.term_func(self.x, n)
            if abs(term) < self.eps and abs(term) <= abs(prev_term):
                break
            
            partial_sum += term
            count += 1
            n += self.step
            prev_term = term
            
            if count > 10000:
                break

        self.results[f"sum_{self.pos}"] = partial_sum
        self.results[f"count_{self.pos}"] = count


def calculate_series_1(x: float, eps: float, num_processes: int = 4) -> Tuple[float, int]:
    def term_func_1(x_val: float, n: int) -> float:

        try:
            return (x_val ** (2 * n + 1)) / (2 * n + 1)
        except (OverflowError, ZeroDivisionError):
            return 0.0

    with Manager() as manager:
        results: dict = manager.dict()
        processes: list = []

        for i in range(num_processes):
            p = SeriesProcess(x, eps, i, num_processes, results, i, term_func_1)
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        total_sum: float = sum(results[f"sum_{i}"] for i in range(num_processes))
        total_count: int = sum(results[f"count_{i}"] for i in range(num_processes))

    return total_sum, total_count


def calculate_series_2(x: float, eps: float, num_processes: int = 4) -> Tuple[float, int]:
    def term_func_2(x_val: float, n: int) -> float:
        try:
            return 1.0 / ((2 * n - 1) * (x_val ** (2 * n - 1)))
        except (OverflowError, ZeroDivisionError):
            return 0.0

    with Manager() as manager:
        results: dict = manager.dict()
        processes: list = []
        for i in range(num_processes):
            p = SeriesProcess(x, eps, i + 1, num_processes, results, i, term_func_2)
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        total_sum: float = sum(results[f"sum_{i}"] for i in range(num_processes))
        total_count: int = sum(results[f"count_{i}"] for i in range(num_processes))

    return total_sum, total_count


def get_control_value_1(x: float) -> float:
    return 0.5 * math.log((1 + x) / (1 - x))


def get_control_value_2(x: float) -> float:
    return 0.5 * math.log((x + 1) / (x - 1))