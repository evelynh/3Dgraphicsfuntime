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
	num_triangles = len(triangles)
	triangle_labels = {}
	for i in range(0, num_triangles):
		external_edges = countexternal(triangles[i], neighbors)
		triangle_labels[str(list(triangles[i]))] = external_edges

	print("-----labels-----")
	return triangle_labels;

def midpoint(i1, i2, vertices):
	'''
		Find the midpoint between two points
		i1 = Label for point 1
		i2 = Label for point 2
		vertices = array that gives correspondence between label and actual point
	'''
	A = vertices[i1]
	B = vertices[i2]
	return [(A[0]+B[0])/2, (A[1]+B[1])/2]
def chordalaxis(triangles, neighbors, vertices):
	'''
		Find the chordal axis
	'''
	ca = []	
	for tri in triangles:
		for i in range(0, len(tri)-1):
			if isExternal(tri[i], tri[i+1], neighbors) == False:
					toAdd = midpoint(tri[0], tri[1], vertices)
					if toAdd not in ca:
						print(tri[i], tri[i+1])
						ca += [toAdd]
		if isExternal(tri[0], tri[len(tri)-1], neighbors) == False:
				toAdd = midpoint(tri[0], tri[len(tri)-1], vertices)
				if toAdd not in ca:
					print(tri[0], tri[len(i)-1])
					ca += [toAdd]
	print("-----chordal axis-----")
	return ca
def nonedgepoint_index(indices):
	'''
		Find the 3rd point index given the two other points
	'''
	if indices == [0, 1]:
		return 2
	elif indices ==  [1, 2]:
		return 0
	elif indices == [2,0]:
		return 1
def checkmerge(triangle, int_edge, int_edge_indices, vertices):
	'''
		Check if should merge sleeve triangle per Teddy algorithm
	'''
	circle_center = midpoint(int_edge[0], int_edge[1], vertices)
	radius = distance(vertices[int_edge[0]], circle_center)
	to_test = []
	to_test_points = []
	for i in triangle:
		if i not in int_edge:
			to_test += [list(vertices[i])
	for i in range(0, len(to_test)):
		x = to_test[i][0]
		y = to_test[i][1]
		if ((x - circle_center[0])**2 + (y - circle_center[1])**2) > radius**2:
			return False
	return True

def findother(triangle, int_edge, triangles):
	'''
		Find the other triangle that shares the same internal edge
	'''
	other = []
	for i in range(0, len(triangles)):
		# print(triangles[i])
		if triangles[i] != triangle:
			if (int_edge[0] in triangles[i]) and (int_edge[1] in triangles[i]):
				other = triangles[i]
	return other

def merge(triangle, other):
	'''
		Merge two triangles
	'''
	combined = np.concatenate((triangle, other), axis=None)	
	new_triangle = [] 
	for num in combined: 
		if num not in new_triangle: 
			new_triangle.append(num)
	new_triangle.sort()  
	return new_triangle

def findinteraledge(triangle, neighbors):
	'''
		Find internal edge of triangle
	'''
	# print("fei")
	int_edge = []
	int_edge_indices = []
	for i in range(0, len(triangle)-1):
		if isExternal(triangle[i], triangle[i+1], neighbors) == False:
			# print([triangle[i], triangle[i+1]], [i, i+1])
			return [triangle[i], triangle[i+1]], [i, i+1]
	if isExternal(triangle[len(triangle)-1], triangle[0], neighbors) == False:
		# print([triangle[len(triangle)-1], triangle[0]], [len(triangle)-1, 0])
		return [triangle[len(triangle)-1], triangle[0]], [len(triangle)-1, 0]
	return None 

def junctionmidpoint(triangle, vertices):
	'''
		Find midpoint of a triangle to merge with a junction triangle
	'''
	x_sum = 0
	y_sum = 0 
	num_sides = length(triangle)
	for i in range(0, len(vertices)):
		x_sum += vertices[triangle[i]][0]
		y_sum += vertices[triangle[i]][1]
	return [x_sum/num_sides, y_sum/num_sides]

def fantriangles(triangle, fanpoint, axis, index, int_edge, triangles, vertices):
	'''
		Fan triangles
		fanpoint: point from which triangles are fanned
		index: index of fanpoint in vertices
	'''
	temp = []
	# check to make sure aren't creating triangle with internal edge
	# check then add wrap around case i.e. [5, 0, index]
	for i in range(0, len(triangles)):
		if triangles[i] != triangle:
			temp.append(triangles[i])
	new_triangles = temp
	for i in range(0, len(triangle)-1):
		if [triangle[i],triangle[i+1]] != int_edge and [triangle[i],triangle[i+1]] != int_edge.reverse():
			fanned_triangle = [triangle[i], triangle[i+1], index]
			if tuple(fanpoint) in axis:
				axis[tuple(fanpoint)].append(triangle[i])
				axis[tuple(fanpoint)].append(triangle[i+1])
			else:
				axis[tuple(fanpoint)] = [triangle[i]]
				axis[tuple(fanpoint)].append(triangle[i+1])
			# print(fanned_triangle)
			new_triangles.append(fanned_triangle)
	if [triangle[0],triangle[len(triangle)-1]] != int_edge and [triangle[i],triangle[i+1]] != int_edge.reverse():
			fanned_triangle = [triangle[0],triangle[len(triangle)-1], index]
			new_triangles.append(fanned_triangle)
			if tuple(fanpoint) in axis:
				axis[tuple(fanpoint)].append(triangle[0])
				axis[tuple(fanpoint)].append(triangle[len(triangle)-1])
			else:
				axis[tuple(fanpoint)] = [triangle[0]]
				axis[tuple(fanpoint)].append(triangle[len(triangle)-1])
	for pair in axis:
		dup_array = axis[pair]
		remove_dup = set(dup_array)
		axis[pair] = list(remove_dup)
	return new_triangles, axis 

def intersection(lst1, lst2):
	'''
		Find intersection of two lists
	'''
	# print("------------------")
	# print("intersection")
	toret = []
	# print(lst1, lst2)
	if len(lst1) > len(lst2):
		for i in range(0, len(lst1)):
			if lst1[i] in lst2:
				print(i, lst1[i])
				toret.append(lst1[i])
	else:
		for i in range(0, len(lst2)):
			if lst2[i] in lst1:
				print(i, lst2[i])
				toret.append(lst2[i])
	# print("toret")
	# print(toret)
	# print("---------------------")
	return toret
def recalc_chordalaxis(old_points, new_points, old_faces, new_faces, neighbors):
	'''
		Recalculate chordal axis after fanning
	'''
	remain_points = intersection(old_points, new_points)
	remain_faces = intersection(old_faces, new_faces)
	chordal_axis = chordalaxis(remain_faces, neighbors, remain_points)
	return chordal_axis

def fanning(triangles, neighbors, vertices, labels):
	'''
		Fan triangles so chordal axis can be pruned
	'''
	print("FANNING")
	new_vertices = []
	for i in range(0, len(vertices)):
		new_vertices.append(list(vertices[i]))
	orig_triangles = []
	new_triangles = []
	axis = {}
	
	# Convert triangles array into Python list for ease of use
	# orig_triangles: copy of inputted array of triangles
	# new_triangles: final output (initially, a copy of orig_triangles)
	for i in range(0, len(triangles)):
		orig_triangles.append(list(triangles[i]))
		new_triangles.append(list(triangles[i]))

	for i in range(0, len(triangles)):
		# We examine each terminal triangle
		if labels[str(list(triangles[i]))] == 2:
			print(triangles[i])
			# Find the internal edge	
			int_edge, int_edge_indices = findinteraledge(orig_triangles[i], neighbors)
			curr_triangle = orig_triangles[i]
			curr_triangle_index = i
			if curr_triangle not in new_triangles:
				continue
			toMerge = True
			num_iterations = 0
			terminate = False
			while toMerge == True:
				num_iterations += 1
# 				print("current triangle")
# 				print(curr_triangle)
				int_edge, int_edge_indices = findinteraledge(curr_triangle, neighbors)

# 				print("internal edge")
# 				print(int_edge)
				    
				other_triangle = findother(curr_triangle, int_edge, new_triangles)

				if other_triangle == []:
					fanpoint = midpoint(int_edge[0], int_edge[1], vertices)
					if tuple(fanpoint) in axis:
						print(tuple(fanpoint))
						axis[tuple(fanpoint)].append(int_edge[0])
						axis[tuple(fanpoint)].append(int_edge[1])
						new_index = new_vertices.index(fanpoint)

					else:
						axis[tuple(fanpoint)] = [int_edge[0]]
						axis[tuple(fanpoint)].append(int_edge[1])
						# Find index of fanpoint in new_vertices
						new_vertices = new_vertices +[fanpoint] 
						new_index = len(new_vertices)-1
					new_triangles, axis = fantriangles(curr_triangle,fanpoint, axis, new_index, int_edge,new_triangles, new_vertices)
					# print(new_triangles)
					break

				print("other triangle")
				print(other_triangle)
				external_count = countexternal(other_triangle, neighbors)
				print("external_count")
				print(external_count)
				#  If the triangle to be merged with is a junction triangle
				if external_count == 0:
					fanpoint = midpoint(int_edge[0], int_edge[1], vertices)
					if tuple(fanpoint) in axis:
						print(tuple(fanpoint))
						axis[tuple(fanpoint)].append(int_edge[0])
						axis[tuple(fanpoint)].append(int_edge[1])
						new_index = new_vertices.index(fanpoint)

					else:
						print(tuple(fanpoint))
						axis[tuple(fanpoint)] = [int_edge[0]]
						axis[tuple(fanpoint)].append(int_edge[1])
						# Find index of fanpoint in new_vertices
						new_vertices = new_vertices +[fanpoint] 
						new_index = len(new_vertices)-1
					new_triangles, axis = fantriangles(curr_triangle,fanpoint, axis, new_index, int_edge,new_triangles, new_vertices)
					break
					# Replace junction triangle 
					#new_triangles.remove(other_triangle)
					#new_triangles.append(other_triangle+[new_index])
				# 	break
				# If the triangle to be merged with is a sleeve triangle
				elif external_count == 1:
					int_edge, int_edge_indices = findinteraledge(curr_triangle, neighbors)
				    	# check if you should merge triangles
					if checkmerge(curr_triangle, int_edge, int_edge_indices, vertices):
						print("merge triangles 1")
						merged_triangle = merge(curr_triangle, other_triangle)
						# int_edge, int_edge_indices = findinteraledge(curr_triangle, neighbors)
						# Remove unmerged triangles 
						# if other_triangle in new_triangles:
						new_triangles.remove(other_triangle)
						new_triangles.remove(curr_triangle)
						curr_triangle = merged_triangle						
						# Add current triangle
						new_triangles.append(curr_triangle)
					# Otherwise, stop and fan
					else:
						print("fan triangles 1")
						fanpoint = midpoint(int_edge[0], int_edge[1], vertices)
						if tuple(fanpoint) in axis:
							print(tuple(fanpoint))
							axis[tuple(fanpoint)].append(int_edge[0])
							axis[tuple(fanpoint)].append(int_edge[1])
						else:
							print(tuple(fanpoint))
							axis[tuple(fanpoint)] = [int_edge[0]]
							axis[tuple(fanpoint)].append(int_edge[1])
						new_vertices = new_vertices +[fanpoint] 
						new_index = len(new_vertices)-1
						# Fan 
						new_triangles, axis = fantriangles(curr_triangle,fanpoint, axis, new_index, int_edge,new_triangles, new_vertices)
						print(new_triangles)
						break

				else:
					if num_iterations > 1:
						int_edge, int_edge_indices = findinteraledge(curr_triangle, neighbors)
						if checkmerge(curr_triangle, int_edge, int_edge_indices, vertices):
							merged_triangle = merge(curr_triangle, other_triangle)
							print(int_edge)
							# int_edge, int_edge_indices = findinteraledge(curr_triangle, neighbors)
							# Remove unmerged triangles 
							new_triangles.remove(other_triangle)
							new_triangles.remove(curr_triangle)
							curr_triangle = merged_triangle						
							# Add current triangle
							new_triangles.append(curr_triangle)
						# Otherwise, stop and fan
						else:
							print("FAN")
							# fanpoint = midpoint(int_edge[0], int_edge[1], vertices)
							# new_vertices = new_vertices +[fanpoint]
							# new_index = len(new_vertices)-1
							# # Fan
							# new_triangles, axis = fantriangles(curr_triangle,fanpoint, axis, new_index, int_edge,new_triangles, new_vertices)
							fanpoint = midpoint(int_edge[0], int_edge[1], vertices)
							if tuple(fanpoint) in axis:
								print(tuple(fanpoint))
								axis[tuple(fanpoint)].append(int_edge[0])
								axis[tuple(fanpoint)].append(int_edge[1])
								new_index = new_vertices.index(fanpoint)

							else:
								print(tuple(fanpoint))
								axis[tuple(fanpoint)] = [int_edge[0]]
								axis[tuple(fanpoint)].append(int_edge[1])
								# Find index of fanpoint in new_vertices
								new_vertices = new_vertices +[fanpoint] 
								new_index = len(new_vertices)-1
							new_triangles, axis = fantriangles(curr_triangle,fanpoint, axis, new_index, int_edge,new_triangles, new_vertices)

							# new_triangles = fantriangles(curr_triangle,fanpoint, new_index, new_triangles, new_vertices)
							break
					else:
						fanpoint = midpoint(int_edge[0], int_edge[1], vertices)
						if tuple(fanpoint) in axis:
							print(tuple(fanpoint))
							axis[tuple(fanpoint)].append(int_edge[0])
							axis[tuple(fanpoint)].append(int_edge[1])
							new_index = new_vertices.index(fanpoint)

						else:
							print(tuple(fanpoint))
							axis[tuple(fanpoint)] = [int_edge[0]]
							axis[tuple(fanpoint)].append(int_edge[1])
							# Find index of fanpoint in new_vertices
							new_vertices = new_vertices +[fanpoint] 
							new_index = len(new_vertices)-1
						new_triangles, axis = fantriangles(curr_triangle,fanpoint, axis, new_index, int_edge,new_triangles, new_vertices)
					break
	# axis is a dictionary that maps a point on the chordal axis to its external edges
	# it gets built during fanning and is used for elevation
	return new_vertices, new_triangles, axis

def retriangulate(old_faces, new_faces, vertices, axis, neighbors, labels):
	'''
		Retriangulate remaining triangles
	'''
	print(old_faces)
	print(new_faces)
	retri_faces = intersection(old_faces, new_faces)
	print("RETRI")
	print(retri_faces)

	retri_mapping = {}
	updated_faces = new_faces
	updated_points = vertices
	for tri in retri_faces: 
		# if a sleeve triangle
		if labels[str(tri)] == 1:
			# find the external edge
			external_edge = []
			for i in range(0, len(tri)-1):
				if isExternal(tri[i], tri[i+1], neighbors) == True:
					external_edge = [tri[i], tri[i+1]]
			if isExternal(tri[0], tri[len(tri)-1], neighbors) == True:
				external_edge = [tri[0], tri[len(tri)-1]]
			other = copy.deepcopy(tri)
			other.remove(external_edge[0])
			other.remove(external_edge[1])

			m_a = midpoint(external_edge[0], other[0], vertices)
			m_b = midpoint(external_edge[1], other[0], vertices)
			# triangulate [m_a, m_b, external_edge[0], external_edge[1]] and [m_a, m_b, other]
			# trap_coords = np.array([m_a, m_b, vertices[external_edge[0]], vertices[external_edge[1]]])
			# vert_map = {}
			# vert_map[0] = len(vertices);
			a_i = -1
			for i in range(0, len(updated_points)):
				if updated_points[i] == m_a:
					a_i = i
			if a_i == -1:
				updated_points.append(m_a)
				a_i = len(updated_points)-1
			
			b_i = -1
			for i in range(0, len(updated_points)):
				if updated_points[i] == m_b:
					b_i = i
			if b_i == -1:
				updated_points.append(m_b)
				b_i = len(updated_points)-1
			
			# Create a mapping between the original triangle and the newly triangulated triangle so that 
			# we can later replace the original triangle
			retri_mapping[str(tri)] = []
			retri_mapping[str(tri)].append([a_i, b_i, external_edge[0]])
			retri_mapping[str(tri)].append([b_i, external_edge[0], external_edge[1]])
			retri_mapping[str(tri)].append([a_i, b_i, other[0]])
			if tuple(m_b) in axis:
				axis[tuple(m_b)].append(external_edge[0])
			else:
				axis[tuple(m_b)]=external_edge[0]
		if labels[str(tri)] == 1:
					# find the external edge
					external_edge = []
					for i in range(0, len(tri)-1):
						if isExternal(tri[i], tri[i+1], neighbors) == True:
							external_edge = [tri[i], tri[i+1]]
					if isExternal(tri[0], tri[len(tri)-1], neighbors) == True:
						external_edge = [tri[0], tri[len(tri)-1]]
					other = copy.deepcopy(tri)
					other.remove(external_edge[0])
					other.remove(external_edge[1])

					m_a = midpoint(external_edge[0], other[0], vertices)
					m_b = midpoint(external_edge[1], other[0], vertices)
					# triangulate [m_a, m_b, external_edge[0], external_edge[1]] and [m_a, m_b, other]
					# trap_coords = np.array([m_a, m_b, vertices[external_edge[0]], vertices[external_edge[1]]])
					# vert_map = {}
					# vert_map[0] = len(vertices);
					a_i = -1
					for i in range(0, len(updated_points)):
						if updated_points[i] == m_a:
							a_i = i
					if a_i == -1:
						updated_points.append(m_a)
						a_i = len(updated_points)-1
					
					b_i = -1
					for i in range(0, len(updated_points)):
						if updated_points[i] == m_b:
							b_i = i
					if b_i == -1:
						updated_points.append(m_b)
						b_i = len(updated_points)-1
					
					# Create a mapping between the original triangle and the newly triangulated triangle so that 
					# we can later replace the original triangle
					retri_mapping[str(tri)] = []
					retri_mapping[str(tri)].append([a_i, b_i, external_edge[0]])
					retri_mapping[str(tri)].append([b_i, external_edge[0], external_edge[1]])
					retri_mapping[str(tri)].append([a_i, b_i, other[0]])
					if tuple(m_b) in axis:
						axis[tuple(m_b)].append(external_edge[0])
					else:
						axis[tuple(m_b)]=external_edge[0]

		# if it's a junction triangle
		elif labels[str(tri)] == 0:
			# get the midpoints
			# fi
			ext_point = -1
			for i in range(0, len(triangle)):
				if triangle[i] in neighbors:
					ext_point = triangle[i]
					break
			if ext_point != -1:
				other_points = copy.deepcopy(tri)
				other_points.remove(ext_point)
				other_midpoint = (other_points[0], other_points[1], vertices)
				
				om_i = -1
				for i in range(0, len(updated_points)):
					if updated_points[i] == other_midpoint:
						om_i = i
				if om_i == -1:
					updated_points.append(om_i)
					om_i = len(updated_points)-1

				retri_mapping[str(tri)] = []
				retri_mapping[str(tri)].append([om_i, ext_point, other_points[0]])
				retri_mapping[str(tri)].append([om_i, ext_point, other_points[1]])
				# axis[tuple(other_midpoint)].append(ext_point)
				if tuple(other_midpoint) in axis:
					axis[tuple(other_midpoint)].append(ext_point)
				else:
					axis[tuple(other_midpoint)]=ext_point		

	# Update the new_triangles to include retriangulated triangles
	for tri in retri_mapping:
		toAdd = retri_mapping[str(tri)]
		list_tri = []
		for i in list(tri):
			if i in "0123456789":
				list_tri.append(int(i))
		updated_faces.remove(list_tri)
		for x in toAdd:
			updated_faces.append(x)
	return updated_faces, updated_points
		# if a junction triangle 
		#if labels[str(tri)] == 0:
		
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

def teddy(points):
	points = np.asarray(points)
	hex_tri = pymesh.triangle();
	hex_tri.points = points;
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

	ret = fanning(hex_tri.faces, neighbors, hex_tri.points, labeled_triangles)
	hex_new_points = ret[0]
	hex_new_faces = ret[1]
	hex_axis = ret[2]

	hex_old_points  = []
	hex_old_faces = []
	for i in range(0, len(hex_tri.points)):
		hex_old_points.append(list(hex_tri.points[i]))

	for i in range(0, len(hex_tri.faces)):
		hex_old_faces.append(list(hex_tri.faces[i]))
	print("old points {}".format(hex_old_points))
	updated_faces, updated_points = retriangulate(hex_old_faces, hex_new_faces, hex_new_points, hex_axis, neighbors, labeled_triangles)
	elevate(updated_points, updated_faces, hex_axis, neighbors);

def main():
	# print("------HEX------");
	# hex = [[0,0],
	# 	[.5, 3],
	# 	[2,5],
	# 	[5,6],
	# 	[6.5,3],
	# 	[7,0]]
	# teddy(hex);

	# print("------PENT------")
	# pent = [[0.0, 0.0], 
	# 	[1.0, 0.0], 
	# 	[1.0, 1.0], 
	# 	[0.5, 1.5], 
	# 	[0.0, 1.0]]
	# teddy(pent);

	sq = [[0, 0],
		[1, 0],
		[1, 1],
		[0, 1]]
	teddy(sq)
	

if __name__== "__main__":
  main()

                
