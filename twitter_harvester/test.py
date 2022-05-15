import pickle

import shapefile
dic_file = "area_coordinate.pkl"
a_file = open(dic_file, "rb")
area_coordinate_dic = pickle.load(a_file)
a_file.close()
area = 'MEL'
serach_coordinate = []
if area == 'Melbourne' or area == 'MEL':
    for key,coordinate_list in area_coordinate_dic.items():
        for coordinate in coordinate_list:
            serach_coordinate.append(coordinate)
print(len(serach_coordinate))