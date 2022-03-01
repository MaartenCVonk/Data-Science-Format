import pandas as pd
import numpy as np
import settings as s
import src.categories_mapping as p
import logging.config

class Prepare_Data:
    def __init__(self):
        """
        :param :
        :param :
        """
        self.logger = logging.getLogger(__name__)
        self.data = pd.read_csv(s.path_data_folder + s.files['input_data'], sep=",")

    def prepare_data(self):
        """
        This functions starts the pre processing activities for the machine price Forecasting Algorithm
        :return:
        """
        self.logger.info("start preprocessing data")

        # Add all the pairings as nodes in the
        self.prepare_initial_data()
        # Add all the pairings as nodes in the
        self.deal_with_missing_data()
        # Create connectivity matrix variable for the assignment
        self.categorical_variables_mapping()
        # Start the calculations of the connections
        return self.data

    def prepare_initial_data(self):
        """
        This functions starts collecting the data and make minor modifications/corrections.
        :return:
        """

        self.logger.info("start initiating data")
        data = self.data

        # Eliminate all rows where there is no sales price present
        data=data[data['Sales Price']>0]

        # Convert dates to datetime values
        data['Sales date']=data['Sales date'].apply(pd.to_datetime)

        # Year value was incorrect cause no machine was made in year 1000. Replace those by nans
        data['Year Made'] = data['Year Made'].replace(1000, np.nan)
        data['datasource'] = data['datasource'].replace(173, data['datasource'].mode()[0])

        self.data=data

    def deal_with_missing_data(self):
        """
        This functions starts collecting the data and make minor modifications.
        :return:
        """

        self.logger.info("deal with missing data")
        data = self.data

        # For integer column values which are almost complete, fill by mean
        data['Year Made'].fillna(data['Year Made'].mean().round(), inplace=True)

        # For categorical column values which are almost complete, fill by mode
        data['Hydraulics'].fillna(data['Hydraulics'].mode()[0], inplace=True)
        data['Enclosure'].fillna(data['Enclosure'].mode()[0], inplace=True)
        data['Machine Size'] .fillna(data['Machine Size'].mode()[0], inplace=True)
        data['Auctioneer ID'].fillna(data['Auctioneer ID'].mode()[0], inplace=True)
        data['Coupler'].fillna(data['Coupler'].mode()[0], inplace=True)

        # For using one-hot decoding we need to make sure the created binary columns will still be unique
        data['datasource'] = 'D'+data['datasource'].astype(str)

        self.data = data

    def categorical_variables_mapping(self):
        """
        Basic strategy: 'modified' label encoding for ordered categoricals
                        one hote decoding for unordered (many unique values) categoricals
        For some categorical values with many unique values, we compute the hierarchy by taking
        the mean of the sales price per category.

        :return:
        """

        self.logger.info("start mapping categorical data")
        data=self.data

        # Map data with predefined mapping (ordinals categoricals)
        data['Usage Band']=data['Usage Band'].map(p.usage_band)
        data['Machine Size'] = data['Machine Size'].map(p.size)
        data['Coupler'] = data['Coupler'].map(p.coupler)
        data['Model Description'] = data['Model Description'].map(p.create_hierarchy_dict(data,'Model Description'))
        data['Auctioneer ID'] = data['Auctioneer ID'].map(p.create_hierarchy_dict(data, 'Auctioneer ID'))

        # One hot Decoding for some features because they do not contain extremely many unique values
        # Map data without predefined mapping (no-order categoricals)
        data = pd.concat([data, pd.get_dummies(data['Enclosure'])], axis=1)
        data = pd.concat([data, pd.get_dummies(data['Hydraulics'])], axis=1)
        data = pd.concat([data, pd.get_dummies(data['datasource'])], axis=1)
        data = pd.concat([data, pd.get_dummies(data['Product Group'])], axis=1)
        data = pd.concat([data, pd.get_dummies(data['Product Class Description'])], axis=1)

        self.data=data


if __name__ == '__main__':
    prepared_data = Prepare_Data()
    prepared_data.prepare_data()
