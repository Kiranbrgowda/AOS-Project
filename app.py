from flask import Flask, render_template, request, send_file
from mix_pi_rr_improved import mix_pi_rr_improved
from Roundrobin import round_robin
from Fcfs import fcfs
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
from io import BytesIO
import json
from urllib.parse import quote, unquote


app = Flask(__name__)

# Import or include your Mix PI-RR function here
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    # Assuming form input names match the variables
    processes = request.form.getlist('processes')
    burst_times = list(map(int, request.form.getlist('burst_times')))
    arrival_times = list(map(int, request.form.getlist('arrival_times')))
    priorities = list(map(int, request.form.getlist('priorities')))
    repeat_counts = list(map(int, request.form.getlist('repeat_counts')))
    quantum = int(request.form['quantum'])

    waiting_times1, turnaround_times1 = mix_pi_rr_improved(
        processes, burst_times, arrival_times, priorities, repeat_counts, quantum)
    
    result1 = zip(processes, waiting_times1, turnaround_times1)
    
    waiting_times2, turnaround_times2 =  round_robin(burst_times, arrival_times, quantum)

    # Combine the results with the process names for display
    
    result2 = zip(processes, waiting_times2, turnaround_times2)

    waiting_times, turnaround_times =  fcfs(processes, burst_times)

    result3 = zip(processes, waiting_times, turnaround_times)

    data = {
        'waiting_times1': waiting_times1,
        'waiting_times2': waiting_times2,
        'waiting_times': waiting_times,
        'turnaround_times1': turnaround_times1,
        'turnaround_times2': turnaround_times2,
        'turnaround_times': turnaround_times
    }

    return render_template('results.html', result1=result1, result2=result2, result3=result3, quantum=quantum, data=quote(json.dumps(data)))


@app.route('/plot')
def plot():
    data = json.loads(unquote(request.args.get('data')))
    waiting_times1 = data['waiting_times1']
    waiting_times2 = data['waiting_times2']
    waiting_times = data['waiting_times']
    turnaround_times1 = data['turnaround_times1']
    turnaround_times2 = data['turnaround_times2']
    turnaround_times = data['turnaround_times']

    # Generate Matplotlib plot
    x = [1, 2, 3]
    y1 = [sum(waiting_times1), sum(waiting_times2), sum(waiting_times)]
    y2 = [sum(turnaround_times1), sum(turnaround_times2), sum(turnaround_times)]
    
    plt.figure(figsize=(8, 6))
    plt.plot(x, y1, marker='o', label='Waiting Time')
    plt.plot(x, y2, marker='o', label='Turnaround Time')
    plt.xticks(x, ['Mix PI RR', 'RR', 'FCFS'])
    plt.xlabel('Scheduling Algorithm')
    plt.ylabel('Time')
    plt.title('Comparison of Scheduling Algorithms')
    plt.legend()

    # Save the plot as a PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
