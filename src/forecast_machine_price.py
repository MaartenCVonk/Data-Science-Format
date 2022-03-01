import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
import logging.config

class ForecastModel:
    def __init__(self, data):
        """
        :param data:
        """
        self.logger = logging.getLogger(__name__)
        self.columns = ['Year Made','Machine Size','Model Description','Auctioneer ID', 'Model ID','Coupler']
        self.grou = list(data['Product Group'].unique())
        self.enc = list(data['Enclosure'].unique())
        self.hyd = list(data['Hydraulics'].unique())
        self.source = list(data['datasource'].unique())
        self.pro = list(data['Product Class Description'].unique())
        self.sou = list(data['State of Usage'].unique())
        self.feature_cols = list(set().union(self.columns,self.enc, self.hyd, self.source, self.grou, self.pro))
        self.data=data
        self.feature_performance = pd.DataFrame(columns={'Feature_name', 'Feature_importance'})

    def calculate(self):
        """
        This functions starts the calculation sequence activities for Machine Forecast Module
        :return:
        """
        self.logger.info("start training and predicting module")

        # Split the data set into train and test
        self.split_data()
        # train the model
        self.fit_model()
        # Make predictions after training
        self.predict_model()
        # Return the R2 ans RMSE performance of the model
        self.return_performance()
        # Return the performance of the individual features
        self.feature_scoring()

        return self.R2, self.RMSE, self.feature_performance

    def split_data(self):
        """
        Splits data into training and test (use 'rule of thumb' 4/5 for training)
        :return:
        """
        self.logger.info("start splitting data")
        X = self.data.loc[:, self.feature_cols]
        y = self.data.loc[:,'Sales Price']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=3)

    def fit_model(self):
        """
        Fit the model
        :return:
        """
        self.logger.info("start fitting model")
        # Set min_samples_split to prevent running out of memory error.
        model = RandomForestRegressor(min_samples_split=16)
        model.fit(self.X_train , self.y_train)
        self.model=model

    def predict_model(self):
        """
        Make predictions with the trained model.
        """
        self.logger.info("start predicting model")
        self.y_test_predict = self.model.predict(self.X_test)

    def return_performance(self):
        """
        Return overal performance in the form of RMSE and R2 score.
        """
        self.logger.info("start returning performance")
        self.RMSE = (np.sqrt(mean_squared_error(self.y_test, self.y_test_predict)))
        self.R2 = (r2_score(self.y_test, self.y_test_predict))

    def feature_scoring(self):
        """
        Return feature performance by inbuilt function.
        """
        self.logger.info("start returning feature scoring")
        feature_performance = self.feature_performance
        feature_performance['Feature_importance'] = self.model.feature_importances_
        for i in range(0,len(feature_performance)):
            feature_performance.loc[i,'Feature_name']=self.X_train.columns[i]

        self.feature_performance=feature_performance

