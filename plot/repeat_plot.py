import matplotlib.pyplot as plt
import numpy as np

def repeat_plot():
    for i in range(1, 5):
        x = np.array([each for each in range(0, 100)])
        y = i * 0.5 * x        
        # plt.cla()
        plt.plot(x, y)
        plt.savefig(f"{i}.png", dpi=120)

if __name__ == '__main__':
    repeat_plot()