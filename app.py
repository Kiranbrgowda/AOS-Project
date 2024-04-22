from flask import Flask, render_template, request, send_file
from mix_pi_rr_improved import mix_pi_rr_improved
from Roundrobin import round_robin
from Fcfs import fcfs
from pbdrr import pb_drr_schedule  # Import the pb_drr_schedule function
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
from io import BytesIO
import json
from urllib.parse import quote, unquote
from compare_file import compare_scheduling_algorithms

app = Flask(__name__)

# Import or include your Mix PI-RR function here

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return schedule()
    else:
        file_name = request.form.get('file')
        if file_name == 'Sample1':
            file_path = 'Sample1.txt'
        elif file_name == 'Sample2':
            file_path = 'Sample2.txt'
        else:
            file_path = 'Sample3.txt'

        with open(file_path, 'r') as file:
            lines = file.readlines()

        data = {}
        for line in lines:
            key, value = line.strip().split('=')
            data[key] = value.split(',')

        quantum = data['quantum'][0]
        processes = data['processes']
        burst_times = list(map(int, data['burst_times']))
        arrival_times = list(map(int, data['arrival_times']))
        priorities = list(map(int, data['priorities']))
        repeat_counts = list(map(int, data['repeat_counts']))

        return render_template('index.html', quantum=quantum, processes=processes,
                                burst_times=burst_times, arrival_times=arrival_times,
                                priorities=priorities, repeat_counts=repeat_counts)

@app.route('/schedule', methods=['POST'])
def schedule():
    # Get the input from the form
    processes = request.form.getlist('processes')
    burst_times = list(map(int, request.form.getlist('burst_times')))
    arrival_times = list(map(int, request.form.getlist('arrival_times')))
    priorities = list(map(int, request.form.getlist('priorities')))
    repeat_counts = list(map(int, request.form.getlist('repeat_counts')))
    quantum = int(request.form['quantum'])

    waiting_times1, turnaround_times1 = mix_pi_rr_improved(
        processes, burst_times, arrival_times, priorities, repeat_counts, quantum)

    result1 = zip(processes, waiting_times1, turnaround_times1)

    waiting_times2, turnaround_times2 = round_robin(burst_times, arrival_times, quantum)

    # Combine the results with the process names for display
    result2 = zip(processes, waiting_times2, turnaround_times2)

    waiting_times, turnaround_times = fcfs(processes, burst_times)

    result3 = zip(processes, waiting_times, turnaround_times)

   # Call pb_drr_schedule function
    pb_drr_processes = [{'id': i + 1, 'burst_time': bt, 'priority': p} for i, (bt, p) in enumerate(zip(burst_times, priorities))]
    scheduled_processes = pb_drr_schedule(pb_drr_processes)

    # Extract waiting times and turnaround times for PB DRR
    waiting_times4 = [p['wait_time'] for p in scheduled_processes]
    turnaround_times4 = [p['turnaround_time'] for p in scheduled_processes]

    result4 = zip(processes, waiting_times4, turnaround_times4)

    # Call compare function
    pb_drr_processes = [{'id': i + 1, 'burst_time': bt, 'priority': p} for i, (bt, p) in enumerate(zip(burst_times, priorities))]
    compared_results = compare_scheduling_algorithms(pb_drr_processes)
    

    avg_wait_rr = compared_results['avg_wait_rr']
    avg_tat_rr = compared_results['avg_tat_rr']
    avg_wait_pbrr = compared_results['avg_wait_pbrr']
    avg_tat_pbrr = compared_results['avg_tat_pbrr']
    avg_wait_mix = compared_results['avg_wait_mix']
    avg_tat_mix = compared_results['avg_tat_mix']
    avg_wait_fcfs = compared_results['avg_wait_fcfs']
    avg_tat_fcfs = compared_results['avg_tat_fcfs']


    data = {
        'waiting_times1': waiting_times1,
        'waiting_times2': waiting_times2,
        'waiting_times': waiting_times,
        'turnaround_times1': turnaround_times1,
        'turnaround_times2': turnaround_times2,
        'turnaround_times': turnaround_times,
        'waiting_times4': waiting_times4,
        'turnaround_times4': turnaround_times4,
        'avg_wait_rr': avg_wait_rr,
        'avg_tat_rr': avg_tat_rr,
        'avg_wait_pbrr': avg_wait_pbrr,
        'avg_tat_pbrr': avg_tat_pbrr,
        'avg_wait_mix': avg_wait_mix,
        'avg_tat_mix': avg_tat_mix,
        'avg_wait_fcfs': avg_wait_fcfs,
        'avg_tat_fcfs': avg_tat_fcfs
    }

    return render_template('results.html', result1=result1, result2=result2, result3=result3, result4=result4, quantum=quantum, data=quote(json.dumps(data)), compared_results=compared_results)
@app.route('/plot')
def plot():
    data = json.loads(unquote(request.args.get('data')))
    waiting_times1 = data['waiting_times1']
    waiting_times2 = data['waiting_times2']
    waiting_times = data['waiting_times']
    turnaround_times1 = data['turnaround_times1']
    turnaround_times2 = data['turnaround_times2']
    turnaround_times = data['turnaround_times']
    waiting_times4 = data['waiting_times4']
    turnaround_times4 = data['turnaround_times4']
    avg_wait_rr = data['avg_wait_rr']
    avg_tat_rr = data['avg_tat_rr']
    avg_wait_pbrr = data['avg_wait_pbrr']
    avg_tat_pbrr = data['avg_tat_pbrr']
    avg_wait_mix = data['avg_wait_mix']
    avg_tat_mix = data['avg_tat_mix']
    avg_wait_fcfs = data['avg_wait_fcfs']
    avg_tat_fcfs = data['avg_tat_fcfs']

    # Generate Matplotlib plot
    x = [1, 2, 3, 4]
    y1 = [sum(waiting_times1), sum(waiting_times2), sum(waiting_times), sum(waiting_times4)]
    y2 = [sum(turnaround_times1), sum(turnaround_times2), sum(turnaround_times), sum(turnaround_times4)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 12))

    # Line graph
    ax1.plot(x, y1, marker='o', label='Waiting Time')
    ax1.plot(x, y2, marker='o', label='Turnaround Time')
    ax1.set_xticks(x)
    ax1.set_xticklabels(['Mix PI RR', 'RR', 'FCFS', 'PB DRR'])
    ax1.set_xlabel('Scheduling Algorithm')
    ax1.set_ylabel('Time')
    ax1.set_title('Comparison of Scheduling Algorithms (Line Graph)')
    ax1.legend()

    # Bar graph
    bar_width = 0.35
    ax2.bar([i - bar_width/2 for i in x], y1, bar_width, label='Waiting Time')
    ax2.bar([i + bar_width/2 for i in x], y2, bar_width, label='Turnaround Time')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Mix PI RR', 'RR', 'FCFS', 'PB DRR'])
    ax2.set_xlabel('Scheduling Algorithm')
    ax2.set_ylabel('Time')
    ax2.set_title('Comparison of Scheduling Algorithms (Bar Graph)')
    ax2.legend()

    plt.tight_layout()

    # Save the plot as a PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

@app.route('/plot2')
def plot2():
    data = json.loads(unquote(request.args.get('data')))
    avg_wait_rr = data['avg_wait_rr']
    avg_tat_rr = data['avg_tat_rr']
    avg_wait_pbrr = data['avg_wait_pbrr']
    avg_tat_pbrr = data['avg_tat_pbrr']
    avg_wait_mix = data['avg_wait_mix']
    avg_tat_mix = data['avg_tat_mix']
    avg_wait_fcfs = data['avg_wait_fcfs']
    avg_tat_fcfs = data['avg_tat_fcfs']

    # Generate Matplotlib plot
    x1 = [1, 2, 3, 4]
    y3 = [avg_wait_rr, avg_wait_pbrr, avg_wait_mix, avg_wait_fcfs]
    y4 = [avg_tat_rr, avg_tat_pbrr, avg_tat_mix, avg_tat_fcfs]

    # y1 = [sum(avg_wait_rr), sum(avg_wait_pbrr), sum(avg_wait_mix), sum(avg_wait_fcfs)]
    # y2 = [sum(avg_tat_rr), sum(avg_tat_pbrr), sum(avg_tat_mix), sum(avg_tat_fcfs)]

    fig, ax3 = plt.subplots(figsize=(10, 6))

    # Line graph
    ax3.plot(x1, y3, marker='o', label='Waiting Time')
    ax3.plot(x1, y4, marker='o', label='Turnaround Time')
    ax3.set_xticks(x)
    ax3.set_xticklabels(['RR','PB DRR', 'Mix PI RR', 'FCFS'])
    ax3.set_xlabel('Scheduling Algorithm')
    ax3.set_ylabel('Time')
    ax3.set_title('Comparison of Scheduling Algorithms (Line Graph)')
    ax3.legend()

    plt.tight_layout()

    # Save the plot as a PNG image
    img1 = BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    plt.close()

    return send_file(img1, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)