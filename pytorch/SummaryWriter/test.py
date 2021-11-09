
from torch.utils.tensorboard import SummaryWriter
import time

def main():
    current_time_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    writer = SummaryWriter(f'summary_test/{current_time_str}') # writer for buffering intermedium results
    for i in range(100):
        writer.add_scalar("0_Training/0_Training_Accuracy", (i / 10) ** 2, i)
        writer.add_scalar("0_Training/0_Test_Accuracy", (i / 10) ** 2 * 0.9, i)


if __name__ == '__main__':
    main()