import matplotlib.pyplot as plt

def get_lr(last_epoch, max_iter): 
    warmup = 5
    min_lr = 0
    base_lr = 0.1
    pow = 2

    if last_epoch < warmup:
        return base_lr / warmup * (last_epoch+1)

    if last_epoch < max_iter:
        coeff = (1 - (last_epoch-warmup) / (max_iter-warmup)) ** pow
    else:
        coeff = 0
    return (base_lr - min_lr) * coeff + min_lr

def plot_poly_lr():
    max_epoch = 50
    x_list = list(range(max_epoch))
    y_list = [get_lr(last_epoch, max_epoch) for last_epoch in x_list]
    plt.plot(x_list, y_list, color="r", marker="*", linewidth=1.0)
    plt.xlabel("epoch")
    plt.ylabel("lr")
    plt.grid(color="k", linestyle=":")
    plt.title("Poly learning rate")
    plt.savefig("poly_lr.png", dpi=120)
    

if __name__ == '__main__':
    plot_poly_lr()


