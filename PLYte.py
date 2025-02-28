from plyfile import PlyData

def find_property_index_contains(ply_data, req_property):
    index = 0
    index_list = []
    #Get a list of all properties.
    for i in ply_data.header.split("property"):
        if req_property in i:
            index_list.append(index)
        index += 1
    return index_list

def find_property_index(ply_data, req_property):
    #Find out the indexes of each of the .ply's properties.
    index = 0
    for i in ply_data.header.split("property"):
        if req_property in i:
            return index
        index += 1
    print("Property no in this .ply.")
    return None

def set_property_instances(ply_data, index, value):
    if 'vertex' in ply_data:
        #Set the property to the given value.
        vertex_element = ply_data['vertex']
        for vertex in vertex_element.data:
            vertex[index] = value
    else:
        print("No vertex element found in this PLY file.")

def set_multiproperty_instances(ply_data, index_list, value):
    count = 0
    #Keep updating and cycling through each property.
    for i in index_list:
        count += 1
        print(str(count) +" of " + str(len(index_list)))
        set_property_instances(ply_data, i, value)

def print_header(ply_data):
    print(ply_data.header)

def find_bounds(ply_data):
    #Sort through every vertex and find the bounds.
    if 'vertex' in ply_data:
        #Initialize our vertex data.
        vertex_element = ply_data['vertex']
        min_verts = [vertex_element.data[0][0],vertex_element.data[0][1],vertex_element.data[0][2]]
        max_verts = [vertex_element.data[0][0],vertex_element.data[0][1],vertex_element.data[0][2]]
        for vertex in vertex_element.data:
            #Check each value of the Vector3.
            for i in range(0,3):
                if vertex[i] < min_verts[i]:
                    min_verts[i] = vertex[i]
                if vertex[i] > max_verts[i]:
                    max_verts[i] = vertex[i]
    print("Max: " + str(max_verts))
    print("Min: " + str(min_verts))

ply_data = PlyData.read(input("Type the name of your file (needs to be in the same directory, ie 'house.ply'):\n"))
print("File Data:")
#Print out the header data and bounds of the file.
print_header(ply_data)
find_bounds(ply_data)

index_list = find_property_index_contains(ply_data, input("What properties would you like to edit? (for instance f_dc_2 for just red, f_dc for all base color values).\n"))
amount = float(input("Type the effect you want to set (for instance, 0.1, 1.1, 2, etc.)):\n"))
set_multiproperty_instances(ply_data,index_list,amount)

#Get file name.
name = input("What name should your .ply have? (for instance house for 'house.ply')\n")

#Write to file.
with open(name+'.ply', 'wb') as f:
    ply_data.write(f)

print("New file created at '"+name+".ply'")

#Notes:
#f_dc_2 is red!
#f_dc_1 is blue!
#f_dc_0 is green!
