import csv
import argparse
from itertools import combinations
import sys
import itertools
import time

def find_optimal_combination(cubes, target_weight):
    closest_overweight = None
    min_overweight = float('inf')
    cubes.sort(key=lambda x: x[1], reverse=True)  # От самого тяжелого к легкому

    # Максимальное количество итераций при полном переборе всех комбинаций
    max_combinations = 2 ** len(cubes)
    print("Начинаем поиск оптимальной комбинации...")

    for i, combination in enumerate(itertools.chain.from_iterable(itertools.combinations(cubes, r) for r in range(1, len(cubes) + 1))):
        # Выводим индикацию работы каждые 1000 итераций
        if i % 1000000 == 0:
            print(f"\rОбработано {i} из {max_combinations} возможных комбинаций...")
        sys.stdout.flush()
        current_weight = sum(cube[1] for cube in combination)
        overweight = current_weight - target_weight
        if 0 <= overweight < min_overweight:
            min_overweight = overweight
            closest_overweight = combination

            # Если достигли точного совпадения - завершаем
            if overweight == 0:
                break

    print("Поиск завершен.")
    return closest_overweight

# def find_optimal_combination(cubes, target_weight):
#     # Находим все уникальные комбинации возможных кубиков
#     all_combinations = (comb for r in range(1, len(cubes) + 1) for comb in combinations(cubes, r))
    
#     # Ищем комбинацию с минимальным перевесом, но весом более target_weight
#     optimal_combination = min(
#         (comb for comb in all_combinations if sum(cube[1] for cube in comb) >= target_weight),
#         key=lambda comb: sum(cube[1] for cube in comb),
#         default=None
#     )
    
#     if optimal_combination is not None:
#         return optimal_combination, sum(cube[1] for cube in optimal_combination)
#     else:
#         return [], 0


# Функция для чтения данных кубиков из CSV
def read_cubes_from_csv(file_path):
    cubes = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3 and row[2].isdigit() and int(row[2]) > 0:
                number, weight, quantity = map(int, row)
                cubes.extend([(number, weight)] * quantity)
    return cubes

# Функция запуска программы
def main(file_path, target_weight):
    cubes = read_cubes_from_csv(file_path)
    
    # Выводим набор кубиков с которым будем работать
    print(f"Работаем с набором из {len(cubes)} кубиков:")
    for cube in cubes:
        print(f"Кубик номер {cube[0]} весом {cube[1]}")

    # Проводим расчет оптимальной комбинации...
    optimal_cubes, optimal_weight = find_optimal_combination(cubes, target_weight)

    print(f"Minimal excess weight: {optimal_weight - target_weight} ({optimal_weight} out of {target_weight})")
    print("Selected cubes:")
    for number, weight in optimal_cubes:
        print(f"Number: {number}, Weight: {weight}")

# Парсинг аргументов командной строки, если они есть
parser = argparse.ArgumentParser(description="Optimize the cube set to reach or exceed a target weight.")
parser.add_argument("-f", "--file", type=str, help="Path to the CSV file containing cubes.")
parser.add_argument("-w", "--weight", type=int, help="The target weight to achieve or exceed.")
args = parser.parse_args()

if not args.file or not args.weight:
    args.file = args.file if args.file else input("Введите путь к файлу CSV с кубиками: ")
    args.weight = args.weight if args.weight else int(input("Введите желаемую конечную массу: "))

# Запускаем основную функцию программы
main(args.file, args.weight)
