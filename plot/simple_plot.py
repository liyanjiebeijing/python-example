import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1.2, 2.5, 4.5, 7.3]

# plot函数作图
plt.plot(x, y, color="r", marker="*", linewidth=1.0)

plt.savefig("test.png", dpi=120)
