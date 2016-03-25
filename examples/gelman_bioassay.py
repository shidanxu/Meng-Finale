from pymc3 import *
from numpy import ones, array
import theano.tensor as t

# Samples for each dose level
n = 5 * ones(4, dtype=int)
# Log-dose
dose = array([-.86, -.3, -.05, .73])

def tinvlogit(x):
    return t.exp(x) / (1 + t.exp(x))

with Model() as model:

    # Logit-linear model parameters
    alpha = Normal('alpha', 0, 0.01)
    beta = Normal('beta', 0, 0.01)

    # Calculate probabilities of death
    theta = Deterministic('theta', tinvlogit(alpha + beta * dose))

    # Data likelihood
    deaths = Binomial('deaths', n=n, p=theta, observed=[0, 1, 3, 5])

    step = NUTS()

def run(n=1000): 
    if n == "short":
        n = 50
    with model:
        trace = sample(n, step)

if __name__ == '__main__':
    run()


