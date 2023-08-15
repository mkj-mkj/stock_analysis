import numpy as np
import pylab 


def fn(x):
    return np.cos(np.sqrt(x))

def f(x):
    return 2 * (np.sqrt(x) * np.sin(np.sqrt(x)) + np.cos(np.sqrt(x))) - 1

a, b, n = 0, 2 * np.pi, 100

xs = np.linspace(a, b, n + 1)
h = (b - a) / n

ys = [None] * (n + 1)

ys[0] = f(a)
for i in range(n):
    ys[i+1] = ys[i] + h * fn(xs[i])

pylab.figure(figsize = (8,4))
pylab.plot(xs, ys, color='blue', label='Euler method')
pylab.plot(xs, f(xs), color='red', label = 'exact')

pylab.title("y' = cos(sqrt(x)) with y(0)=1")
pylab.xlabel("X")
pylab.ylabel("Y")
pylab.xlim(0, 7)
pylab.ylim(0, 2.5)
#pylab.xticks([0, 1, 2, 3, 4, 5, 6, 7])
#pylab.yticks([0.5, 1, 1.5, 2, 2.5])
pylab.grid(True)

pylab.legend(
    loc = 'best',
    fontsize = '10',
    shadow = False,
    edgecolor = 'black'
)

pylab.show()