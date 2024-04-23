import csv

# Функция для чтения данных кубиков из CSV
def read_cubes_from_csv(file_path):
    cubes = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Предполагаем, что CSV файл имеет две колонки: номер и масса кубика
            number, weight = int(row[0]), int(row[1])
            cubes.append((number, weight))
    return cubes

# Предположим, что вы храните данные кубиков в файле 'cubes.csv'
file_path = 'cubes.csv'
cubes = read_cubes_from_csv(file_path)

# Введите желаемую конечную массу
target_weight = int(input("Введите желаемую массу: "))

# Функция поиска оптимального решения
def find_min_excess(cubes, target_weight):
    total_weight = sum(weight for number, weight in cubes)
    dp = [0] + [-1]*(total_weight + 1)
    
    for i in range(len(cubes)):
        for w in range(total_weight, cubes[i][1] - 1, -1):
            if dp[w - cubes[i][1]] != -1:
                dp[w] = max(dp[w], dp[w - cubes[i][1]] + cubes[i][1])
    
    # Находим минимальный перевес (наименьший вес, который больше заданной массы)
    for i in range(target_weight, total_weight + 1):
        if dp[i] >= target_weight:
            return i, dp[i]

# Вызов функции поиска и вывод результата
min_excess_weight, cubes_weight = find_min_excess(cubes, target_weight)
print(f"Minimal possible weight above {target_weight} is: {min_excess_weight} with total weight: {cubes_weight}")
