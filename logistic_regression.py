from numpy import *
import math
def HypothesisFunction(x,theta):
    '''This is a linear model.
    x and theta are two vectors(array).
    return a function value.
    '''
    return 1/(1+math.exp(-inner(x,theta)))

class SigmoidNode(object):
    '''X and y are the data-set, X is a feature matrix(array), y is a label vector(array).
    lamb is the regularization parameter. alpha is the learning rate.
    theta is the initialed hypothesis parameter.
    times is the iterations of Gradient-Decent. minerror is the min error allowed.
    The regularization term would use square.
    '''
    def __init__(self,X,y,alpha,theta,times,minerror,lamb=0):
        self.X = X
        self.y = y
        self.alpha = alpha
        self.theta = theta
        self.times = times
        self.minerror = minerror
        self.lamb = lamb
    def CostFunction(self):
        '''return a function value.
        '''
        return -sum([self.y[i] * log(HypothesisFunction(self.X[i], self.theta)) + (1 - self.y[i]) * log(1 - HypothesisFunction(self.X[i], self.theta)) \
                     for i in range(len(self.y))]) / len(self.y) + self.lamb * (inner(self.theta, self.theta) - self.theta[0] ** 2) / (2 * len(self.y))
    def GradientDecent(self):
        '''cauculate the best theta.
        return the cost-function.
        '''
        circle = 0
        '''convergeflag = 0'''
        while circle < self.times:
            circle += 1
            delta = self.alpha * self.CostGradient()
            self.theta -= delta
            '''if inner(delta, delta) < self.minerror ** 2:
                convergeflag = 1
                break
        print("Converge completed!\n" if convergeflag else "Converge imcompleted!\n")'''
        return self.CostFunction()
    def CostGradient(self):
        '''return an array.
        '''
        return array(list(map(sum, zip(*[(HypothesisFunction(self.X[i], self.theta) - self.y[i]) * self.X[i] for i in range(len(self.y))])))) / len(self.y) \
               + array([0] + list(self.theta)[1::]) * self.lamb / len(self.y)
    def Predict(self,x):
        '''return P{y(x)==1}
        '''
        self.GradientDecent()
        return HypothesisFunction(x, self.theta)

X = array([[1,0,9],[1,2/3,4],[1,2,1/2],[1,1/3,7],[1,5/3,7],[1,2,5],[1,0,6],[1,0,0]])
y = array([1,0,0,1,1,1,0,0])
theta = array([0.,0.,0.])
A = SigmoidNode(X,y,0.006,theta,35000,0.001)
print("Cost is",A.GradientDecent())
print(theta)
