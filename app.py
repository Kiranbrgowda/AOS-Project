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
import base64

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')
    
@app.route('/readfile',methods=['POST'])
def readfile():
    file_name = request.form.get('file')
    if file_name == 'Sample1':
        file_path = 'Sample1.txt'
    elif file_name == 'Sample2':
        file_path = 'Sample2.txt'
    elif file_name == 'Sample3':
        file_path = 'Sample3.txt'
    elif file_name == 'Sample4':
        file_path = 'Sample4.txt'
    elif file_name == 'Sample5':
        file_path = 'Sample5.txt'
    else:
        file_path = 'Sample6.txt'

    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    for line in lines:
        key, value = line.strip().split('=')
        data[key] = value.split(',')

    quantum = int(data['quantum'][0])
    processes = data['processes']
    burst_times = list(map(int, data['burst_times']))

    arrival_times = list(map(int, data['arrival_times']))
    priorities = list(map(int, data['priorities']))
    repeat_counts = list(map(int, data['repeat_counts']))

    result1,result2,result3,result4,compared_results,rr_plot, fcfs_plot, mix_plot, pbdr_plot,data = processalgo(processes,burst_times,arrival_times,priorities,repeat_counts,quantum)

    return render_template('results.html', result1=result1, result2=result2, result3=result3, result4=result4, quantum=quantum, compared_results=compared_results, rr_plot=rr_plot, fcfs_plot=fcfs_plot, mix_plot=mix_plot, pbdr_plot=pbdr_plot,data=quote(json.dumps(data)))


def plot_times(processes, waiting_times, turnaround_times, title):
    fig, ax = plt.subplots()
    indices = range(len(processes))
    ax.bar(indices, waiting_times, width=0.3, label='Waiting Time', align='center')
    ax.bar([p + 0.3 for p in indices], turnaround_times, width=0.3, label='Turnaround Time', align='center')
    ax.set_xlabel('Processes')
    ax.set_ylabel('Time Units')
    ax.set_title(title)
    ax.set_xticks([p + 0.15 for p in indices])
    ax.set_xticklabels(processes)
    ax.legend()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)  # Close the figure to free memory
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def processalgo(processes,burst_times,arrival_times,priorities,repeat_counts,quantum):
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


    rr_plot = plot_times(processes, waiting_times2, turnaround_times2, 'Round Robin Results')
    fcfs_plot = plot_times(processes, waiting_times, turnaround_times, 'FCFS Results')
    mix_plot = plot_times(processes, waiting_times1, turnaround_times1, 'Mix PI-RR Improved Results')
    pbdr_plot = plot_times(processes, waiting_times4, turnaround_times4, 'Priority Based DRR Results')



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
    return result1,result2,result3,result4,compared_results,rr_plot, fcfs_plot, mix_plot, pbdr_plot,data

@app.route('/schedule', methods=['POST'])
def schedule():
    # Get the input from the form
    processes = request.form.getlist('processes[]')
    burst_times = [int(x) for x in request.form.getlist('burst_times[]')]
    arrival_times = [int(x) for x in request.form.getlist('arrival_times[]')]
    priorities = [int(x) for x in request.form.getlist('priorities[]')]
    repeat_counts = [int(x) for x in request.form.getlist('repeat_counts[]')]
    quantum = int(request.form['quantum'])

    result1,result2,result3,result4,compared_results,rr_plot, fcfs_plot, mix_plot, pbdr_plot, data = processalgo(processes,burst_times,arrival_times,priorities,repeat_counts,quantum)
    return render_template('results.html', result1=result1, result2=result2, result3=result3, result4=result4, quantum=quantum, compared_results=compared_results, rr_plot=rr_plot, fcfs_plot=fcfs_plot, mix_plot=mix_plot, pbdr_plot=pbdr_plot,data=quote(json.dumps(data)))

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

if __name__ == '__main__':
    app.run(debug=True)