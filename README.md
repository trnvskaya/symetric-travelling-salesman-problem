# Symetric Travelling Salesman Problem

## Overview

This project implements a solution to the Traveling Salesman Problem (TSP) using the Hill-Climbing algorithm. The goal is to find a near-optimal route that minimizes the total travel distance between cities.

## Features

- **State Encoding:** The solution represents a tour as a permutation of cities.

- **Objective Function:** The total distance of the tour is minimized.

- **Neighborhood Search:** The algorithm explores nearby solutions by swapping cities in the tour.

- **Local Search Strategy:** Supports both steepest ascent and first improvement hill-climbing variations.

- **Escape from Local Optima:** Random restarts (represented by parameter *steepest* being set to True) help avoid getting stuck in local optima.

## Usage

```sh
python3 main.py <distances-file-csv> <algorithm>
```

### Arguments

- `<distances-file-csv>`: CSV file containing city names and distances between them.
- `<algorithm>`: The algorithm to be used:
  - `bruteforce` → Try all possible routes (exhaustive search).
  - `hill-climbing` → Use a local search method to find an optimized route.

### Example Input CSV

```
Prague,0,2215,2292
Madrid,2215,0,3982
Ankara,2292,3982,0
```

This means:
- Madrid is **3982 km** from Ankara.
- Prague is **2215 km** from Madrid.
- Ankara is **2292 km** from Prague.

### Dependencies

- Python 3
- NumPy
- tqdm

### Running the Program

```sh
python3 main.py distances.csv hill-climbing
```

This will attempt to solve TSP using the **Hill-Climbing algorithm**.

```sh
python3 main.py distances.csv bruteforce
```

This will attempt to solve TSP using **Brute Force** (not recommended for large inputs).

The project contains 2 input files: `in10.csv` and `in18.csv`.

Brute Force is **NOT** recommended to use on the second input file.

                       

