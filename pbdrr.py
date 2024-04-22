def pb_drr_schedule(processes, ots=4):
    # Initialize each process with the default time slice and additional metrics
    for process in processes:
        process['ITS'] = ots  # Start with the Original Time Slice
        process['remaining_time'] = process['burst_time']
        process['completion_time'] = 0
        process['start_time'] = None
        process['wait_time'] = 0

    current_time = 0
    last_burst_time = float('inf')  # To compare with the first process

    while any(p['remaining_time'] > 0 for p in processes):
        for process in processes:
            if process['remaining_time'] > 0:
                # Determine PC based on priority
                if process['priority'] == min(p['priority'] for p in processes):
                    pc = 1
                else:
                    pc = 0
                
                # Determine SC based on burst time comparison with last process
                if process['burst_time'] < last_burst_time:
                    sc = 1
                else:
                    sc = 0

                # Calculate ITS for this round
                process['ITS'] = ots + pc * ots + sc * ots

                # Execute process for ITS time quantum or remaining time
                time_slice = min(process['ITS'], process['remaining_time'])
                process['remaining_time'] -= time_slice
                if process['start_time'] is None:
                    process['start_time'] = current_time
                last_burst_time = process['burst_time']  # Update last burst time for next comparison

                current_time += time_slice

                # If process finishes, calculate completion and wait times
                if process['remaining_time'] == 0:
                    process['completion_time'] = current_time
                    process['turnaround_time'] = process['completion_time'] - process['start_time']
                    process['wait_time'] = process['turnaround_time'] - process['burst_time']

    # return processes
    avg_waiting_time = sum(p['wait_time'] for p in processes) / len(processes)
    avg_turnaround_time = sum(p['turnaround_time'] for p in processes) / len(processes)
    return avg_waiting_time, avg_turnaround_time

# # Example usage:
# processes_info = [
#     {'id': 1, 'burst_time': 5, 'priority': 1},
#     {'id': 2, 'burst_time': 12, 'priority': 2},
#     {'id': 3, 'burst_time': 16, 'priority': 5},
#     {'id': 4, 'burst_time': 21, 'priority': 3},
#     {'id': 5, 'burst_time': 23, 'priority': 4},
# ]

# scheduled_processes = pb_drr_schedule(processes_info)
# for p in scheduled_processes:
#     print(f"Process {p['id']}: Wait Time: {p['wait_time']}, Turnaround Time: {p['turnaround_time']}")

# # Define processes based on the given case 1 data
# processes_case_1 = [
#     {'id': 1, 'initial_burst': 50, 'burst_time': 5, 'priority': 2},
#     {'id': 2, 'initial_burst': 27, 'burst_time': 12, 'priority': 3},
#     {'id': 3, 'initial_burst': 12, 'burst_time': 16, 'priority': 1},
#     {'id': 4, 'initial_burst': 55, 'burst_time': 21, 'priority': 4},
#     {'id': 5, 'initial_burst': 5, 'burst_time': 23, 'priority': 5},
# ]


# # Compute average waiting time and turnaround time
# avg_waiting_time = sum(p['wait_time'] for p in scheduled_processes) / len(scheduled_processes)
# avg_turnaround_time = sum(p['turnaround_time'] for p in scheduled_processes) / len(scheduled_processes)

# print("avg_waiting_time: ", avg_waiting_time, "avg_turnaround_time: ",avg_turnaround_time)

# # processes = [
# #     {'id': 1, 'burst_time': 50, 'priority': 1},
# #     {'id': 2, 'burst_time': 27, 'priority': 2},
# #     {'id': 3, 'burst_time': 12, 'priority': 5},
# #     {'id': 4, 'burst_time': 55, 'priority': 3},
# #     {'id': 5, 'burst_time': 5, 'priority': 4},
# # ]
