#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from series_two_series import (
    calculate_series_1,
    calculate_series_2,
    get_control_value_1,
    get_control_value_2
)


def print_series_info(series_num: int, x: float, eps: float, 
                     calculated_sum: float, control_value: float, 
                     term_count: int) -> None:
    """Вывод информации о вычислениях ряда."""
    error = abs(calculated_sum - control_value)
    
    print(f"\n{'='*60}")
    print(f"РЯД {series_num}")
    print(f"{'='*60}")
    
    if series_num == 1:
        print("Ряд: S = Σ [x^(2n+1)/(2n+1)], n=0..∞")
        print("Контрольная функция: y = ln(√((1+x)/(1-x))) = 0.5 * ln((1+x)/(1-x))")
    else:
        print("Ряд: S = Σ [1/((2n-1)*x^(2n-1))], n=1..∞")
        print("Контрольная функция: y = 0.5 * ln((x+1)/(x-1))")
    
    print(f"\nx = {x}, ε = {eps}")
    print("\nРезультаты:")
    print(f"  Вычисленная сумма: {calculated_sum:.10f}")
    print(f"  Контрольное значение: {control_value:.10f}")
    print(f"  Абсолютная погрешность: {error:.2e}")
    print(f"  Учтено членов ряда: {term_count}")
    
    if error < eps:
        print("  ✓ Точность достигнута (погрешность < ε)")
    else:
        print("  ✗ Погрешность превышает ε")


def main() -> None:
    """Основная функция для выполнения индивидуального задания."""
    print("ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ")
    print("Вычисление сумм двух бесконечных рядов с использованием многопроцессности")
    print("=" * 60)
    
    # Параметры из задания
    x1 = 0.35  # Для первого ряда |x| < 1
    x2 = 3.0   # Для второго ряда |x| > 1
    eps = 1e-7
    
    print(f"\nОбщая точность: ε = {eps}")
    
    # Вычисление первого ряда
    print("\n" + "="*60)
    print("ВЫЧИСЛЕНИЕ ПЕРВОГО РЯДА")
    print("="*60)
    
    sum1, count1 = calculate_series_1(x1, eps, num_processes=4)
    control1 = get_control_value_1(x1)
    print_series_info(1, x1, eps, sum1, control1, count1)
    
    # Вычисление второго ряда
    print("\n" + "="*60)
    print("ВЫЧИСЛЕНИЕ ВТОРОГО РЯДА")
    print("="*60)
    
    sum2, count2 = calculate_series_2(x2, eps, num_processes=4)
    control2 = get_control_value_2(x2)
    print_series_info(2, x2, eps, sum2, control2, count2)
    
    # Сводка результатов
    print("\n" + "="*60)
    print("СВОДКА РЕЗУЛЬТАТОВ")
    print("="*60)
    
    error1 = abs(sum1 - control1)
    error2 = abs(sum2 - control2)
    
    print(f"\nПервый ряд (x={x1}):")
    print(f"  Погрешность: {error1:.2e} {'<' if error1 < eps else '>'} ε")
    print(f"  Членов ряда учтено: {count1}")
    
    print(f"\nВторой ряд (x={x2}):")
    print(f"  Погрешность: {error2:.2e} {'<' if error2 < eps else '>'} ε")
    print(f"  Членов ряда учтено: {count2}")
    
    print("\n" + "="*60)
    if error1 < eps and error2 < eps:
        print("✓ ОБА РЯДА ВЫЧИСЛЕНЫ С ЗАДАННОЙ ТОЧНОСТЬЮ")
    else:
        print("✗ ТОЧНОСТЬ НЕ ДОСТИГНУТА ДЛЯ ОДНОГО ИЛИ ОБОХ РЯДОВ")
    print("="*60)


if __name__ == "__main__":
    main()
