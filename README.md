# CPU Scheduling Simulator

A Python-based simulation tool to understand and analyze various CPU scheduling algorithms. This project supports the following algorithms:
1. **First-Come-First-Serve (FCFS)**
2. **Shortest Job First (SJF)**
3. **Round Robin (RR)**

The tool enables users to input processes, calculate key scheduling metrics, and perform comparative analysis of the algorithms.

## Features
- **Interactive CLI Interface**: Choose algorithms and analyze their metrics.
- **Performance Metrics**:
  - CPU Utilization
  - Average Waiting Time
  - Average Turnaround Time
- **Comparative Analysis**:
  - Bar chart visualization of waiting and turnaround times for different algorithms.
- **Dynamic Input**:
  - Processes loaded from a file (`data.txt`) with process ID, arrival time, and burst time.
  - Time Quantum input for Round Robin scheduling.

## Prerequisites
- Python 3.8 or later
- Required libraries: `pandas`, `matplotlib`, `numpy`

Install dependencies using:
```bash
pip install pandas matplotlib numpy


Hint: Create virtual environment for your own convenience!!