import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

times = []
for line in open("ping/ping.txt"):
    found = re.search(r"time=([\d.]+)", line)
    if found:
        times.append(float(found.group(1)))

times = np.array(times)
print("обработано:", len(times))

mean = times.mean()
std = times.std()
print("среднее", mean)
print("станд. отк", std)

plt.hist(times, bins=20, density=True, color="#F7C6D9", label="данные ping")

x = np.linspace(times.min(), times.max(), 200)
plt.plot(x, norm.pdf(x, mean, std), color="#E75480", linewidth=2, label="норм. распределение")

plt.xlabel("t доставки, мс")
plt.ylabel("плотность вероятности")
plt.title("гистограмма времени доставки")
plt.legend()
plt.savefig("histogram.png")
plt.show()