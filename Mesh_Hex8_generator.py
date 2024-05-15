import h5py
import numpy as np

def divide_list_into_sublists(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def extract_coordinates(lst, number_of_coordinates=3):
    """Assuming number_of_coordinates defaults to 3 for 3D models."""
    for i in range(0, len(lst), number_of_coordinates):
        yield lst[i:i + number_of_coordinates]

def generate_elements(node_coordinates, element_node_connectivity):
    elements = []
    for element in element_node_connectivity:
        # Assuming element ordering is correct for HE8, if not, adjust as per your element definition
        element_dict = {
            'nodes': element,
            'coords': np.array([node_coordinates[node - 1] for node in element])
        }
        elements.append(element_dict)
    return elements

def read_mesh_data(file_name):
    with h5py.File(file_name, 'r') as file:
        # Read coordinate data for 3D
        coo_dataset = file['ENS_MAA/Mesh_5/-0000000000000000001-0000000000000000001/NOE/COO']
        coo_data = coo_dataset[:]
        num_nodes = len(coo_data) // 3
        subcoord = list(extract_coordinates(coo_data, num_nodes))
        # Assuming every 3 values represent X, Y, Z coordinates for a node
        node_coordinates = [group for group in zip(*subcoord)]
        # print('node_coordinates:', node_coordinates)

        
        # Accessing QU8 element connectivity
        he8_dataset = file['ENS_MAA/Mesh_5/-0000000000000000001-0000000000000000001/MAI/HE8/NOD']
        he8_data = he8_dataset[:]
        num_quadrilaterals = len(he8_data) // 8
        sublists = list(divide_list_into_sublists(he8_data, num_quadrilaterals))
        element_node_connectivity = [group for group in zip(*sublists)]
        # print('element_node_connectivity:', element_node_connectivity)
    return node_coordinates, element_node_connectivity

if __name__ == "__main__":
    node_coordinates, element_node_connectivity = read_mesh_data('Mesh_5.med')
    elements = generate_elements(node_coordinates, element_node_connectivity)
