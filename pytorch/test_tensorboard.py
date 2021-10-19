from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

def main():
    writer = SummaryWriter(f'tensorboard/test')
    for epoch in tqdm(range(100)):
        writer.add_scalar("0_Training/3_Training_Accuracy", epoch ** 2, epoch + 1)
        writer.add_scalar("0_Training/4_Loss", (0.1 * epoch) ** 2, epoch + 1)
        writer.add_scalar("0_Training/5_Student_Loss", (0.2 * epoch) ** 2, epoch + 1)
        writer.add_scalar("0_Training/6_Teacher_Loss", (0.3 * epoch) ** 2, epoch + 1)

if __name__ == '__main__':
    main()