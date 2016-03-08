from sklearn import svm

def data_build_up(filename):
    data = []
    label = []
    reader = open(filename, 'r')
    for line in reader:
        line = line[0:len(line)-1]
        features = line.split(' ')
        data.append(features[1:len(features)-1])
        features.append(features[len(features)-1])
        label.append(features[-1])
    return data, label

def svm_func():
    train_data, train_label = data_build_up('input')
    test_data, test_label = data_build_up('predict')

    clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
    clf.fit(train_data, train_label)
    count = 0
    for i, feature in enumerate(test_data):
        pre = clf.predict(feature)
        if pre == test_label[i]:
            count += 1
    print(float(count)/len(test_label))

svm_func()
