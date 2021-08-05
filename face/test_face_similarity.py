from face_utils import *

def main():
    img_suffixes = ['png', 'jpg', 'jpeg']
    features = []
    image_dir = 'images'
    for name in os.listdir(image_dir):
        suffix = name.split('.')[-1]
        if suffix in img_suffixes:
            feature = np.load(f"{image_dir}/{name + '.npy'}")
            img = cv2.imread(f'{image_dir}/{name}')
            features.append((name, feature, img))

    save_dir = image_dir + '_compare'
    if not os.path.exists(save_dir): os.makedirs(save_dir)
    visilize_similarity(features, save_dir)


if __name__ == '__main__':
    main()