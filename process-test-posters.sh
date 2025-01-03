#!/bin/bash

# Loop through each .txt file in the test_posters directory
for file in test_posters/*.txt; do
    # Print the name of the file
    echo "Processing file: $file"

    # Invoke the Python script with the file as an argument
    python learning-poster-analyzer.py "$file"
done
