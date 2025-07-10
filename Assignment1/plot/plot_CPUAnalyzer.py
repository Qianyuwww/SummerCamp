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
                            'cpu_usage': [],
                            'cpu_freq': [],
                            'miss_rate': []
                        }
                        start_time = timestamp
                continue

            if 'CPU Metrics for' in line:
                continue

            if current_process != "check" and not current_process.startswith("startup"):
                cpu_usage_match = re.search(r'Process CPU Usage: (\d+\.\d+)%', line)
                if cpu_usage_match and current_process:
                    cpu_usage = float(cpu_usage_match.group(1))
                    processes[current_process]['cpu_usage'].append(cpu_usage)

                cpu_freq_match = re.search(r'CPU Frequency: (\d+\.\d+) GHz', line)
                if cpu_freq_match and current_process:
                    cpu_freq = float(cpu_freq_match.group(1))
                    processes[current_process]['cpu_freq'].append(cpu_freq)

                miss_rate_match = re.search(r'Miss Rate: (\d+\.\d+)%', line)
                if miss_rate_match and current_process:
                    miss_rate = float(miss_rate_match.group(1))
                    processes[current_process]['miss_rate'].append(miss_rate)

                    relative_time = int((timestamp - start_time).total_seconds())
                    processes[current_process]['time'].append(relative_time)

    return processes

# 绘制 Process CPU Usage 折线图
def plot_cpu_usage(processes):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    for i, (process, data) in enumerate(processes.items()):
        color = colors[i % len(colors)]
        plt.plot(data['time'], data['cpu_usage'], label=process, marker='o', linestyle='-', markersize=3, color=color)

    plt.xlabel('Time (second)')
    plt.ylabel('Process CPU Usage (%)')
    plt.title('CPU Usage Over Time')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7,)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.show()
    plt.savefig("~/cpu_usage.jpg", format="jpeg", bbox_inches='tight', dpi=500)

# 绘制 CPU Frequency 折线图
def plot_cpu_frequency(processes):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    for i, (process, data) in enumerate(processes.items()):
        color = colors[i % len(colors)]
        plt.plot(data['time'], data['cpu_freq'], label=process, marker='o', linestyle='-', markersize=3, color=color)

    plt.xlabel('Time (second)')
    plt.ylabel('CPU Frequency (GHz)')
    plt.title('CPU Frequency Over Time')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7, )
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.show()
    plt.savefig("~/cpu_frequency.jpg", format="jpeg", bbox_inches='tight', dpi=500)

# 绘制 Cache Miss Rate 折线图
def plot_miss_rate(processes):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    for i, (process, data) in enumerate(processes.items()):
        color = colors[i % len(colors)]
        plt.plot(data['time'], data['miss_rate'], label=process, marker='o', linestyle='-', markersize=3, color=color)

    plt.xlabel('Time (second)')
    plt.ylabel('Cache Miss Rate (%)')
    plt.title('Cache Miss Rate Over Time')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7, )
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.show()
    plt.savefig("~/cache_miss_rate.jpg", format="jpeg", bbox_inches='tight', dpi=500)


file_path = '~/analyzers/cpu_monitor.log'
processes = parse_cpu_log(file_path)
plot_cpu_usage(processes)
plot_cpu_frequency(processes)
plot_miss_rate(processes)
