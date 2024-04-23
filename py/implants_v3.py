import csv

# Функция для чтения данных кубиков из CSV и их дублирования согласно количеству
import csv

def read_cubes_from_csv(file_path):
    cubes = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                number, weight = int(row[0]), int(row[1])
                # Установить количество равным 0, если оно не указано
                quantity = int(row[2]) if len(row) > 2 else 0
                for _ in range(quantity):
                    cubes.append((number, weight))
            except ValueError as e:
                print(f"Ошибка при обработке строки {row}: {e}")
    return cubes


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

# Введите путь к вашему CSV-файлу здесь
file_path = input("Введите путь к файлу CSV с кубиками: ")

# Запрашиваем набор кубиков из файла
cubes = read_cubes_from_csv(file_path)

# Вводим желаемую массу
target_weight = int(input("Введите желаемую конечную массу: "))

# Находим оптимальную комбинацию кубиков
optimal_cubes, optimal_weight = find_optimal_cubes(cubes, target_weight)

# Выводим результаты
print(f"Minimal excess weight: {optimal_weight - target_weight} ({optimal_weight} out of {target_weight})")
print("Selected cubes:")
for number, weight in optimal_cubes:
    print(f"Number: {number}, Weight: {weight}")
