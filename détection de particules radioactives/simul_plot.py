"""
Plot simulation of beams.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import sys
#############################################################################

def main():
    data = np.loadtxt(str(sys.argv[1]), skiprows=1, usecols=(0), delimiter=",") # load data file

    plt.hist(data, int(sys.argv[2])) # create histogram
    plt.xlabel("Energy deposited")
    plt.ylabel("Number of particles")
    plt.title("Histogram of " + str(sys.argv[1]))
    plt.show()


if __name__ == "__main__":
    main()