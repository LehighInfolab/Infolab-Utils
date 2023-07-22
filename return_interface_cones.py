#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def parse_cones_file(pathname, dictionary, switch):
    '''Parses a .cones file and returns a formatted dictionary of all of its cones'''
    pathname = pathname.strip() # eliminate embedded null character
    if switch == "acceptorCones": # ACCEPTOR
        with open(pathname, 'r') as f:
            for line in f:
                if line.startswith("CONES:"): #why do we skip lines starting with 'cones'? 
                    break
            for line in f:
                coors = line.strip().split() # removes any leading and trailing whitespaces and split the resulting string
                key = line.strip().split('[')[1][:-14] 
                apex = tuple(coors[0:3])
                perp_vec = tuple(coors [3:6])
                dictionary['ACCEP ' + key] = [apex, perp_vec]
    else: # DONOR 
        with open(pathname, 'r') as f:
            for line in f:
                if line.startswith("CONES:"):
                    break
            for line in f:
                coors = line.strip().split()
                apex = tuple(coors[0:3])
                perp_vec = tuple(coors [3:6])
                key = line.strip().split("180.0")[1][12:]
                dictionary['DONOR ' + key] = [apex, perp_vec]
    return dictionary

def return_condensed_dicts(half1_dict, half2_dict, half1_interface_atoms, half2_interface_atoms):
    # Create empty dictionaries to store the filtered key-value pairs
    new_half1_dict = {}
    new_half2_dict = {}
    
    # Extract the tuples from the interface atoms arrays
    half1_tuples = set(map(tuple, half1_interface_atoms)) # where are we getting these data from?
    half2_tuples = set(map(tuple, half2_interface_atoms))
    
    # Loop over the key-value pairs in half1_dict
    for key, value in half1_dict.items():
        if tuple(map(float, value[0])) in half1_tuples:
            new_half1_dict[key] = value
    
    # Loop over the key-value pairs in half2_dict
    for key, value in half2_dict.items():
        if tuple(map(float, value[0])) in half2_tuples:
            new_half2_dict[key] = value
    
    return new_half1_dict, new_half2_dict

