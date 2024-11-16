import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = burst_time

def read_processes_from_file(file_path):
    try:
        processes = []
        with open(file_path, 'r') as f:
            for line in f:
                pid, at, bt = map(int, line.strip().split())
                processes.append(Process(pid, at, bt))
        return processes
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except ValueError:
        print("Error: Invalid file format. Ensure the file contains integers in each line.")
    return []

def calculate_metrics(processes):
    total_waiting = sum(p.waiting_time for p in processes)
    total_turnaround = sum(p.turnaround_time for p in processes)
    total_burst_time = sum(p.burst_time for p in processes)
    total_time = max(p.completion_time for p in processes)
    cpu_util = (total_burst_time / total_time) * 100
    avg_waiting = total_waiting / len(processes)
    avg_turnaround = total_turnaround / len(processes)
    return cpu_util, avg_waiting, avg_turnaround

def generate_dataframe(processes):
    return pd.DataFrame([{
        'Process ID': p.process_id,
        'Arrival Time': p.arrival_time,
        'Burst Time': p.burst_time,
        'Completion Time': p.completion_time,
        'Waiting Time': p.waiting_time,
        'Turnaround Time': p.turnaround_time
    } for p in processes])

def plot_combined_graph(algorithms, waiting_times, turnaround_times):
    if len(algorithms) != len(waiting_times) or len(waiting_times) != len(turnaround_times):
        print("Error: Input lists must have the same length.")
        return

    x = np.arange(len(algorithms))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))

    bars1 = ax.bar(x - width / 2, waiting_times, width, label='Average Waiting Time', color='skyblue')
    bars2 = ax.bar(x + width / 2, turnaround_times, width, label='Average Turnaround Time', color='black')

    ax.set_xlabel('Scheduling Algorithms')
    ax.set_ylabel('Time (units)')
    ax.set_title('Comparison of Average Waiting Time and Turnaround Time')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()

    max_value = max(max(waiting_times), max(turnaround_times))
    ax.set_ylim(0, max_value + max_value * 0.1)

    plt.tight_layout()
    plt.show()

def reset_remaining_time(processes):
    for process in processes:
        process.remaining_time = process.burst_time

def fcfs_sched(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        current_time = max(current_time, process.arrival_time)
        process.completion_time = current_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        current_time = process.completion_time
    return calculate_metrics(processes), generate_dataframe(processes)

def round_robin_sched(processes, time_quantum):
    queue = processes.copy()
    current_time = 0
    while queue:
        current_process = queue.pop(0)
        current_time = max(current_time, current_process.arrival_time)
        if current_process.remaining_time <= time_quantum:
            current_time += current_process.remaining_time
            current_process.remaining_time = 0
        else:
            current_time += time_quantum
            current_process.remaining_time -= time_quantum
            queue.append(current_process)

        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
    return calculate_metrics(processes), generate_dataframe(processes)

def shortest_job_first_sched(processes):
    queue = processes.copy()
    current_time = 0
    while queue:
        queue.sort(key=lambda x: (x.burst_time, x.arrival_time))
        current_process = queue.pop(0)
        current_time = max(current_time, current_process.arrival_time)
        current_process.completion_time = current_time + current_process.burst_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        current_time = current_process.completion_time
    return calculate_metrics(processes), generate_dataframe(processes)

# Function to add unique instances
def add_unique_instance(instance_list, new_instance):
    for existing_instance in instance_list:
        if new_instance.equals(existing_instance):
            return
    instance_list.append(new_instance)

def view_instances(algorithms, waiting_times, turnaround_times, fcfs_instances, sjf_instances, rr_instances):
    print("\nResults for all instances:\n")
    print("1. View all instances")
    print("2. View a specific instance")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Error: Invalid choice.")
        return

    if choice == 1:
        print("\nFCFS Results:")
        for idx, instance in enumerate(fcfs_instances):
            print(f"Instance {idx + 1}:\n", instance.to_string(index=False))
        print("\nSJF Results:")
        for idx, instance in enumerate(sjf_instances):
            print(f"Instance {idx + 1}:\n", instance.to_string(index=False))
        print("\nRR Results:")
        for idx, instance in enumerate(rr_instances):
            print(f"Instance {idx + 1}:\n", instance.to_string(index=False))
        plot_combined_graph(algorithms, waiting_times, turnaround_times)

    elif choice == 2:
        print("1. FCFS")
        print("2. SJF")
        print("3. RR")
        try:
            algo_choice = int(input("Enter algorithm type: "))
            instance_number = int(input("Enter instance number: ")) - 1

            if algo_choice == 1:
                selected_instances = fcfs_instances
                algo_name = "FCFS"
            elif algo_choice == 2:
                selected_instances = sjf_instances
                algo_name = "SJF"
            elif algo_choice == 3:
                selected_instances = rr_instances
                algo_name = "RR"
            else:
                print("Invalid option.")
                return

            if 0 <= instance_number < len(selected_instances):
                instance_df = selected_instances[instance_number]
                print(f"{algo_name} Instance {instance_number + 1}:\n", instance_df.to_string(index=False))
                plot_combined_graph([algo_name], [waiting_times[instance_number]], [turnaround_times[instance_number]])
            else:
                print("Instance out of range.")
        except (ValueError, IndexError):
            print("Error: Invalid input.")

def main():
    file_path = 'data.txt'
    processes = read_processes_from_file(file_path)
    if not processes:
        return

    fcfs_instances, sjf_instances, rr_instances = [], [], []
    algorithms, waiting_times, turnaround_times = [], [], []

    while True:
        print("\nSelect a CPU Scheduling Algorithm:")
        print("1. First-Come-First-Serve (FCFS)")
        print("2. Shortest Job First (SJF)")
        print("3. Round Robin (RR)")
        print("4. Comparative Analysis")
        print("5. Exit")

        try:
            option = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue

        if option == 1:  # FCFS
            metrics, df = fcfs_sched(processes.copy())
            add_unique_instance(fcfs_instances, df)
            print("\n\t\t ------------------------------------")
            print("\t\t  FIRST COME FIRST SERVED SCHEDULING:")
            print("\t\t ------------------------------------")
            print(df)
            print(f"\nMetrics: CPU Utilization = {metrics[0]:.2f}%, Average Waiting Time = {metrics[1]:.2f}, Average Turnaround Time = {metrics[2]:.2f}")
            algorithms.append("FCFS")
            waiting_times.append(metrics[1])
            turnaround_times.append(metrics[2])

        elif option == 2:  # SJF
            metrics, df = shortest_job_first_sched(processes.copy())
            add_unique_instance(sjf_instances, df)
            print("\n\t\t\t-------------------------------")
            print("\t\t\tSHORTEST JOB FIRST SCHEDULING:")
            print("\t\t\t-------------------------------")
            print(df)
            print(f"\nMetrics: CPU Utilization = {metrics[0]:.2f}%, Average Waiting Time = {metrics[1]:.2f}, Average Turnaround Time = {metrics[2]:.2f}")
            algorithms.append("SJF")
            waiting_times.append(metrics[1])
            turnaround_times.append(metrics[2])

        elif option == 3:  # RR
            try:
                tq = int(input("Enter Time Quantum: "))
                reset_remaining_time(processes)
                metrics, df = round_robin_sched(processes.copy(), tq)
                add_unique_instance(rr_instances, df)
                print("\n\t\t\t---------------------------")
                print("\t\t\t  ROUND ROBIN SCHEDULING:")
                print("\t\t\t---------------------------")
                print(df)
                print(f"\nMetrics: CPU Utilization = {metrics[0]:.2f}%, Average Waiting Time = {metrics[1]:.2f}, Average Turnaround Time = {metrics[2]:.2f}")
                algorithms.append("RR")
                waiting_times.append(metrics[1])
                turnaround_times.append(metrics[2])
            except ValueError:
                print("Invalid input for Time Quantum. Please enter a valid integer.")

        elif option == 4:  # Comparative Analysis
            view_instances(algorithms, waiting_times, turnaround_times, fcfs_instances, sjf_instances, rr_instances)

        elif option == 5:  # Exit
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a number between 1 and 5.")

if __name__ == '__main__':
    main()
