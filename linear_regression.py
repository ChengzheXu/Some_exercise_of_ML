def Linear_regression(data):
    x = sum(data.keys)/len(data.keys)
    y = sum(data.values)/len(data.values)
    k = (sum(map(lambda x:x[0]*x[1],data.items()))/len(data)-x*y)/(sum(map(lambda x:x**2,data.keys()))/len(data)-x**2)
    b = y - k*x
    return (k,b)
def Gradient_descent_linear_regression(data):
    x = sum(data.keys) / len(data.keys)
    y = sum(data.values) / len(data.values)
    x_y = sum(map(lambda x:x[0]*x[1],data.items()))/len(data)
    x_2 = sum(map(lambda x:x**2,data.keys()))/len(data)
    k,b = (eval(i) for i in input("Please initial the slope and intercept, devided by ','.\n").split(','))
    a = eval(input("Please enter the learning rate.\n"))
    e = eval(input("Please enter the max error.\n"))
    e0 = b + k*x - y
    e1 = b*x + k*x_2 - x_y
    while e0**2 + e1**2 >= e**2:
        b = b - a*e0
        k = k - a*e1
        e0 = b + k * x - y
        e1 = b * x + k * x_2 - x_y
    return (k,b)
def main(data):
    k1,b1 = Linear_regression(data)
    k2,b2 = Gradient_descent_linear_regression(data)
    print('''Regression by Linear Regression:
        y = %f +%f*x
        '''%(b1,k1))
    print('''Regression by Gradient descent linear regression:
            y = %f +%f*x
            ''' % (b2, k2))
    return None
