import learner
from IntegralImage import IntegralImage
import os
import random
import cv2

DATASET_PATH = '/Users/adwivedi/self/code/face_dataset/'


def read_image(filepath, label):
    return IntegralImage(cv2.imread(filepath, cv2.CV_LOAD_IMAGE_GRAYSCALE), label)


def get_images(path, label):
    images = []
    for file_name in os.listdir(path):
        if file_name.endswith('png') or file_name.endswith('.pgm'):
            images.append(read_image(os.path.join(path, file_name), label))
    return images


def get_dataset(subdir):
    dir_path = os.path.join(DATASET_PATH, subdir)
    faces = get_images(os.path.join(dir_path, 'face'), 1)
    nonfaces = get_images(os.path.join(dir_path, 'nonface'), -1)
    return faces, nonfaces


def main():
    faces, non_faces = get_dataset('train')

    T = 20

    boost_learner = learner.AdaBoostLearner(image_height=25, image_width=25)
    boost_learner.addEvidence(faces, non_faces, T)

    faces, non_faces = get_dataset('test')

    correct_faces = 0
    correct_non_faces = 0
    data = faces + non_faces
    random.shuffle(data)

    for image in data:
        result = boost_learner.query(image)
        if image.label == 1 and result == 1:
            correct_faces += 1
        if image.label == -1 and result == -1:
            correct_non_faces += 1

    print '..done. Result:\n  Faces: ' + str(correct_faces) + '/' + str(len(faces)) + '\n  non-Faces: ' + str(correct_non_faces) + '/' + str(len(non_faces))


if __name__ == "__main__":
   main()