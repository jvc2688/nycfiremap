import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cross_validation
import itertools
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn import linear_model, datasets
from sklearn import preprocessing


class FirePredictor():
    def __init__(self, model, X_train, y_train, X_test, y_test f_names):
        self.model = model
        self.scale = preprocessing.StandardScaler().fit(X_train)
        self.update(X_test, y_test)
        self.f_names = f_names
        X_scale = self.scale.transform(X_train)
        self.model.fit(X_scale, y_train)

        self.class_names = ['no fire','fire']

    def update(X_test, y_test):
        self.X_test = self.scale.transform(X_test)
        self.y_test = y_test
        self.y_pred = self.model.predict(self.scale.transform(self.X_test))
        self.y_prob = self.model.predict_proba(self.scale.transform(self.X_test))[:,1]
        self.auc = roc_auc_score(self.y_test, self.y_pred)

    def plot_roc_curve():
        plt.figure(figsize=(4,5))
        fpr, tpr, thresholds = metrics.roc_curve(self.y_test, self.y_prob, pos_label=1)
        plt.plot(np.arange(10)/9., np.arange(10)/9.)
        plt.plot(fpr,tpr)
        plt.xlabel('False Positive')
        plt.ylabel('True Positive')
        plt.title('AUC={0:.2f}'.format(self.auc))

    def plot_confusion_matrix(normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):

        cm = confusion_matrix(self.y_test, self.y_pred)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(self.class_names))
        plt.xticks(tick_marks, self.class_names, rotation=45)
        plt.yticks(tick_marks, self.class_names)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    def feature_importance(self):
        X_test_scale = self.scale.transform(X_test)
        importances_scaled_sign = np.std(X_test_scale,axis=0)*self.model.coef_[0]
        importances_scaled = abs(np.std(X_test_scale,axis=0)*self.model.coef_[0])

        indices_scaled = np.argsort(importances_scaled)[::-1]
        print("Feature ranking:")
        for i in range(X_test_scale.shape[1]):
            print("{0}. feature: {1} {2}".format(i + 1, self.f_names[indices_scaled[i]],\
                                            importances_scaled_sign[indices_scaled[i]]))



if __name__ == '__main__':
    print('FirePredictor')