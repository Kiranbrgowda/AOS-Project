def fcfs(processes, burst_times):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Waiting time for first process is 0
    waiting_time[0] = 0

    # Calculate waiting time for each process
    for i in range(1, n):
        waiting_time[i] = waiting_time[i - 1] + burst_times[i - 1]

    # Calculate turnaround time for each process
    for i in range(n):
        turnaround_time[i] = waiting_time[i] + burst_times[i]

    return waiting_time, turnaround_time

def calculate_fcfs():
    # Extract burst times from the processes information
    processes = [p['id'] for p in processes_info]
    burst_times = [p['burst_time'] for p in processes_info]

    # Call the FCFS function
    waiting_times, turnaround_times = fcfs(processes, burst_times)

    # Calculate average waiting time and turnaround time
    average_waiting_time = sum(waiting_times) / len(waiting_times)
    average_turnaround_time = sum(turnaround_times) / len(turnaround_times)

    # print("Waiting Times:", waiting_times)
    # print("Turnaround Times:", turnaround_times)
    # print("Average Waiting Time:", average_waiting_time)
    # print("Average Turnaround Time:", average_turnaround_time)

    return waiting_times, turnaround_times, average_waiting_time, average_turnaround_time

# Example usage:
processes_info = [
    {'id': 1, 'burst_time': 5, 'priority': 1},
    {'id': 2, 'burst_time': 12, 'priority': 2},
    {'id': 3, 'burst_time': 16, 'priority': 5},
    {'id': 4, 'burst_time': 21, 'priority': 3},
    {'id': 5, 'burst_time': 23, 'priority': 4},
]

calculate_fcfs()

