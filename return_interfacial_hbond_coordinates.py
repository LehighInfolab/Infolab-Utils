#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def extract_lists(half1_dict, half2_dict):
    '''Returns 2 lists of tuples containing only the apex atom coordinates for both dictionaries'''
    half1_list = []
    half2_list = []
    
    # iterate over each key-value pair in half1_dict
    for value in half1_dict.values(): # where did we define half1_dict?
        # extract the first tuple from the value and append it to half1_list
        half1_list.append(value[0]) # add the 1st value within half1_dict to half1_list
    
    # iterate over each key-value pair in half2_dict
    for value in half2_dict.values():
        # extract the first tuple from the value and append it to half2_list
        half2_list.append(value[0]) # add the 1st value within half2_dict to half2_list
    
    return half1_list, half2_list


def eliminate_triplets(list1, list2, hbond_distance_cutoff):
    '''Computes the pairwise distance between all atomic coordinates in list1 and list2
    and returns lists of only those x,y,z coordinates that are within the the pariwise 
    distance cut off'''

    # Convert the input lists to a 2-dimensional numpy array
    list1 = np.array([list(map(float, tup)) for tup in list1])
    list2 = np.array([list(map(float, tup)) for tup in list2])

    # Calculate pairwise distances between all elements of list1 and list2
    distances = pairwise_distances(list1, list2)

    # Identify indices where the distance is less than or equal to the cutoff value * 2
    indices = np.where(distances <= hbond_distance_cutoff*2)

    # Extract the corresponding elements from list1 and list2 based on the identified indices
    result1 = list1[indices[0]]
    result2 = list2[indices[1]]

    return result1, result2, distances

