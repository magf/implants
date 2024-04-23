package main

import (
	"bufio"
	"encoding/csv"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
)

type Implant struct {
	Number   int
	Weight   int
	Quantity int
}

func loadImplantsFromCSV(filePath string) ([]Implant, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(bufio.NewReader(file))
	var implants []Implant

	for {
		line, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			continue // Пропускаем ошибочные строки
		}
		if len(line) < 3 {
			continue // Пропускаем строки с недостаточным количеством колонок
		}

		number, errNumber := strconv.Atoi(line[0])
		weight, errWeight := strconv.Atoi(line[1])
		quantity, errQuantity := strconv.Atoi(line[2])
		if errNumber != nil || errWeight != nil || errQuantity != nil || quantity <= 0 {
			continue // Пропускаем строки, если данные некорректны
		}

		for i := 0; i < quantity; i++ {
			implants = append(implants, Implant{Number: number, Weight: weight})
		}
	}

	return implants, nil
}

func getIntFromUser(prompt string) int {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print(prompt)
	input, _ := reader.ReadString('\n')
	value, err := strconv.Atoi(strings.TrimSpace(input))
	if err != nil {
		fmt.Println("Неверный ввод, попробуйте еще раз.")
		return getIntFromUser(prompt) // Рекурсивно запрашиваем ввод
	}
	return value
}

func printImplants(implants []Implant) {
	implantMap := make(map[int]int)
	for _, implant := range implants {
		implantMap[implant.Number] += 1
	}

	fmt.Println("Список имплантов, полученных из файла:")
	for number, count := range implantMap {
		fmt.Printf("Имплант №%d: %d шт.\n", number, count)
	}
}

// // Оставшиеся функции, реализующие алгоритм поиска оптимального набора имплантов и вычисления...

// func findAllCombinations(implants []Implant) [][]Implant {
// 	fmt.Println("Начинаем подбор всех возможных комбинаций имплантов...")
// 	var combinations [][]Implant
// 	var currentCombination []Implant
// 	var findCombinations func(int, int)
// 	findCombinations = func(startIndex, currentWeight int) {
// 		for i := startIndex; i < len(implants); i++ {
// 			newCombination := append(currentCombination, implants[i])
// 			combinations = append(combinations, newCombination)
// 			findCombinations(i+1, currentWeight+implants[i].Weight)
// 		}
// 	}
// 	findCombinations(0, 0)
// 	fmt.Println("Подбор комбинаций завершён.", len(combinations), "комбинаций найдено.")
// 	return combinations
// }

// func findOptimalCombinations(combinations [][]Implant, targetWeight, maxOverweight int) [][]Implant {
// 	fmt.Printf("Поиск оптимальных комбинаций с минимальным перевесом не более %d...\n", maxOverweight)
// 	optimalCombinations := make([][]Implant, 0)
// 	for _, combination := range combinations {
// 		totalWeight := 0
// 		for _, implant := range combination {
// 			totalWeight += implant.Weight
// 		}
// 		overweight := totalWeight - targetWeight
// 		if overweight >= 0 && overweight <= maxOverweight {
// 			optimalCombinations = append(optimalCombinations, combination)
// 		}
// 	}
// 	fmt.Println("Поиск завершён. Найдено оптимальных комбинаций:", len(optimalCombinations))
// 	return optimalCombinations
// }

func findImplantCombinations(
	implants []Implant, targetWeight, maxOverweight int,
) (optimalCombinations []Implant, totalWeight int) {
	fmt.Println("Поиск оптимальных комбинаций имплантов...")

	// Инициализация вспомогательных переменных
	bestWeight := targetWeight + maxOverweight
	bestCombination := make([]Implant, 0)

	// Вспомогательная функция для рекурсивного поиска
	var findCombinations func(int, int, []Implant)
	findCombinations = func(startIndex, currentWeight int, currentCombination []Implant) {
		if currentWeight > bestWeight {
			return // Прекратить поиск, если вес превысил максимально допустимый
		}
		if currentWeight >= targetWeight && currentWeight <= bestWeight {
			bestWeight = currentWeight           // Сохранить наилучший вес
			bestCombination = currentCombination // Сохранить наилучшую комбинацию
		}
		// Итерация по оставшимся имплантам
		for i := startIndex; i < len(implants); i++ {
			findCombinations(i+1, currentWeight+implants[i].Weight,
				append(currentCombination, implants[i]))
		}
	}

	// Начать поиск с первого импланта
	findCombinations(0, 0, []Implant{})

	// Вычислить общий вес оптимальной комбинации
	for _, implant := range bestCombination {
		totalWeight += implant.Weight
	}

	return bestCombination, totalWeight
}

// Остальной код функции main...
func main() {
	filePathPtr := flag.String("file", "", "путь к файлу CSV с имплантами")
	targetWeightPtr := flag.Int("target", 0, "необходимый минимальный вес")
	maxOverweightPtr := flag.Int("maxover", 0, "максимально допустимый перевес")

	flag.Parse()

	filePath := *filePathPtr
	targetWeight := *targetWeightPtr
	maxOverweight := *maxOverweightPtr

	if filePath == "" {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print("Введите путь к файлу CSV с имплантами: ")
		filePath, _ = reader.ReadString('\n')
		filePath = strings.TrimSpace(filePath)
	}
	if filePath == "" {
		fmt.Printf("Путь к файлу не задан, используем значение по умолчанию 'implants.csv'\n")
		filePath = "implants.csv"
	}
	for targetWeight <= 0 {
		targetWeight = getIntFromUser("Введите необходимый минимальный вес (больше 0): ")
	}
	for maxOverweight <= 0 {
		maxOverweight = getIntFromUser("Введите максимально допустимый перевес (больше 0): ")
	}

	implants, err := loadImplantsFromCSV(filePath)
	if err != nil {
		log.Fatalf("Ошибка при загрузке имплантов из CSV: %s", err)
	}
	printImplants(implants)

	// Поиск оптимальных комбинаций
	optimalCombinations, totalWeight := findImplantCombinations(implants, targetWeight, maxOverweight)

	// Вывод найденных оптимальных комбинаций
	fmt.Printf("Найденные оптимальные комбинации имплантов (Общий вес: %d):\n", totalWeight)
	for _, implant := range optimalCombinations {
		fmt.Printf("Имплант №%d (Вес: %d)\n", implant.Number, implant.Weight)
	}
}
