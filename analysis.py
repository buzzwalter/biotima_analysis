import numpy as np
import emgfit as emg

def analyze_data(peak,window_size,threshold=8e-3):
    '''
    main function for analyzing peaks with emg fit

    parameters:
        - peak double associated with tabulated mass value of species we're calibrating our shape to
        - window_size double associated with half with width of the width around the peak which we want to process.
        - threshold double for peak detection threshold under emgfit second derivative 

    returns:
        - detected_peaks list containing masses of the peaks found within the mass of interest. Ideally should be one, but can sometimes resolve to isotopes. will depend on precision chosen
        - num_detection integer associated with detected_peaks list length
    '''
    # Analyze calibrated data to extract properties
    resolving_power = 1e4 # resolving power to use for shape parameter initialization
    m_start = peak - window_size/2 # low-mass cut off
    m_stop = peak + window_size/2 # high-mass cut off
    detected_peaks, detected_indices, num_detections = single_peak_analysis(peak,window_size,threshold)
    for detected_index, detected_peak in zip(detected_indices,detected_peaks):

        
        spec = emg.spectrum('./tmp/tmp_calibrated_data.txt',m_start=m_start,m_stop=m_stop,resolving_power=resolving_power)    


        spec.detect_peaks(thres=threshold,window='bartlett',window_len=9,width=1e-4)#2.25e-3,window_len=99,thres=10,plot_smoothed_spec=True,plot_2nd_deriv=True,plot_detection_result=True) 190	250.34	514.6	614.7	720.7	840.8	1008

        # look for peak in mass region and use as shape/fit calibrant.  If there are multiple, do and save multiple fits
        spec.determine_peak_shape(index_shape_calib=detected_index,x_fit_range=1.5)
        spec.fit_peaks(index_mass_calib=detected_index,x_fit_range=1.5)    

        spec.savefit('./results/spec_analysis_{detected_index}.csv')    

    return detected_peaks,num_detections

def single_peak_analysis(peak,window_size,threshold,precision=1.0):
    '''
    helper function for finding the peaks in the neighborhood of the peak of interest

    parameters:
        - peak double associated with tabulated mass value of species we're calibrating our shape to
        - window_size double associated with half with width of the width around the peak which we want to process.
        - threshold double for peak detection threshold under emgfit second derivative 
        - precision double associated with mass region around the peak that should be searched.  Directly controls how many peaks to look for.  Default is set to 1.0 for sub amu res ToF
    
    returns:
        - detected_peaks list containing masses of the peaks found within the mass of interest. Ideally should be one, but can sometimes resolve to isotopes.
        - indices in the spectrum table associated with these peaks
        - num_detection integer associated with detected_peaks list length
    '''
    resolving_power = 1e4 # resolving power to use for shape parameter initialization
    m_start = peak - window_size/2 # low-mass cut off
    m_stop = peak + window_size/2 # high-mass cut off
    spec = emg.spectrum('./tmp/tmp_calibrated_data.txt',m_start=m_start,m_stop=m_stop,resolving_power=resolving_power)
    spec.detect_peaks(thres=threshold,window='barlett',window_len=9,width=1e-4)
    detected_peaks = np.array([detected_peak.x_pos for detected_peak in spec.peaks])
    mask = np.logical_and(peak-precision<detected_peaks,detected_peaks<peak+precision)
    detected_indices = np.where(mask)
    num_detections = len(detected_indices)
    return detected_peaks, detected_indices, num_detections
    