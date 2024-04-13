from utils import *
from preprocessing import *
from calibration import *
from analysis import *

def main():
    # Load raw data
    raw_data = DataLoader.load_data()
    
    # Preprocess data
    preprocessed_data = preprocess_data(raw_data)
    
    # Calibrate data
    calibrated_data = calibrate_data(preprocessed_data)
    
    # Analyze data
    analysis_results = analyze_data(calibrated_data)
    
    # Save results
    DataSaver.save_data(analysis_results)
    
    log_message("Analysis completed successfully.")

if __name__ == "__main__":
    main()