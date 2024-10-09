import os 
import numpy as np
from sklearn.metrics import f1_score, recall_score, precision_score, multilabel_confusion_matrix
true_labels =[]
pre_labels=[]
sum_true = 0
len_labels = 0
# file_ = open('pre_true_tina.txt','w')
# file_false = open('pre_false_tina.txt','w')

# for file in os.listdir('plate_results_tina'):
#   len_labels += 1
#   if 'trans' in file :
#     name = file.split('_trans')[0]+ '.txt'
#   else:
#     name = file 
#   label_txt = open(f'label_LPs/{name}', 'r').read().splitlines()
#   true_label = ''
#   for line in label_txt:
#     true_label+=line
#   true_labels.append(true_label)
#   pre_label_txt = open(f'plate_results_tina/{file}').read().splitlines()
#   pre_labels.append(pre_label_txt[0])
    
#   if(pre_label_txt[0] == true_label):
#     sum_true += 1
#     # file_.write(file +'\n')
#   else:
    # file_false.write(file+ '\n')
# print(float(sum_true/len_labels))
# print(sum_true)
# print(len_labels)
# lst =[]
# sum = 0
# with open('pre_true_tina.txt','r') as f:
#   for line in f:
#     lst.append(line)  
# with open('pre_true_rotate.txt','r') as f:
#   for line in f:
#     if line in lst :
#       sum += 1
    
# print(sum)



with open('test_rotate','r') as f:
  for _line in f:
    len_labels += 1

    _line = _line.replace("\n",'')
    if 'trans' in _line :
      name = _line.split('_trans')[0]+ '.txt'
    else:
      name = _line
    
    label_txt = open(f'label_LPs/{name}', 'r').read().splitlines()
    true_label = ''
    for line in label_txt:
      true_label+=line
    true_labels.append(true_label)
    pre_label_txt = open(f'plate_results/{_line}').read().splitlines()
    pre_labels.append(pre_label_txt[0])
    if(pre_label_txt[0] == true_label):
      sum_true += 1
#define array of actual classes
actual = np.array(true_labels)

#define array of predicted classes
pred = np.array(pre_labels)
#calculate F1 score
 
rs = recall_score(y_true=actual, y_pred=pred, average='weighted')

ps = precision_score(y_true=actual, y_pred=pred, average='weighted')


f1_Score=f1_score(y_true=actual, y_pred=pred, average='weighted')

cm = multilabel_confusion_matrix(actual, pred)
print('True positive = ', cm[0][0])
print('False positive = ', cm[0][1])
print('False negative = ', cm[1][0])
print('True negative = ', cm[1][1])  
print(float(sum_true/len_labels))
print(sum_true)
print(len_labels)
print(f1_Score)
print(rs)
print(ps)
      
  
  
      

