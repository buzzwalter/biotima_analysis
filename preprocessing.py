import scipy
from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt

def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    apply a low-pass Butterworth filter

    parameters:
        - data numpy array 1xN where N is the number of data points 
        - cutoff float indicating the cutoff frequency for the low-pass
        - fs float sampling rate, shouldn't be greater than twice the cutoff

    returns:
        - y 1xN numpy array of the filtered data.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def preprocess_data(df,verbose=False):
    '''
    main function for data processing.  Applies the Butterworth filter and coverts the signal to amicable units for emgfit processing.

    parameters:
        - df 2 column data frame associated with loaded data.  Has time in the first column and volts in the second.
        - verbose boolean for toggling the plots

    returns:
        - Nx2 np array with the microseconds in the first column and millivolts in the second column
    '''
    # Preprocess raw ToF data
    df['time'] = df['time']*1e6 ## covert to microseconds
    df['volts'] = df['volts']*(-1e3) # convert to inverted millivolts

    # Define the cutoff frequency as appropriate for your data
    cutoff_frequency = 1e3  # Adjust this based on your specific data
    sampling_rate = 10000  # Adjust based on your time series data sampling rate

    filtered_volts = butter_lowpass_filter(df['volts'], cutoff_frequency, sampling_rate)

    # Step 2 Fit a line using least squares
    time = df['time'].to_numpy()
    slope, intercept = np.polyfit(time, filtered_volts, 1)

    # Step 3: Subtract the fitted line from the original data
    fitted_line = slope * time + intercept
    corrected_volts = df['volts'] - fitted_line
    corrected_volts[corrected_volts <0] = 0 # remove negative counts
    
    # Step 4: Save the corrected data
    data = np.zeros((len(corrected_volts),2))
    data[:,0] = df['time'].to_numpy()
    data[:,1] = corrected_volts
    np.savetxt('./tmp/tmp_pre_processed.txt',data)

    if verbose:
        fig, ax = plt.subplots(figsize=(8,6))
        plt.plot(corrected_volts,alpha=0.5,c='b')
        plt.plot(df['volts'],alpha=0.5, c='r')
        plt.plot(fitted_line,c='teal')
        plt.legend(['corrected','original','fitted floor: $y = {:.4f}x + {:.4f}$'.format(slope,intercept)])
        plt.show()

    return data
