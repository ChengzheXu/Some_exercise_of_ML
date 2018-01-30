import numpy as np
import pandas as pd
from sklearn import model_selection

def navive_bayesian(train, label, features):
    '''
    :param train: the training dataset, containning at least the label and the features
    :param label: the label of classes
    :param features: the features used to make the classification
    :return: prior prob of classes and the prob of feature condition on classes
    '''
    ylist = train[label]
    y = list(set(ylist))
    N = train.shape[0]
    N_class = [train.loc[train[label] == yy].shape[0] for yy in y]
    P_C = {yy:(train.loc[train[label] == yy].shape[0]+1)*1.0/(N+len(y)) for yy in y}
    #we use Laplasian correction to get the prior distribution of classes and sample conditional distribution
    prob_condition = {}
    for feature in features:
        prob_condition[feature] = {}
        for y0 in y:
            prob_condition[feature][y0] = {}
            for x in set(train[feature]):
                sample_subset = train.loc[(train[label] == y0)&(train[feature]==x)]
                class_subset = train.loc[train[label] == yy]
                P_x_c = (sample_subset.shape[0]+1)*1.0/(class_subset.shape[0]+len(set(train[feature])))
                prob_condition[feature][y0][x] = P_x_c
    return [P_C, prob_condition]

def prediction_nb(test, features, P_C, prob_condition, N_class):
    '''
    :param test: the testing dataset, containing all the features used in training step
    :param features: features used in training step
    :param P_C: the prior probability for the classes
    :param prob_condition: the probability of features conditional on the classes
    :param N_class: the count of each class used in the Laplasian correction step
    :return: the predicted class
    '''
    result = []
    for i in test.index:
        print(i)
        sample = test.loc[test.index == i]
        class_prob = {c:p for c,p in P_C.items()}
        for feature in features:
            dict1 = prob_condition[feature]
            for c in P_C.keys():
                cond_dict = dict1[c]
                xx = list(sample[feature])[0]
                if xx not in cond_dict:
                    class_prob[c] = class_prob[c] * 1.0/(N_class[c]+len(N_class))
                else:
                    class_prob[c] = class_prob[c]*cond_dict[xx]
        result.append(max(class_prob.items(), key=lambda x: x[1])[0])
    return result


data  = pd.read_csv('C:/Users/OkO/Desktop/金融数据分析/第2期/Notes/cust data.csv', header = 0, encoding='gb2312')

train, test = model_selection.train_test_split(data, test_size=0.4, random_state=0)

continue_var = ['term','limit','amt_in_acct','age']
for var in continue_var:
    x1 = train[var]
    mean = np.mean(x1)
    train[var] = train[var].map(lambda x: int(x<=mean))

    x1 = test[var]
    mean = np.mean(x1)
    test[var] = test[var].map(lambda x: int(x <= mean))


ind_var = ['monthly_saving','monthly_investment','monthly_insurance']
for var in ind_var:
    train[var] = train[var].map(lambda x: int(x>0))
    test[var] = test[var].map(lambda x: int(x > 0))

features = ['term','limit','amt_in_acct','no_of_loan','area','province','credit_level','gender','age','monthly_saving',
            'monthly_investment','monthly_insurance','credit_card']

[P_C, prob_condition] = navive_bayesian(train, 'classes', features)

ylist = train['classes']
y = list(set(ylist))
N_class = {yy: train.loc[train['classes'] == yy].shape[0] for yy in y}
pred = prediction_nb(test, features, P_C, prob_condition,N_class)

true = list(test['classes'])

precision = [int(pred[i]==true[i]) for i in range(len(true))]
