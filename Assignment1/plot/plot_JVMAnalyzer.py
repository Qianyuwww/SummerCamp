import matplotlib.pyplot as plt
from datetime import datetime
import re

def parse_cpu_log(file_path):
    processes = {}
    start_time = None
    current_process = None

    with open(file_path, 'r') as file:
        for line in file:
            time_match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
            if time_match:
                timestamp = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S')

            process_match = re.search(r'Starting CPUAnalyzer for ([\w\.]+)', line)
            if process_match:
                current_process = process_match.group(1)
                if current_process != "check" and not current_process.startswith("startup"):
                    if current_process not in processes:
                        processes[current_process] = {
                            'time': [],
                            'miss_rate': []
                        }
                        start_time = timestamp
                continue

            if 'CPU Metrics for' in line:
                continue

            if current_process != "check" and not current_process.startswith("startup"):
                miss_rate_match = re.search(r'Miss Rate: (\d+\.\d+)%', line)
                if miss_rate_match and current_process:
                    miss_rate = float(miss_rate_match.group(1))
                    processes[current_process]['miss_rate'].append(miss_rate * 100)

                    relative_time = int((timestamp - start_time).total_seconds())
                    processes[current_process]['time'].append(relative_time)

    return processes

def parse_jvm_log(file_path):
    processes = {}
    start_time = None
    current_process = None

    with open(file_path, 'r') as file:
        for line in file:
            time_match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', line)
            if time_match:
                timestamp = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S')

            process_match = re.search(r'Starting JVMAnalyzer for ([\w\.]+)', line)
            if process_match:
                current_process = process_match.group(1)
                if current_process != "check" and not current_process.startswith("startup"):
                    if current_process not in processes:
                        processes[current_process] = {
                            'time': [],
                            'heap_usage': []
                        }
                        start_time = timestamp
                continue

            if 'JVM Metrics for' in line:
                continue

            if current_process != "check" and not current_process.startswith("startup"):
                heap_usage_match = re.search(r'Heap Usage: (\d+) MB / \d+ MB', line)
                if heap_usage_match and current_process:
                    heap_usage = float(heap_usage_match.group(1))
                    processes[current_process]['heap_usage'].append(heap_usage)

                    relative_time = int((timestamp - start_time).total_seconds())
                    processes[current_process]['time'].append(relative_time)

    return processes

def plot_heap_usage(processes_jvm, processes_cpu):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    for i, (process, data) in enumerate(processes_jvm.items()):
        if process == "scimark.fft.large":
            plt.plot(processes_jvm[process]['time'], processes_jvm[process]['heap_usage'], label='Crypto.aes heap_usage', marker='o', linestyle='-', markersize=3, color='blue')
            plt.plot(processes_cpu[process]['time'], processes_cpu[process]['miss_rate'], label='Crypto.aes miss_rate', marker='o', linestyle='-', markersize=3, color='red')

    plt.xlabel('Time (second)')
    plt.ylabel('Process Heap Usage (MB) / Cache Miss Rate X 100 (%)')
    plt.title('')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7,)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
    #plt.savefig("~/crypto.aes.jpg", format="jpeg", bbox_inches='tight', dpi=500)


file_path = '~/anlyzers/jvm_monitor.log'
processes_jvm = parse_jvm_log(file_path)
file_path = '~/anlyzers/cpu_monitor.log'
processes_cpu = parse_cpu_log(file_path)
plot_heap_usage(processes_jvm, processes_cpu)
