import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import leastsq


def mass_func(a,b,x):
    '''
    ToF fit function

    parameters:
        - a, double associated with the scaling from the ToF, generally modeled as 2qU/(md^2) 
        - b, offset from the voltage signal, generally considered t_0
        - x, input array 1xN associated with data points to evaluate at.  Should be time data.

    returns:
        - array 1xN associated with the output of the functional form
    '''
    return a*(x-b)**2

def mass_func_residual(p,x,t):
    '''
    residual associated with ToF function

    parameters:
        - p, list with two doubles for a and b to be passed to ToF fit function
        - x, input array 1xN associated with data points to evaluate at. Should be time data
        - t, target data associated with the ToF signal, 1XN array.  Should be masses.

    returns:
        - returns 1xN array associated with the difference between the mass function and the target data
    '''
    a,b = p
    sim = mass_func(a,b,x)
    return t-sim

def calibrate_data(data,calib_mass_list,calib_peak_times,verbose=False):
    """
    uses leastsq to establish ToF parameters associated with the mass_function from time data

    parameters:
        - data Nx2 array with time and voltage associated with our raw data, already preprocessed
        - calib_mass_list list of double calibration masses we use as target data
        - calib_peak_times list of double time values associated with raw data
        - verbose boolean for toggling graphs
    
    returns:
        - calibrated data Nx2 array with mass in the first column and voltage in the second.
    """
    # Apply calibration to preprocessed data
    t = calib_mass_list
    time_data = np.array(calib_peak_times)


    p_0 = [1e12,1e-5]
    pfit , pcov = leastsq(mass_func_residual,p_0,args=(np.array(time_data),t),full_output=1)[:2]

    if verbose:
        fig, axs = plt.subplots(figsize=(8, 6))
        axs.plot(np.array(time_data)*1e6,t,'.')
        axs.plot(np.array(time_data)*1e6,mass_func(pfit[0],pfit[1],time_data))
        title_string = "MCP 2.3a={0:.6E} and t_0 = {1:.6E}".format(*pfit)
        axs.set(xlabel='time(us)', ylabel = 'mass($\sqrt{amu}$)', title=title_string)
        plt.show()

    data[:,0] = mass_func(pfit[0],pfit[1],data[:,0]*1e-6)
    start_index = np.argmin(data[:,0])
    if verbose:
        plt.plot(data[start_index:start_index+30000,0],data[start_index:start_index+30000,1])
        plt.xlabel('amu/q')
        plt.show
    calibrated_data = np.vstack((data[start_index:start_index+30000,0],data[start_index:start_index+30000,1])).T
    np.savetxt('./tmp/tmp_calibrated_data.txt',calibrated_data)

    return calibrated_data
