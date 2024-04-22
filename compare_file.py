from Roundrobin import round_robin
from pbdrr import pb_drr_schedule
from mix_pi_rr_improved import mix_pi_rr_improved, test_scheduler
from Fcfs import fcfs

def compare_scheduling_algorithms(processes_info):
    burst_times = [p['burst_time'] for p in processes_info]
    priorities = [p['priority'] for p in processes_info]
    process = [p['id'] for p in processes_info]
    repeat_counts = [3] * len(processes_info)  # Example repeat count for Mix_Pi_RR
    quantum = 4  # Example quantum for RR and PBDRR if applicable

    waiting_times_rr, turnaround_times_rr = round_robin(burst_times, [0, 0, 0, 0, 0], quantum)

    scheduled_processes = pb_drr_schedule(processes_info)
    waiting_times_pbrr = [p['wait_time'] for p in scheduled_processes]
    turnaround_times_pbrr = [p['turnaround_time'] for p in scheduled_processes]
    avg_wait_pbrr = sum(waiting_times_pbrr) / len(waiting_times_pbrr)
    avg_tat_pbrr = sum(turnaround_times_pbrr) / len(turnaround_times_pbrr)

    waiting_times_mix, turnaround_times_mix = mix_pi_rr_improved(
        processes=process,
        burst_times=burst_times,
        arrival_times=[0, 0, 0, 0, 0],
        priorities=priorities,
        repeat_counts=repeat_counts,
        quantum=quantum
    )

    waiting_times_fcfs, turnaround_times_fcfs = fcfs(process, burst_times)

    avg_wait_rr = sum(waiting_times_rr) / len(waiting_times_rr)
    avg_tat_rr = sum(turnaround_times_rr) / len(turnaround_times_rr)
    avg_wait_mix = sum(waiting_times_mix) / len(waiting_times_mix)
    avg_tat_mix = sum(turnaround_times_mix) / len(turnaround_times_mix)
    avg_wait_fcfs = sum(waiting_times_fcfs) / len(waiting_times_fcfs)
    avg_tat_fcfs = sum(turnaround_times_fcfs) / len(turnaround_times_fcfs)

    return {
        'avg_wait_rr': avg_wait_rr,
        'avg_tat_rr': avg_tat_rr,
        'avg_wait_pbrr': avg_wait_pbrr,
        'avg_tat_pbrr': avg_tat_pbrr,
        'avg_wait_mix': avg_wait_mix,
        'avg_tat_mix': avg_tat_mix,
        'avg_wait_fcfs': avg_wait_fcfs,
        'avg_tat_fcfs': avg_tat_fcfs
    }