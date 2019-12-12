import pymesh
import numpy as np
import os
import math
import copy

def distance(A, B):
	'''
		Find the distance between two points
		A = coordinates of point 1
		B = coordinates of point 2
        return distance between two points
	'''
	return math.sqrt((A[0]-B[0])**2 + (A[1]-B[1])**2 )

def construct_neighbors(vertices):
    '''
        Construct a dictionary of adjacent vertices (all the external points and edges)
        Vertices = array of 2D points
        neighbors = {vertex_index: [adjacent vertices]}
        return dictionary of external vertices and external edges
    '''
    neighbors = {};
    num_vertices = len(vertices);
    for i in range(0, num_vertices):
        if i == 0:
            neighbors[i] = (num_vertices - 1, i + 1);
        elif i == num_vertices - 1: 
            neighbors[i] = (i - 1, 0);
        else:
            neighbors[i] = (i - 1, i + 1);

    print("-----neighbors-----");
    return neighbors

def isExternal(p1, p2, neighbors):
    '''
        Check if the edge created by two points is an external edge
        p1 = index of vertex 1
        p2 = index of vertex 2
        neighbors = dictinary of external vertices and edges
        return True of edge is external and False if not external
    '''
    if p1 in neighbors:
        num_neighbors = len(neighbors[p1]);
        for i in range(0, num_neighbors):
            if neighbors[p1][i] == p2:
                return True;
    return False;

def countexternal(triangle, neighbors):
	external_edges = 0
	for j in range(0, len(triangle)-1):
		if isExternal(triangle[j], triangle[j+1], neighbors):
			external_edges = external_edges + 1
	if isExternal(triangle[len(triangle)-1], triangle[0], neighbors):
		external_edges = external_edges + 1
	return external_edges

def label(triangles, neighbors):
    '''
        Label each triangle as terminal, sleeve, or junction
        triangles = array of arrays containing vertices of triangles
        neighbors = dictinary of external vertices and edges
        return dictionary mapping triangle to the number of external edges it has

        terminal: 2 external edges        2
        sleeve:   1 external edges        1
        junction: 0 external edges        0
    '''
	num_triangles = len(triangles);
	triangle_labels = {}
	for i in range(0, num_triangles):
		external_edges = countexternal(triangles[i], neighbors)
		triangle_labels[str(list(triangles[i]))] = external_edges
	
    print("-----labels-----")
	return triangle_labels;

def distinct_pairs(arr):
    arr_len = len(arr);
    ret_arr = [];
    for i in range(0, arr_len):
        for j in range (i + 1, arr_len):
            pair = (arr[i], arr[j]);
            ret_arr.append(pair);
    return ret_arr;

def elevate(vertices, faces, axis, neighbors):
    '''
        Elevate the vertices to create a volumetric object
        vertices = all the points of the polygon (includes both internal and external)
        faces = array of arrays containing vertices of triangles
        axis = dictionary mapping 2D coordinate points of the spine to the indices of the external vertices they are connected to
        neighbors = dictinary of external vertices and edges
    '''
    num_vertices = len(vertices);
    
    # add z value to all vertices. Set all to 0
    for v in range(0, num_vertices):
        vertices[v].append(0.0);
    
    # copy faces for the opposite side
    faces_copy = copy.deepcopy(faces)
    # iterate through points in spine
    for i in axis:
        print("spine point: {}".format(i))
        old = vertices.index([i[0], i[1], 0])
        num_external_neighbors = len(axis[i]);
        dist = 0;
        # iterate through each external point it is connected to
        for j in range(0, num_external_neighbors):
            # distance between spine point and external edge
            print("vertices[axis[{}][{}]] = {}".format(i, j, axis[i][j]));
            external = vertices[axis[i][j]];
            dist += distance(i, external);
        # this is the z coordinate of the current spine point
        avg = dist/num_external_neighbors;

        # update the z value in vertices list
        for v in vertices:
            if ((v[0] == i[0]) and (v[1] == i[1])):
                print("adding")
                v[2] = avg
        
        # add the vertex on the other side
        other_vertex = (i[0], i[1], avg * -1)
        vertices.append(other_vertex)
        # this is the index of the new vertex on the other side
        new = len(vertices) - 1
        # iterate through faces_copy and everywhere there was the old vertex, add this one
        print("old: {} and new: {}".format(old, new))
        for f in faces_copy:
            for i in range (0, 3):
                if f[i] == old:
                    f[i] = new

    print("faces before {}".format(faces))
    # add faces on other side to the faces list
    for face in faces_copy:
        faces.append(face)
    print("faces after {}".format(faces))

    # convert to ndarry for pymesh
    vertices = np.asarray(vertices);
    faces = np.asarray(faces);
    final_mesh = pymesh.form_mesh(vertices, faces);
    pymesh.save_mesh("result.obj", final_mesh, ascii=True);
    return 0;
    
def main():
    print("------HEX------");
    hex = np.array([
 		[0,0],
 		[.5, 3],
 		[2,5],
 		[5,6],
 		[6.5,3],
 		[7,0]
 	]);
    hex_tri = pymesh.triangle();
    hex_tri.points = hex;
    hex_tri.split_boundary = False;
    hex_tri.verbosity = 0;
    hex_tri.keep_convex_hull = True;
    hex_tri.run();
    print("-----points-----");
    print(hex_tri.points);
    print("-----vertices-----");
    print(hex_tri.vertices);
    print("-----faces-----");
    print(hex_tri.faces);

    hex_mesh_tri = hex_tri.mesh;
    neighbors = construct_neighbors(hex_tri.points);
    print(neighbors);
    labeled_triangles = label(hex_tri.faces, neighbors);
    print(labeled_triangles);
    vertices = [[0.0, 0.0], 
                [0.5, 3.0], 
                [2.0, 5.0], 
                [5.0, 6.0], 
                [6.5, 3.0], 
                [7.0, 0.0], 
                [3.75, 1.5], 
                [3.5, 3.0]];
    faces = [[7, 6, 4],
            [6, 4, 5],
            [7, 6, 1],
            [1, 0, 6], 
            [5, 0, 6], 
            [1, 2, 7], 
            [2, 3, 7], 
            [3, 4, 7]];
    axis = {(3.5, 3.0) : [1, 2, 3, 4],
            (3.75, 1.5) : [0, 5, 1]};

    elevate(vertices, faces, axis, neighbors);

    print("------PENT------")
    axis = {(0.5, 1.0): [0, 1, 2, 4]}
    faces = [[4, 5, 3], [3, 5, 2], [0, 1, 5], [1, 2, 5], [0, 4, 5]]
    points = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.5, 1.5], [0.0, 1.0], [0.5, 1.0]]
    neighbors = {0: (4, 1), 1: (0, 2), 2: (1, 3), 3: (2, 4), 4: (3, 0)}

    elevate(points, faces, axis, neighbors)

if __name__== "__main__":
  main()

                
