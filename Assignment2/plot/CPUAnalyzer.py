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
def plot_cpu_usage(processes_openjdk, processes_kona, processes_bisheng, processes_dragonwell):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    plt.plot(processes_openjdk['compress']['time'], processes_openjdk['compress']['cpu_usage'], label='OpenJDK', marker='o', linestyle='-', markersize=3, color=colors[0])
    plt.plot(processes_kona['compress']['time'], processes_kona['compress']['cpu_usage'], label='Kona', marker='o', linestyle='-', markersize=3, color=colors[1])
    plt.plot(processes_bisheng['compress']['time'], processes_bisheng['compress']['cpu_usage'], label='Bisheng', marker='o', linestyle='-', markersize=3, color=colors[2])
    plt.plot(processes_dragonwell['compress']['time'], processes_dragonwell['compress']['cpu_usage'], label='Dragonwell', marker='o', linestyle='-', markersize=3, color=colors[3])

    plt.xlabel('Time (second)')
    plt.ylabel('Process CPU Usage (%)')
    plt.title('CPU Usage Over Time')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7,)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.show()
    plt.savefig("~/cpu_usage.jpg", format="jpeg", bbox_inches='tight', dpi=500)

def plot_cpu_frequency(processes_openjdk, processes_kona, processes_bisheng, processes_dragonwell):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    plt.plot(processes_openjdk['compress']['time'], processes_openjdk['compress']['cpu_freq'], label='OpenJDK',
             marker='o', linestyle='-', markersize=3, color=colors[0])
    plt.plot(processes_kona['compress']['time'], processes_kona['compress']['cpu_freq'], label='Kona', marker='o',
             linestyle='-', markersize=3, color=colors[1])
    plt.plot(processes_bisheng['compress']['time'], processes_bisheng['compress']['cpu_freq'], label='Bisheng',
             marker='o', linestyle='-', markersize=3, color=colors[2])
    plt.plot(processes_dragonwell['compress']['time'], processes_dragonwell['compress']['cpu_freq'],
             label='Dragonwell', marker='o', linestyle='-', markersize=3, color=colors[3])

    plt.xlabel('Time (second)')
    plt.ylabel('CPU Frequency (GHz)')
    plt.title('CPU Frequency Over Time')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7, )
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.show()
    plt.savefig("~/cpu_frequency.jpg", format="jpeg", bbox_inches='tight', dpi=500)

def plot_miss_rate(processes_openjdk, processes_kona, processes_bisheng, processes_dragonwell):
    plt.figure(figsize=(15, 6))

    colors = plt.cm.tab20.colors
    plt.plot(processes_openjdk['compress']['time'], processes_openjdk['compress']['miss_rate'], label='OpenJDK',
             marker='o', linestyle='-', markersize=3, color=colors[0])
    plt.plot(processes_kona['compress']['time'], processes_kona['compress']['miss_rate'], label='Kona', marker='o',
             linestyle='-', markersize=3, color=colors[1])
    plt.plot(processes_bisheng['compress']['time'], processes_bisheng['compress']['miss_rate'], label='Bisheng',
             marker='o', linestyle='-', markersize=3, color=colors[2])
    plt.plot(processes_dragonwell['compress']['time'], processes_dragonwell['compress']['miss_rate'],
             label='Dragonwell', marker='o', linestyle='-', markersize=3, color=colors[3])


    plt.xlabel('Time (second)')
    plt.ylabel('Cache Miss Rate (%)')
    plt.title('Cache Miss Rate Over Time')

    plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=7, )
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    #plt.show()
    plt.savefig("~/cache_miss_rate.jpg", format="jpeg", bbox_inches='tight', dpi=500)


file_path = '~/openJDK-8/cpu_monitor.log'
processes_openjdk = parse_cpu_log(file_path)
file_path = '~/Kona-8/cpu_monitor.log'
processes_kona = parse_cpu_log(file_path)
file_path = '~/Bisheng-8/cpu_monitor.log'
processes_bisheng = parse_cpu_log(file_path)
file_path = '~/Dragonwell-8/cpu_monitor.log'
processes_dragonwell = parse_cpu_log(file_path)
plot_cpu_usage(processes_openjdk, processes_kona, processes_bisheng, processes_dragonwell)
plot_cpu_frequency(processes_openjdk, processes_kona, processes_bisheng, processes_dragonwell)
plot_miss_rate(processes_openjdk, processes_kona, processes_bisheng, processes_dragonwell)
