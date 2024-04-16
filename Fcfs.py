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

