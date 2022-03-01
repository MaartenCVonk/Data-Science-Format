# Machine Prediction Calculator. 

This tool is created to predict the price of the machines. It consists of a pre 
processing stage, which uses data mappings from categories_mapping and a forecast
train and test phase. All phases are run from the main.py. The output is a feature 
importance csv, while the R2 and RMSE are displayed by the logger. 

Please look at the powerpoint to figure out why I made certain technical 
strategic choices.

### Prerequisites

Package requirements are contained in the requirement.txt. Since there was trouble running pipreqs, I created this manually. 

### Installing

#####Adjust the path data folder in the settings file!
Make sure the AI_data.csv is in the required folder.


## Usage
Data exploration has been realized in a jupyter notebook, to be found in the 
notebook folder.

The code can be run from the main.py. Note that the only output of the model is
the csv which contains feature importance information.
 
The performance of the model in terms of R2 score and RMSE (root mean squared error)
is given by the logger in the main.py.

The results of the features importance are further analyzed in a notebook, to be found
in the notebook folder


The Pre Processing of the data happens in the pre_processing_data.py, where the imput
is the raw AI_data.csv and the output a pandas DataFrame where relevant pre processing
steps have been executed.
```python
import src.pre_processing_data as prep
data = prep.Prepare_Data()
data = data.prepare_data()
```
where pre_processing_data.py uses categories_mapping.py to import relevant predetermined
mappings of some of the categorical data to numeric. This has been predetermined 
by quick analyzes carried out in the jupyter notebook.

```python
import src.categories_mapping as p
data['Usage Band']=data['Usage Band'].map(p.usage_band)
data['Machine Size'] = data['Machine Size'].map(p.size)
data['Coupler'] = data['Coupler'].map(p.coupler)
data['Model Description'] = data['Model Description'].map(p.create_hierarchy_dict(data,'Model Description'))
data['Auctioneer ID'] = data['Auctioneer ID'].map(p.create_hierarchy_dict(data, 'Auctioneer ID'))
```

The core (train an predict) of the module can be called by
 
```python
import src.forecast_machine_price as cmodnet
# Train the machine Forecast Model and Fit
logger.info('Start Training and Fitting')
data = cmodnet.ForecastModel(data)
R2, RMSE, feature_performance=data.calculate()
logger.info('RMSE: '+ RMSE.astype(str)  + ', R2: ' + R2.astype(str))
logger.info('Finished Training and Predicting')
```

where the logger outputs the RMSE and R2. The feature importance is saved to a CSV.


### Recommended:

Read the readme for information about the code structure.

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Pycharm](https://www.jetbrains.com/pycharm//) - Python IDE

## Contributing

Please read

## Versioning

Not Applicable

## Authors

* **Maarten Vonk** - *Initial work*

## License

Not Applicable

## Acknowledgments

Bit 
