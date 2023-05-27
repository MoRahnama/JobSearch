"""
n = int(input("please give a number : "))
print("before reverse your numeber is : %d" %n)
print(f"Addition by 10: {n + 10}")
print(f"Subtraction by 10 : {n - 10}")
print(f"Multiplication by 10: {n * 10}")
print(f"Division by 10: {n / 10}")
print(f"Floor division by 10: {n // 10}")
print(f"Modulus by 10: {n % 10}")
print(f"Exponentiation by 10: {n ** 10}") 
"""

def creating_gen(index): 
    months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']  
    yield months[index]  
    yield months[index+2]  
next_month = creating_gen(3)  
print(next(next_month), next(next_month)) 


n = int(input("please give a number : "))
print("before reverse your numeber is : %d" %n)
reverse = 0
while n!=0:
    reverse = reverse*10 + n%10       
    n = (n//10)
print("After reverse : %d" %reverse) 


import numpy  
#method 1  
array_1 = numpy.array([])  
print(array_1)  
#method 2  
array_2 = numpy.empty(shape=(3,3))  
print(array_2)  

import array  
a = [4, 6, 8, 3, 1, 7]  
print(a[-3])  
print(a[-5])  
print(a[-1])  


def fetch_traffic_signals_data(base_url, package):
    """
    Fetch traffic signals data from CKAN API using package data.
    """
    for resource in package["result"]["resources"]:
        if resource["datastore_active"]:
            url = base_url + "/datastore/dump/" + resource["id"]
            traffic_signals = pd.read_csv(url)
            break
    return traffic_signals

def my_funstion(input):
    """
    This is my function
    """
    for 

def main():
    # Fetch and process traffic collision data
    gdf = fetch_collision_data(COLLISION_DATA_URL)
    gdf = extract_lat_lon(gdf)

    # Fetch and process traffic signals data
    package_data = fetch_package_data(TORONTO_OPEN_DATA_API, TRAFFIC_SIGNALS_PACKAGE_ID)
    traffic_signals = fetch_traffic_signals_data(TORONTO_OPEN_DATA_API, package_data)
    traffic_signals = process_traffic_signals_data(traffic_signals)

    # Calculate the distance from each traffic collision event to the nearest traffic signal
    gdf = calculate_distance_to_nearest_signal(gdf, traffic_signals)

    # Visualize the data
    plot_collision_density_map(gdf)
    plot_collision_histogram(gdf)

if __name__ == "__main__":
    main()