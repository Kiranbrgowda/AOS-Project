def round_robin(burst_time, arrival_time, quantum_time):
    n = len(burst_time)
    remaining_time = [0] * n
    waiting_time = [0] * n
    turnaround_time = [0] * n
    total_burst_time = sum(burst_time)
    current_time = 0
    
    for i in range(n):
        remaining_time[i] = burst_time[i]
    
    while total_burst_time > 0:
        for i in range(n):
            if remaining_time[i] > 0:
                if remaining_time[i] > quantum_time:
                    current_time += quantum_time
                    remaining_time[i] -= quantum_time
                    total_burst_time -= quantum_time
                else:
                    current_time += remaining_time[i]
                    total_burst_time -= remaining_time[i]
                    turnaround_time[i] = current_time - arrival_time[i]
                    remaining_time[i] = 0
        
        for i in range(n):
            if remaining_time[i] > 0:
                waiting_time[i] = current_time - arrival_time[i]
                break
    
    for i in range(n):
        print("Process", i+1, "Waiting Time:", waiting_time[i], "Turnaround Time:", turnaround_time[i])

    return waiting_time , turnaround_time
