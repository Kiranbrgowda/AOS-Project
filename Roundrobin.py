def round_robin(burst_time, arrival_time, quantum_time):
    n = len(burst_time)
    remaining_time = burst_time[:]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completed = [False] * n
    current_time = 0

    while any(not x for x in completed):
        for i in range(n):
            if remaining_time[i] > 0 and arrival_time[i] <= current_time:
                executed_time = min(remaining_time[i], quantum_time)
                remaining_time[i] -= executed_time
                current_time += executed_time
                
                if remaining_time[i] == 0:
                    completed[i] = True
                    turnaround_time[i] = current_time - arrival_time[i]
                    waiting_time[i] = turnaround_time[i] - burst_time[i]

    return waiting_time, turnaround_time

# Test data
burst_times = [5,12,16,21,23]
arrival_times = [0,0,0,0,0]
quantum_time = 3

# Use the Round Robin function with the extracted data
waiting_times, turnaround_times = round_robin(burst_times, arrival_times, quantum_time)

# Calculate the average turnaround time
average_turnaround_time = sum(turnaround_times) / len(turnaround_times)
average_waiting_times = sum(waiting_times) / len(waiting_times)
# print("Average Turnaround Time: ", average_turnaround_time,"average_waiting_times: ",average_waiting_times)
