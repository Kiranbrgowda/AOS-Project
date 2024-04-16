from flask import Flask, render_template, request
from mix_pi_rr_improved import mix_pi_rr_improved
from Roundrobin import round_robin
from Fcfs import fcfs
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

    waiting_times, turnaround_times = mix_pi_rr_improved(
        processes, burst_times, arrival_times, priorities, repeat_counts, quantum)
    
    result1 = zip(processes, waiting_times, turnaround_times)
    
    waiting_times, turnaround_times =  round_robin(burst_times, arrival_times, quantum)

    # Combine the results with the process names for display
    
    result2 = zip(processes, waiting_times, turnaround_times)

    waiting_times, turnaround_times =  fcfs(processes, burst_times)

    result3 = zip(processes, waiting_times, turnaround_times)

    return render_template('results.html', result1=result1, result2=result2, result3 = result3,  quantum=quantum)

if __name__ == '__main__':
    app.run(debug=True)
