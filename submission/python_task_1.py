import pandas as pd
import  numpy as np


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix


dataset_1 = pd.read_csv('C:\\Users\MSI\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')

result_matrix = generate_car_matrix(dataset_1)
print(result_matrix)
    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    
    type_counts = df['car_type'].value_counts().to_dict()

    
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts


dataset_1 = pd.read_csv('C:\\Users\\MSI\\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')

result_type_counts = get_type_count(dataset_1)
print(result_type_counts)
    


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """

    bus_mean = df['bus'].mean()

    
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    
    sorted_bus_indexes = sorted(bus_indexes)

    return sorted_bus_indexes


dataset_1 = pd.read_csv('C:\\Users\\MSI\\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')

result_bus_indexes = get_bus_indexes(dataset_1)
print(result_bus_indexes)





def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
   
    route_avg_truck = df.groupby('route')['truck'].mean()

    
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    
    sorted_selected_routes = sorted(selected_routes)

    return sorted_selected_routes


dataset_1 = pd.read_csv('C:\\Users\\MSI\\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv')

result_routes = filter_routes(dataset_1)
print(result_routes)

   


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    
    modified_matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    
    rounded_matrix = modified_matrix.round(1)

    return rounded_matrix


result_matrix = generate_car_matrix(pd.read_csv('C:\\Users\\MSI\\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-1.csv'))
modified_matrix = multiply_matrix(result_matrix)
print(modified_matrix)


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    
def time_check(file_path):
 
    
    df = pd.read_csv(file_path)

   
    time_data = df[['id', 'id_2', 'startDay', 'startTime', 'endDay', 'endTime']].copy()

    
    time_data['start_datetime'] = pd.to_datetime(time_data['startDay'] + ' ' + time_data['startTime'], format="%A %H:%M:%S")
    time_data['end_datetime'] = pd.to_datetime(time_data['endDay'] + ' ' + time_data['endTime'], format="%A %H:%M:%S")

    
    time_data['duration'] = time_data['end_datetime'] - time_data['start_datetime']

    
    time_check_result = (
        (time_data['duration'] >= pd.Timedelta(hours=24)) &
        (time_data['start_datetime'].dt.day_name().isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])) &
        (time_data['end_datetime'].dt.day_name().isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
    )

    
    df.loc[:, 'time_check_result'] = time_check_result

    
    result_series = df.groupby(['id', 'id_2'])['time_check_result'].all()

    return result_series


result_series = time_check('C:\\Users\\MSI\\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-2.csv')
print(result_series)

