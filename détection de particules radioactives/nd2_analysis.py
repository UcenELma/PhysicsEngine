"""
This version of the code was written by Elias Fink and Timothy Chew.

Analyse nd^2 data.
"""
#############################################################################
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
import sys
from scipy.integrate import quad
from scipy.stats import chi2
#############################################################################

def main():
    # -- Import data --
    data = np.loadtxt(str(sys.argv[1]), skiprows=1, delimiter=',')
    cycle = int(sys.argv[2]) # time per cycle
    
    # -- Transpose data matrix --
    d = np.array([])
    n = np.array([])
    for meas in data:
        d = np.append(d, (meas[0])/100)
        n = np.append(n, meas[1])
    
    # -- Plot d-n --
    yerr_dn = np.sqrt(n*cycle) / cycle # errors from histogram
    if False:
        plt.plot(d, n, 'o')
        plt.errorbar(x=d, y=n, xerr=0.1, yerr=yerr_dn, fmt='none')
        plt.show()
    
    # -- Calculate nd2 and account for effects --
    nd2 = n * (d**2)
    yerr_dnd2_1 = np.sqrt(n*30) / 30 * (d**2) # errors from histogram scaled to nd^2
    yerr_dnd2_2 = np.sqrt(n*60) / 60 * (d**2)

    att_fit, att_cov = op.curve_fit(exp, d[25:], nd2[25:], p0=[15, 2.6], sigma=3*yerr_dnd2_2[25:]*np.sqrt((1+0.25/d[25:]**2))) # attenuation
    _, p_att = chisq(nd2[40:], exp(d[40:], *att_fit), 0.8*yerr_dnd2_2[40:]*np.sqrt((1+0.25/d[40:]**2)))
    print("Attenuation", att_fit, p_att, att_cov)

    nps_fit, _ = op.curve_fit(lambda x, A: cs(x, A) + exp(x, *att_fit) - exp(0, *att_fit), d[:8], nd2[:8], p0=[5.5e5]) # non-point source
    _, p_nps = chisq(nd2[:10], cs(d[:10], *nps_fit), 3*yerr_dnd2_1[:10]*(1+0.02/d[:10]**2))
    print("Non-point source effect", nps_fit, p_nps)
    
    _, p_null = 1e9*np.array(chisq(nd2, np.linspace(13, 13, len(nd2)), 10*yerr_dnd2_2*np.sqrt((1+0.25/d**2))))
    print("Null hypothesis", p_null)
    
    # -- Plot d-nd2 and fit --
    d_fit = np.linspace(0, 1, 500)
    trans_nps = np.linspace(100, 100, 500)
    trans_att = np.linspace(0, 0, 500)
    plt.xlabel("$d \; [m]$")
    plt.ylabel("$nd^2 \; [m^2s^{-1}]$")
    plt.plot(d_fit, exp(d_fit, *att_fit), '-', color='green', label='Attenuation effect')
    plt.plot(d_fit, cs(d_fit, *nps_fit), '-',color='red', label='NPS effect')
    plt.plot(d_fit, cs(trans_nps, *nps_fit) - cs(d_fit, *nps_fit), '-', color='orange', label='Significance of NPS effect')
    plt.plot(d_fit, exp(trans_att, *att_fit) - exp(d_fit, *att_fit), '-', color='aqua', label='Significance of attenuation effect')
    plt.plot(d, nd2, 'o')
    plt.errorbar(x=d[:10], y=nd2[:10], xerr=0.00001, yerr=0.8*yerr_dnd2_1[:10]*(1+0.02/d[:10]**2), fmt='none', capsize=3)
    plt.errorbar(x=d[10:33], y=nd2[10:33], xerr=0.001, yerr=0.8*yerr_dnd2_1[10:33]*np.sqrt((1+0.25/d[10:33]**2)), fmt='none', capsize=3)
    plt.errorbar(x=d[33:], y=nd2[33:], xerr=0.001, yerr=0.8*yerr_dnd2_2[33:]*np.sqrt((1+0.25/d[33:]**2)), fmt='none', capsize=3)
    plt.legend()
    #plt.savefig("img_nd2.png", dpi=1000)
    plt.show()

# -- Account for attenuation --
def exp(x, A, k):
    return A * np.exp(-x/k)

def chisq(exp, obs, sig):
    chis = 0
    for i in range(len(exp)):
        chis += (exp[i] - obs[i])**2 / sig[i]**2
    return chis, chi2.pdf(chis, len(exp) - 1)
    

# -- Account for non-point source --
def cylindrical_source_integrand(p, r, a): # define geometry of cylindrical source
    #p - radial coordinate centred on the source
    #r - perpendicular distance from source to detector
    #a - side length of detector assuming square
    return (1/np.pi) * np.arctan(a/2 * r/(r**2 + p**2)) * 1/np.sqrt(1 + (2/a * (r**2 + p**2)/r)**2) * p * 2*np.pi

def cs(x, A): # predict count rate of source at distance x (A: activity)
    source_diameter = 0.010
    detector_length = 0.015
    #rho and width correspond to source_diameter and detector_length respectively
    return [A/(np.pi*source_diameter**2/4) * quad(cylindrical_source_integrand, 0, source_diameter/2, args=(i, detector_length))[0] for i in x] * x**2

if __name__ == "__main__":
    main()