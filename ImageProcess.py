import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from skimage.feature import hog
from sklearn.cluster import KMeans
from time import time

def load_dataset(class_names,path, num_per_class=-1):
    data = []
    labels = []
    for id, class_name in class_names.items():

        print("Loading images from class: %s" % id)
        img_path_class = glob.glob(path + class_name + '/*.png')
        if num_per_class > 0:
            img_path_class = img_path_class[:num_per_class]
        labels.extend([id]*len(img_path_class))
        for filename in img_path_class:
            data.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    dataf = []
    for x in data:
        flipped = cv2.flip(x, 1)
        dataf.append(flipped)

    for y in dataf:
        data.append(y)

    for z in range(len(labels)):
        labels.append(labels[z])

    dataf = []
    for x in data:
        flipped = cv2.flip(x, 0)
        dataf.append(flipped)

    for y in dataf:
        data.append(y)

    for z in range(len(labels)):
        labels.append(labels[z])

    return data, labels

def split(img,n):
    row = np.vsplit(img,n)
    hold = []
    for x in row:
        cols = np.hsplit(x,n)
        for box in cols:
            hold.append(box)
    return hold

def extracthog(data):

    hold = []
    for img in data:
        keep = hog(img)
        hold.append(keep)

    hold = np.asarray(hold)
    return hold


def train(samples,n,ground):
    # Shapes for regular
    # loading data
    class_names = [name[9:] for name in glob.glob('./Shapes/*')]
    class_names = dict(zip(range(3, len(class_names) + 3), class_names))
    print("class_names: %s " % class_names)
    n_train_samples_per_class = samples #250 max

    train_data, train_label = load_dataset(class_names,'./Shapes/', n_train_samples_per_class)
    n_train = len(train_label)
    print("n_train: %s" % n_train)

    grid = cv2.imread("grid.png", 0)
    boxes = split(grid, n)
    boxes = np.asarray(boxes)
    # print(boxes.shape)

    # plt.imshow(boxes[len(boxes)-1],"gray")
    # plt.show()
    img_new_size = (80, 80)
    trainD = list(map(lambda x: cv2.resize(x, img_new_size), train_data))
    trainD = np.stack(trainD)

    boxes = boxes[1:len(boxes) - 1]
    # print(len(boxes))
    testD = list(map(lambda x: cv2.resize(x, img_new_size), boxes))
    testD = np.stack(testD)

    # extracting features
    print("extracting features")
    trainD = extracthog(trainD)
    testD = extracthog(testD)
    # trainD, testD = extract(trainD,testD)
    print("finished extracting")

    #testL = [7, 5, 5, 5, 5, 5, 6, 6, 3,
             #6, 8, 5, 7, 4, 6, 7, 7, 7, 5,
             #4, 3, 4, 3, 8, 5, 8, 8, 4, 7,
             #3, 3, 6, 3, 6, 3, 5, 3, 5, 6,
             #4, 7, 5, 5, 7, 8, 7, 3, 6, 5,
             #5, 4, 4, 4, 7, 8, 3, 3, 3, 4,
             #5, 5, 8, 4, 4, 8, 4, 7, 5, 5,
             #7, 6, 7, 5, 4, 6, 7, 6, 6, 6,
             #5, 6, 7, 8, 3, 5, 4, 3, 6, 7,
             #8, 6, 3, 8, 7, 7, 6, 6, 5]
    testL = ground[1:len(ground) - 1]

    # print(train_label)
    lin = LinearSVC(max_iter=3000)
    lin.fit(trainD, train_label)
    result = lin.predict(testD)
    # ===== Output functions ======
    print('estimated labels: ', result)
    print('ground truth labels: ', testL)
    print('Accuracy: ', lin.score(testD, testL) * 100, '%')

    result = np.asarray(result)
    result = np.insert(result,0,0)
    result = np.append(result,1)
    result = np.reshape(result,(n,n))

    print(result)
    return result




if __name__ == "__main__":
    pass
    #train(250,10,ground)








