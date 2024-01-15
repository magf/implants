package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

type Implant struct {
	level int
	power int
	count int
}

func main() {

	file, err := os.Open("implants.csv")

	// Checks for the error
	if err != nil {
		log.Fatal("Error while reading the file", err)
	}

	// Closes the file
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = 3
	records, err := reader.ReadAll()

	// Checks for the error
	if err != nil {
		fmt.Println("Error reading records.\n", err)
	}

	for _, eachrecord := range records {
		if level, err := strconv.Atoi(eachrecord[1]); err == nil {
			implant{level:???????????????? } := level
		}
		fmt.Println(eachrecord)
	}
}
