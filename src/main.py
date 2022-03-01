# Import packages
import sys
import logging
import logging.config
import pandas as pd

# Custom imports
import src.forecast_machine_price as cmodnet
import src.pre_processing_data as prep
import settings as s
import warnings

# TODO: Remove ignore warnings, solve reference issues.
warnings.filterwarnings("ignore")


def main():
    # Create logger
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
    logging.basicConfig(format=log_format, level=logging.INFO, stream=sys.stdout)
    logger = logging.getLogger()
    logger.info('Run machine price forecast tool - started')

    # Retrieve prepared machine data
    logger.info('Get prepared data - started')
    if s.bool_data_from_workset:
        data = prep.Prepare_Data()
        data = data.prepare_data()
    else:
        data = pd.read_pickle(s.path_data_folder + s.files['output_pairing'])
    logger.info('Get prepared data - finished')

    # Train the machine Forecast Model and Fit
    logger.info('Start Training and Fitting')
    data = cmodnet.ForecastModel(data)
    R2, RMSE, feature_performance=data.calculate()
    logger.info('RMSE: '+ RMSE.astype(str)  + ', R2: ' + R2.astype(str))
    logger.info('Finished Training and Predicting')

    # Write output data to csv
    logger.info('Export to file - started')
    file_path_local = s.path_data_folder + s.files["output_data"]
    feature_performance.to_csv(file_path_local, index=False)
    logger.info('Export to file - finished')
    logger.info('Run machine price forecast tool - finished')
    logger.info('')


if __name__ == '__main__':
    main()
