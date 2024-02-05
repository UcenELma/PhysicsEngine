"""
Analyse absorption data.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
import sys
#############################################################################

def main():
    # -- Import data --
    data = np.loadtxt(str(sys.argv[1]), skiprows=1, delimiter=',')
    cycle = int(sys.argv[2]) # time per cycle
    
    # -- Transpose data matrix --
    vis = float(sys.argv[3])
    d1 = np.array([])
    n1 = np.array([])
    d2 = np.array([])
    n2 = np.array([])
    for meas in data:
        if meas[0] < vis:
            d1 = np.append(d, meas[0])
            n1 = np.append(n, meas[1])
        else:
            d2 = np.append(d, meas[0])
            n2 = np.append(n, meas[1])

    # -- Get cut-off --
    fit1 = np.polyfit(d1, np.log(n1), 1, cov=False)
    fit2 = np.polyfit(d2, np.log(n2), 1, cov=False)
    cutoff = (fit2[0] - fit1[0])/(fit1[1] - fit2[1])
    print(cutoff)
    
    # -- Plot d-n --
    yerr_dn = np.sqrt(n*cycle) / cycle # errors from histogram
    plt.plot(d1, np.log(n1), 'o')
    plt.plot(d2, np.log(n2), 'o')
    plt.plot(cutoff, 0, 'o')
    plt.errorbar(x=d, y=n, xerr=0.1, yerr=yerr_dn, fmt='none')
    plt.show()



if __name__ == "__main__":
    main()