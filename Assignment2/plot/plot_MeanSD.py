import numpy as np
import matplotlib.pyplot as plt

jvms = ['OpenJDK 8', 'Alibaba Dragonwell 8', 'Tencent Kona 8', 'Huawei Bisheng 8']
scores = {
    'OpenJDK 8': [1425.59, 1419.69, 1420.65],
    'Alibaba Dragonwell 8': [1457.23, 1458.03, 1457],
    'Tencent Kona 8': [1436.88, 1435.07, 1434.01],
    'Huawei Bisheng 8': [1484.39, 1485.38, 1484.22]
}

means = [np.mean(scores[jvm]) for jvm in jvms]
stds = [np.std(scores[jvm], ddof=1) for jvm in jvms]

x = np.arange(len(jvms))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(x, means, width, label='Mean Score', yerr=stds, capsize=5,
              color=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
              edgecolor='black')

ax.set_ylabel('Score (ops/m)')
ax.set_title('Mean SPECjvm2008 Scores with Standard Deviations')
ax.set_xticks(x)
ax.set_xticklabels(jvms)

for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{means[i]:.2f}\n±{stds[i]:.2f}',
            ha='center', va='bottom')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
#plt.show()
plt.savefig("~/Mean_SD.jpg", format="jpeg", bbox_inches='tight', dpi=500)
