import pandas as pd
import networkx as nx
from datetime import time, timedelta

def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], distance=row['distance'])
    
    result_matrix = nx.floyd_warshall_numpy(G, weight='distance')

    print("Distance Matrix:")
    print(pd.DataFrame(result_matrix, index=G.nodes, columns=G.nodes))

    return pd.DataFrame(result_matrix, index=G.nodes, columns=G.nodes)

def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    unrolled_data = []

    for id_start, distances in df.iterrows():
        for id_end, distance in distances.items():
            if id_start != id_end:
                unrolled_data.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance
                })

    return pd.DataFrame(unrolled_data)


df = pd.read_csv('C:\\Users\\MSI\\Downloads\\task\\sudharsun\\MapUp-Data-Assessment-F-main\\datasets\\dataset-3.csv')


result_matrix = calculate_distance_matrix(df)


unrolled_df = unroll_distance_matrix(result_matrix)

print("\nUnrolled DataFrame:")
print(unrolled_df)



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """

    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()


    lower_threshold = 0.9 * reference_avg_distance
    upper_threshold = 1.1 * reference_avg_distance


    result_df = df[(df['id_start'] != reference_id) & (df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]

    return result_df


reference_id = 1001400
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(f"\nIDs within 10% threshold of average distance for reference ID {reference_id}:\n")
print(result_within_threshold)



def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """

    df = df.copy()

    df['moto'] = 0.8 * df['distance']
    df['car'] = 1.2 * df['distance']
    df['rv'] = 1.5 * df['distance']
    df['bus'] = 2.2 * df['distance']
    df['truck'] = 3.6 * df['distance']

    df.drop(columns=['distance'], inplace=True)
    

    return df




df_with_toll_rates = calculate_toll_rate(unrolled_df)


print("\nDataFrame with Toll Rates:")
print(df_with_toll_rates)



    


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
   
def calculate_time_based_toll_rates(df):

    df = df.copy()


    if 'start_day' not in df.columns:
        df['start_day'] = 'Monday'
    if 'end_day' not in df.columns:
        df['end_day'] = 'Sunday'


    weekday_time_ranges = [
        (time(0, 0, 0), time(10, 0, 0)),   
        (time(10, 0, 0), time(18, 0, 0)),  
        (time(18, 0, 0), time(23, 59, 59))  
    ]

    weekend_time_ranges = [
        (time(0, 0, 0), time(23, 59, 59))  
    ]


    time_range_discounts = {
        'weekday': [0.8, 1.2, 0.8],
        'weekend': [0.7]
    }

    time_based_toll_rates = []


    for _, row in df.iterrows():

        day_type = 'weekday' if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'weekend'

  
        for start_time, end_time in weekday_time_ranges if day_type == 'weekday' else weekend_time_ranges:
            discount_factor = time_range_discounts[day_type][weekday_time_ranges.index((start_time, end_time))]
            start_datetime = timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)
            end_datetime = timedelta(hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)

  
            time_based_toll_rates.append({
                'id_start': row['id_start'],
                'id_end': row['id_end'],
                'distance': row['distance'],
                'start_day': row['start_day'],
                'start_time': start_datetime,
                'end_day': row['end_day'],
                'end_time': end_datetime,
                'moto': discount_factor * 0.8 * row['distance'],
                'car': discount_factor * 1.2 * row['distance'],
                'rv': discount_factor * 1.5 * row['distance'],
                'bus': discount_factor * 2.2 * row['distance'],
                'truck': discount_factor * 3.6 * row['distance']
            })

    time_based_toll_rates_df = pd.DataFrame(time_based_toll_rates, columns=[
        'id_start', 'id_end', 'distance', 'start_day', 'start_time', 'end_day', 'end_time', 'moto', 'car', 'rv', 'bus', 'truck'
    ])

    return time_based_toll_rates_df


time_based_toll_rates_df = calculate_time_based_toll_rates(unrolled_df)
print("\nDataFrame with Time-Based Toll Rates:")
print(time_based_toll_rates_df)
