#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def find_intersection(hashmap1, hashmap2):
    '''Checks the condensed dictionaries hashmap1 and hashmap2 for spherical cones that both face each 
    other and intersect.
    
    A new hashmap, intersecting_spheres, is returned with keys from hashmap1 and values from hashmap2 
    '''
    intersecting_spheres = {}
    for sphere1, values1 in hashmap1.items(): # looping through every sphere(key)-value pair in hashmap1
        for sphere2, values2 in hashmap2.items():
            if face_each_other(values1, values2): # calling a function defined above
                intersection = intersect(values1, values2) # calling a function defined above. Making value1 the key and value2 the value
                if intersection:
                    # Append hashmap2 keys as values to hashmap1 keys in intersecting_spheres dictionary
                    if sphere1 in intersecting_spheres:
                        intersecting_spheres[sphere1].append(sphere2)
                    else:
                        intersecting_spheres[sphere1] = [sphere2]
                    # Append hashmap1 keys as values to hashmap2 keys in intersecting_spheres
                    # We want the hashmap to be directed from hashmap1 -> hashmap2 so we omit this part
#                     if sphere2 in intersecting_spheres:
#                         intersecting_spheres[sphere2].append(sphere1)
#                     else:
#                         intersecting_spheres[sphere2] = [sphere1]                        
                                             
    return intersecting_spheres

def face_each_other(sphere1, sphere2):
    """If the dot product of two vectors is positive, it means that 
    the angle between them is less than 90 degrees (i.e., they are acute). 
    In other words, the two vectors point in the same general direction, 
    and they face each other."""
    dot_product = dot(sphere1[1], sphere2[1]) # perpendicular vectors [x,y,z]
    
    magnitude_product = math.sqrt(sum((float(a) ** 2) for a in sphere1[1]))*math.sqrt(sum((float(b) ** 2) for b in sphere2[1]))
    if magnitude_product == 0:
        return 0
    
    cos_angle = dot_product / magnitude_product
    angle_radians = math.acos(cos_angle)
    angle_degrees = math.degrees(angle_radians)
    
    if angle_degrees <= angle_tolerance:
        return True
    return False

def intersect(sphere1, sphere2):
    """Check if two spheres intersect, and return the intersection points."""
    dist_between_apex_points = distance(sphere1[0], sphere2[0])
    radius1 = hbond_distance_cutoff      
    radius2 = hbond_distance_cutoff
    if dist_between_apex_points <= radius1 + radius2:
        # They intersect
        return True
    return False

def distance(p1, p2):
    """Calculate the distance between two points."""
    p1_float = [float(num) for num in p1]
    p2_float = [float(num) for num in p2]
    distance = np.sqrt(((p1_float[0] - p2_float[0])**2) + 
                       ((p1_float[1] - p2_float[1])**2) + 
                       ((p1_float[2] - p2_float[2])**2) )
    return distance

def dot(v1, v2):
    """Calculate the dot product of two vectors."""
    return float(v1[0]) * float(v2[0]) + float(v1[1]) * float(v2[1]) + float(v1[2]) * float(v2[2]) 
# where are v1 and v2 coming from?
#def length(v):
  #  """Calculate the length of a vector."""
  #  return math.sqrt(dot(v, v))

