import os
import cv2
import numpy as np
from skimage import transform

def to_numpy(v):
    if isinstance(v, list): return np.array(v)
    if isinstance(v, np.ndarray): return v

def get_similarity(a, b):
    a = to_numpy(a)
    b = to_numpy(b)
    return (np.sum(a * b) + 1.0) / 2.0

def resize_image(img, max_len):
    longer = max(img.shape[:2])
    if max(img.shape[:2]) > max_len:
        ratio = max_len / longer
        new_h, new_w = round(img.shape[0] * ratio), round(img.shape[1] * ratio)
        return cv2.resize(img, (new_w, new_h))
    else:
        return img

#calculate similarity
def visilize_similarity(features, save_dir):
    '''
    features is a list with each elem a tuple :
    [(name, feature, img), (name, feature, img)]
    '''
    max_img_size = 400
    for i in range(len(features) - 1):
        name1, fea1, img1 = features[i]
        img1 = resize_image(img1, max_img_size)
        for j in range(i+1,  len(features)):
            name2, fea2, img2 = features[j]
            img2 = resize_image(img2, max_img_size)
            similarity = get_similarity(fea1, fea2)
            print(f'{name1}<-->{name2}: {similarity}')
            
            img_w = max(img1.shape[1], img2.shape[1])
            img_h = max(img1.shape[0], img2.shape[0])
            img_similarity = np.zeros((img_h, img_w * 2, 3), np.uint8)
            print(img2.shape, img_similarity.shape)
            img_similarity[:img1.shape[0], :img1.shape[1]] = img1
            img_similarity[:img2.shape[0], img_w:(img_w + img2.shape[1])] = img2

            kFontSize = 1.6
            kFontStyle = cv2.FONT_HERSHEY_PLAIN
            kFontColor = (0, 69, 255)
            cv2.putText(img_similarity, 'sim=(%.3f)' % (similarity), 
                (10, 10 + 20), kFontStyle, kFontSize, kFontColor, 2)
            output_dir = save_dir
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            cv2.imwrite(os.path.join(output_dir, '%03d_%03d.jpg' % (i,j)), img_similarity)



def align_face(src_img, face_5p, dst_size = 112):
    align_5p = np.array([
      [30.2946, 51.6963],
      [65.5318, 51.5014],
      [48.0252, 71.7366],
      [33.5493, 92.3655],
      [62.7299, 92.2041] ], dtype=np.float32)
    align_5p[:,0] += 8.0
    assert(face_5p.shape == align_5p.shape)
    face_5p = face_5p.astype(np.float32)

    kOriginSize = 112
    scale = 1.0 * dst_size / kOriginSize
    align_5p = align_5p * scale

    tform = transform.SimilarityTransform()
    tform.estimate(face_5p, align_5p)
    M = tform.params[0:2,:]

    face_aligned  = cv2.warpAffine(src_img, M, (dst_size, dst_size), borderValue = 0.0)

    return face_aligned