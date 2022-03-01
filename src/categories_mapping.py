
# Usage_ Band
usage_band = dict()
usage_band['Low'] = 1  # Usage band with lowest sales value
usage_band['Medium'] = 2  # Usage band with middle sales value
usage_band['High'] = 3  # Usage band with highest sales value

# Coupler
coupler = dict()
coupler['None or Unspecified'] = 1  # None is the weakest coupler
coupler['Manual'] = 2  # Manual is a mediocre coupler
coupler['Hydraulic'] = 3  # Hydraulic is a good coupler


# Machine Size
size = dict()
size['Mini'] = 1  # Mini has lowest sales price (mean)
size['Compact'] = 2  # Compact has almost the lowest sales price (mean)
size['Small'] = 3  # Small has almost the lowest sales price (mean)
size['Large'] = 4  # Large has high sales value
size['Medium'] = 5  # Medium has high sales value
size['Large / Medium'] = 6  # Large / Medium has highest sales value

# More Generic


def create_hierarchy_dict(data, column):
    """
    Create dictionary that contains an ordinal from categorical column value to integer
    based on the relation of that value to the sales price
    """
    sorted_values = data.groupby(column)['Sales Price'].mean().sort_values().reset_index()
    sorted_values['Mapping_Value'] = range(0,(len(sorted_values)))
    del sorted_values['Sales Price']
    # Return the desired mapping in a dict form
    return sorted_values.set_index(column).to_dict()['Mapping_Value']
