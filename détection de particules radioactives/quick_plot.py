"""
Plot histogram of DAQ output.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit
from scipy.special import gamma
#############################################################################

def main():
    data = np.loadtxt(str(sys.argv[1])) # load data file

    bin_height, bin_edge, _ = plt.hist(data, int(sys.argv[2])) # create histogram
    plt.xlabel("Counts per cycle")
    plt.ylabel("Number of cycles")
    plt.title("Histogram of " + str(sys.argv[1]))

    bin_mid = [0.5*(bin_edge[i] + bin_edge[i+1]) for i in range(len(bin_edge) - 1)]
    bin_mid = bin_mid
    bin_height = bin_height
    plt.plot(bin_mid, bin_height, 'o')
    print(bin_height)

    lamb, cov = curve_fit(poisson, bin_mid, bin_height, p0=[5])

    x = np.linspace(bin_edge[0], bin_edge[-1], int(sys.argv[2])*20)
    plt.plot(x + (bin_mid[0] - bin_edge[0]), [poisson(m, lamb)*len(data)*2 for m in x], label="Poisson fit")
    print(lamb)

    plt.legend()
    plt.show()

def poisson(x: int, lamb) -> float:
    return (np.abs(lamb)**x)/(gamma(x+1)) * np.exp(-lamb)

if __name__ == "__main__":
    main()