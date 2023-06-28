'''
Author: Grant Armstrong
Reproduced by: Theodore Guo
Date: 6/23/23

- Description -
`obtain_adjacency( )` and `obtain_coord( )`, work together to create an undirected hashmap of the triangle vertices
in the mesh described by .SURF files. 

Each row of the GEOMETRY section describes  vertices in the triangular mesh where the first 3 values correspond to the 
X, Y, Z coordinates of a vertex and the last 3 are visualization parameters. Each
row is indexed starting at zero.
 
Each row of the TOPOLOGY section describes edges between vertices where vertices are represented by their index. 
'''
import sys 
import numpy as np


def obtain_coord(filename): 
    '''
    Read and extract coordinate information from a .SURF file.

    This function opens the specified file in read mode, searches for the
    'GEOMETRY' section, and extracts the coordinate values from each vertex. The extracted
    coordinates are stored in a list. The function also calls another function, obtain_adjacency,
    to obtain the adjacency information for the vertices.
    
    Parameters:
    - filename (str): The name of the .SURF file to be processed.

    Returns:
    - coors (list): A list of vertex coordinate values, where each vertex is represented as a
      list of [x, y, z] coordinates.
    - hashmap (object): The result obtained by calling the obtain_adjacency function,
      representing the adjacency information.
    - length (int): The number of vertex lines found in the file.
    '''
    with open(filename, 'r') as f1:
      
        for line in f1:  
            if not line.strip().startswith("GEOMETRY"): # if line does not start with 'GEOMETRY', we ignore it and move on
                continue # continue to the next line of the current file
    
            length = int(line.split()[1]) # 2nd element becomes the length value
            for i in range(length):
                nextLine = next(f1) 
                coors.append(nextLine.split()[:3]) #OBTAIN COORDINATES [[x,y,z], ...] 
                #disregard the remaining 3 parameters because they are irrelevant to this script
            hashmap = obtain_adjacency(f1) # passing a filepoint to the next function. Reading continues where it left off
        f1.close()
    return coors, hashmap, length

def obtain_adjacency(filepointer):
    '''
    Extracts adjacency information from a file.

    This function reads the lines from the provided file pointer and extracts the adjacency
    information from the 'TOPOLOGY' section of the file. The adjacency information describes
    the edges or connections between triangular vertices.

    Parameters:
    - filepointer (file object): The file pointer to the file containing the topology information.

    Returns:
    - hashmap (dict): A dictionary representing the adjacency information, where each vertex is a key
      mapping to a set of neighboring vertices. There are N keys in hashmap where N  is the the number of vertices.
    '''
    hashmap = {}
    for line in filepointer.readlines(): # reads each line of the filepointer
        if line.strip().startswith("#"):
            continue # skip the header section before the topology information begins
        if line.strip().startswith("TOPOLOGY"):
            length = int(line.split()[1]) # 2nd element becomes the length value
        elif line not in ['\n', '\r\n']: # Use this regex to only process non-blank lines of the TOPOLOGY section
            [a,b,c] = line.strip().split()[:3] # assigning the first thee elements as a, b, c variables
            #activate the hash map
   
            if a not in hashmap.keys():
                hashmap[a] = set()
            if b not in hashmap.keys():
                hashmap[b] = set()
            if c not in hashmap.keys():
                hashmap[c] = set()
            # Hashmap is undirected. All vertices in a TOPOLOGY line are interconnected to form a complete triangle
            hashmap[a].add(b)
            hashmap[a].add(c) #{a:{b,c}, }
            hashmap[b].add(a)
            hashmap[b].add(c) #{b:{a,c}, }
            hashmap[c].add(a)
            hashmap[c].add(b) #{c:{a,b}, }
    return(hashmap)

def remove_nans(filename, coors, hashmap, length):
    ''' 
    This function reads the input file, reproduces its content line by line, and fixes any NaN values found in the first
    3 columns of the GEOMETRY section. The fix is achieved by calculating the mean coordinate value of all neighboring
    vertices within a one-hop distance for the vertex containing the NaN coordinate value. The fixed output is written to
    a new .SURF file with '_patched' appended to the original filename. This script was conceived as temporary fix to the
    deep rooted NaN production problem in genSurf, and remains the best available option.
    
    Parameters:
    - filename (str): The name of the input file to be processed.
    - coors (list): A list of coordinate values, where each coordinate is represented as a list of [x, y, z] values.
    - hashmap (dict): A dictionary representing the adjacency information, where each vertex is a key mapping to a set
      of neighboring vertices.
    - length (int): The number of vertices in the GEOMETRY section.

    Returns:
    Writes to a new .SURF file with '_patched' appended to the original filename
    '''
    g = open(filename.split(".")[0] + "_patched.SURF", "w")
    with open(filename, 'r') as f2:
        for line in f2:
            if not line.strip().startswith("GEOMETRY"): # writing the header to the output file
                g.write(line)
                continue
            g.write(line) # writing the GEOMETRY line to the output file
            for vertex_index in range(length): # loop through the GEOMETRY section
                nextLine = next(f2)
                if 'nan' not in nextLine.split(" ")[:3]:
                    g.write(nextLine) # writing the non-problematic lines to the output file
                else:
                    nan_index = nextLine.split(" ")[:3].index('nan') # finds the index of the nan in the first 3 columns
                    coordinates = []
                    # hashmap looks like { '7156' : ['10', '6597', '133'], }
                    for neighbor in hashmap[str(vertex_index)]:    # neighborhood look-up for the vertex containing NaN coordinate
                        if coors[int(neighbor)][nan_index] != 'nan': # finds the non-NaN coordiantes from the neighbors of the problematic vertex
                            coordinates.append(float(coors[int(neighbor)][nan_index])) # appends that coor value to the coordinate array
                    #write modified line to g
                    mean = str(round(np.mean(coordinates), 6)) # Averages the neighboring x, y, or z coordinates and rounds 
                    line_array = list(nextLine.split(" ")) # split nextLine by blank spaces and create a list of the elements
                    line_array[nan_index] = mean # replacing NAN value with mean value
                    print_me = ' '.join([str(elem) for elem in line_array])
                    g.write(print_me) # write the fixed line to the output file!
    f2.close()
                                                                                        
# Usage
coors = []
coors, hashmap, length = obtain_coord(filename = sys.argv[1])
remove_nans(sys.argv[1], coors, hashmap, length)

                                                
