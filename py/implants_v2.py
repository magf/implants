import csv
from itertools import combinations

# основной алгоритм
def find_optimal_cubes(cubes, target_weight):
    best_weight = 0
    best_combination = []
    
    # Генерируем все возможные комбинации кубиков
    for r in range(1, len(cubes) + 1):
        for combo in combinations(cubes, r):
            current_weight = sum(weight for number, weight in combo)
            
            # Выбираем комбинацию, ближайшую к желаемой массе, но не меньше её
            if best_weight < current_weight >= target_weight and (best_weight == 0 or current_weight < best_weight):
                best_weight = current_weight
                best_combination = combo
    
    return best_combination, best_weight

# читает данные из CSV-файла
def read_cubes_from_csv(file_path):
    cubes = []
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            number, weight = int(row[0]), int(row[1])
            cubes.append((number, weight))
    return cubes

# Введите путь к вашему CSV-файлу здесь
file_path = input("Введите путь к файлу CSV с кубиками: ")

# Запрашиваем набор кубиков из файла
cubes = read_cubes_from_csv(file_path)

# Вводим желаемую массу
target_weight = int(input("Введите желаемую конечную массу: "))

# Находим оптимальную комбинацию
optimal_cubes, optimal_weight = find_optimal_cubes(cubes, target_weight)

# Выводим результаты
print(f"Оптимальный перевес: {optimal_weight - target_weight} ({optimal_weight} из {target_weight})")
print("Использованные кубики:")
for number, weight in optimal_cubes:
    print(f"Номер: {number}, Вес: {weight}")
