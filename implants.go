package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
)

func main() {

	file, err := os.Open("implants.csv")

	// Checks for the error
	if err != nil {
		log.Fatal("Error while reading the file", err)
	}

	// Closes the file
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()

	// Checks for the error
	if err != nil {
		fmt.Println("Error reading records")
	}

	// Loop to iterate through
	// and print each of the string slice
	for _, eachrecord := range records {
		fmt.Println(eachrecord)
	}
}
