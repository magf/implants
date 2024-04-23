import csv
import argparse
from itertools import combinations

# Функция для чтения данных кубиков из CSV
def read_cubes_from_csv(file_path):
    cubes = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            number, weight = int(row[0]), int(row[1])
            # Установить количество равным 0, если оно не указано или неверно указано
            quantity = int(row[2]) if len(row) > 2 and row[2].isdigit() else 0
            for _ in range(quantity):
                cubes.append((number, weight))
    return cubes

# Функция для определения оптимального набора кубиков
# Возвращает список комбинаций кубиков, вес которых близок к целевому значению с наименьшим перевесом
def find_optimal_cubes(cubes, target_weight):
    # Сортируем список в порядке убывания веса
    cubes.sort(key=lambda x: x[1], reverse=True)
    
    selected_cubes = []
    total_weight = 0

    for cube in cubes:
        if total_weight + cube[1] <= target_weight:
            selected_cubes.append(cube)
            total_weight += cube[1]

    # В случае если общий вес недостаточен, попробуем добавить следующий самый тяжелый кубик
    if total_weight < target_weight and cubes:
        next_cube = min(cubes, key=lambda x: target_weight - (total_weight + x[1]))
        selected_cubes.append(next_cube)
        total_weight += next_cube[1]

    return selected_cubes, total_weight

# Основная программа
def main(file_path, target_weight):
    cubes = read_cubes_from_csv(file_path)
    optimal_cubes, optimal_weight = find_optimal_cubes(cubes, target_weight)

    print(f"Minimal excess weight: {optimal_weight - target_weight} ({optimal_weight} out of {target_weight})")
    print("Selected cubes:")
    for number, weight in optimal_cubes:
        print(f"Number: {number}, Weight: {weight}")

# Настройка анализатора аргументов командной строки
parser = argparse.ArgumentParser(description="Optimize cube weights.")
parser.add_argument("-f", "--file", type=str, help="Path to the CSV file with the cubes.")
parser.add_argument("-w", "--weight", type=int, help="Target weight to reach.")
args = parser.parse_args()

# Если аргумент файл не предоставлен, запросить его у пользователя
if args.file is None:
    file_path = input("Введите путь к файлу CSV с кубиками: ")
else:
    file_path = args.file

# Если аргумент вес не предоставлен, запросить его у пользователя
if args.weight is None:
    target_weight = int(input("Введите желаемую конечную массу: "))
else:
    target_weight = args.weight

# Запускаем основную функцию программы
main(file_path, target_weight)
