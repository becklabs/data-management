import matplotlib.pyplot as plt

def summary_stats(x):
    x = sorted(x)
    
    #MEAN CALC
    mean = sum(x)/len(x)
    
    #MEDIAN CALC
    i = len(x)
    if i%2 == 0:
        median = (x[int(i/2)]+x[int(i/2 - 1)])/2
    else:
        median =  x[int((i-1)/2)]
    
    #IQR CALC
    q1 = (x[0]+median)/2
    q3 = (x[-1]+median)/2
    IQR = q3 - q1
    
    return mean, median, IQR
    
def circle_params(data):
    xs = [i[0] for i in data]
    ys  =[i[1] for i in data]
    meanx, medianx, IQRx = summary_stats(xs)
    meany, mediany, IQRy = summary_stats(ys)
    radius = 1.5*((IQRx+IQRy)/2)
    return (meanx, meany), (medianx, mediany), radius

def draw(xs, ys):
    data = [(xs[i],ys[i]) for i in range(len(xs))]
    meanpoint, medianpoint, radius = circle_params(data)
    print(meanpoint, radius)
    mean_circle = plt.Circle(meanpoint, radius, color='r', fill=False)
    median_circle = plt.Circle(medianpoint, radius, color='b', fill=False)
    ax = plt.gca()
    ax.set_xlim((meanpoint[0]-radius*3,meanpoint[0]+radius*3))
    ax.set_ylim((meanpoint[1]-radius*2),(meanpoint[1]+radius*2))
    ax.add_patch(mean_circle)
    ax.add_patch(median_circle)
    for point in data:
        ax.plot(point[0],point[1], 'o')
