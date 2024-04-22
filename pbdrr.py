def pb_drr_schedule(processes, ots=4):
    # Initialize each process with the default time slice and additional metrics
    for process in processes:
        process['ITS'] = ots  # Start with the Original Time Slice
        process['remaining_time'] = process['burst_time']
        process['completion_time'] = 0
        process['start_time'] = None
        process['wait_time'] = 0
        process['turnaround_time'] = 0

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

    return processes