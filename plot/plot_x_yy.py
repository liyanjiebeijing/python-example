import matplotlib.pyplot as plt

def load_data(data_path):
    with open(data_path) as f:
        lines = f.readlines()
        titles = lines[0].split()

        x_list = []
        y1_list = []
        y2_list = []
        for line in lines[1:]:
            x, y1, y2 = line.split()
            x_list.append(float(x))
            y1_list.append(float(y1))
            y2_list.append(float(y2))

        return titles, x_list, y1_list, y2_list


def plot(titles, x_list, y1_list, y2_list):
    plt.plot(x_list, y1_list, color="r", marker="*", linewidth=1.0, label=titles[1])
    plt.plot(x_list, y2_list, color="b", marker="*", linewidth=1.0, label=titles[2])
    plt.xlabel("cluster-thresh")
    plt.ylabel("v-mesure-score")
    plt.legend(loc='lower right')
    plt.grid(color="k", linestyle=":")
    plt.title("Face Cluster Thresh")
    plt.savefig("face-cluster-thresh.png", dpi=120)


def main():
    titles, x_list, y1_list, y2_list = load_data('./cluster_result.txt')
    plot(titles, x_list, y1_list, y2_list)


if __name__ == '__main__':
    main()