import matplotlib.pyplot as plt
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
import numpy as np
from itertools import cycle
from sklearn.metrics import confusion_matrix, roc_curve, auc
import itertools

class Ploty(object):
    @staticmethod
    def plot_history(history):
        # if not isinstance(history, keras.callbacks.History):
        #     return f"{history} is not a valid keras.callbacks.History"
        metrics = [v for v in history.history.keys() if not v.startswith('val')]
        
        fig, ax=plt.subplots(1, len(metrics), figsize=(20,5))
        
        for n, metric in enumerate(metrics):
            plt.subplot(1,len(metrics),n+1)
            plt.plot(history.epoch, 
                    history.history[metric],
                    color=colors[0],
                    linestyle="-",
                    linewidth='3',
                    label='Training')
            
            val_metric = f"val_{metric}"
            if val_metric in history.history.keys():
                plt.plot(history.epoch,
                        history.history[val_metric],
                        color=colors[1],
                        linestyle="-",
                        linewidth='3',
                        label='Validation')
            
            plt.xlabel('EPOCH', fontsize=18)
            plt.ylabel(metric.upper(), fontsize=18)
            plt.subplots_adjust(wspace=.15, hspace=.2)

            fig.tight_layout()
            plt.legend()

    @staticmethod
    def confusion_matrix(y_true, y_pred, target_name=None, Normalize=False, file_name=None):
        """
        cm:         : confusion matrix
        Target_Name : array-like with class names ['a','b','c'] or ohe.categories_[0]
        Normalize   : If False, plot the raw numbers
                    If True, plot the proportions
        file_name   : file name to save current figure in JPG format
        """

        cm = confusion_matrix(y_true.argmax(axis=1), y_pred.argmax(axis=1))

        fig, ax = plt.subplots(figsize=(10, 5))
        plt.imshow(cm, interpolation='nearest', cmap=plt.get_cmap('Blues'))
        plt.colorbar()
        
        if Normalize:
            # normalize the confusion matrix data by dividing its values over sum of rows
            cm = cm.astype('float') / cm.sum(axis=1)
            threshold = cm.max() / 1.5
        else:
            threshold = cm.max() / 2
        
        if target_name is not None:
            tricks = np.arange(len(target_name))
            plt.xticks(tricks, target_name)
            plt.yticks(tricks, target_name)

        for x, y in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if Normalize:
                plt.text(y, x, "{:.4f}".format(cm[x,y]),
                        horizontalalignment="center", color="white" if cm[x,y] > threshold else "black")
            else: 
                plt.text(y,x, "{0}".format(cm[x, y]),
                        horizontalalignment="center", color="white" if cm[x,y] > threshold else "black")

        plt.title('Confusion Matrix', fontsize=10)
        plt.ylabel('True Label', fontsize=10)
        plt.xlabel('Predicted label', fontsize=10)
        if file_name is not None:
            plt.savefig(file_name,format="jpg")
        plt.show()

    @staticmethod
    def plot_roc_curve(y_true, y_pred, file_name=None):
        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        lw = 2
        n_classes = y_pred.shape[1]
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_pred[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        
        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_pred.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        
        # First aggregate all false positive rates
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

        # Then interpolate all ROC curves at this points
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

        # Finally average it and compute AUC
        mean_tpr /= n_classes

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        # Plot all ROC curves
        plt.figure(figsize=(6, 5))
        plt.plot(fpr["micro"], tpr["micro"],
                label='micro-average ROC curve (area = {0:0.2f})'
                    ''.format(roc_auc["micro"]),
                color='deeppink', linestyle=':', linewidth=4)

        plt.plot(fpr["macro"], tpr["macro"],
                label='macro-average ROC curve (area = {0:0.2f})'
                    ''.format(roc_auc["macro"]),
                color='navy', linestyle=':', linewidth=4)

        colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                    label='ROC curve of class {0} (area = {1:0.2f})'
                    ''.format(i, roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc="lower right")
        if file_name is not None:
            plt.savefig(file_name,format="jpg")
        plt.show()