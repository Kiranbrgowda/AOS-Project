from collections import deque

def mix_pi_rr_improved(processes, burst_times, arrival_times, priorities, repeat_counts, quantum):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n
    remaining_times = burst_times.copy()
    completion_times = [0] * n
    queue = deque()
    current_time = 0
    completed = 0
    arrived = [False] * n
    original_repeat_counts = repeat_counts.copy()

    while completed < n:
        for i in range(n):
            if arrival_times[i] <= current_time and not arrived[i]:
                queue.append(i)
                arrived[i] = True

        if not queue:
            current_time += 1
            continue

        highest_priority = min(priorities[i] for i in queue)
        same_priority_processes = [i for i in queue if priorities[i] == highest_priority]
        process_index = min(same_priority_processes, key=lambda x: arrival_times[x])
        queue.remove(process_index)

        execution_time = min(remaining_times[process_index], quantum)
        current_time += execution_time
        remaining_times[process_index] -= execution_time

        if remaining_times[process_index] == 0:
            completion_times[process_index] = current_time
            completed += 1
        else:
            if repeat_counts[process_index] > 1:
                repeat_counts[process_index] -= 1
            else:
                priorities[process_index] = max(priorities) + 1
                repeat_counts[process_index] = original_repeat_counts[process_index]
            queue.append(process_index)

    for i in range(n):
        turnaround_times[i] = completion_times[i] - arrival_times[i]
        waiting_times[i] = turnaround_times[i] - burst_times[i]
    
    # print(waiting_times)
    # print(turnaround_times)

    return waiting_times, turnaround_times

def test_scheduler():
    processes = ['P1', 'P2', 'P3', 'P4', 'P5']
    burst_times = [5,12,16,21,23]
    arrival_times = [0, 0, 0, 0, 0]
    priorities = [1, 2, 5, 3, 4]
    repeat_counts = [3, 3, 3, 3, 3]  # Repeating with original priority
    quantum = 4

    waiting_times, turnaround_times = mix_pi_rr_improved(
        processes=processes,
        burst_times=burst_times,
        arrival_times=arrival_times,
        priorities=priorities,
        repeat_counts=repeat_counts,
        quantum=quantum
    )

    # Calculate average waiting time and turnaround time
    average_waiting_time = sum(waiting_times) / len(waiting_times)
    average_turnaround_time = sum(turnaround_times) / len(turnaround_times)

    # print("Average Waiting Time:", average_waiting_time)
    # print("Average Turnaround Time:", average_turnaround_time)

    return waiting_times, turnaround_times

# Call the testing function
test_scheduler()
