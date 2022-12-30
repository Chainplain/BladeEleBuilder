# Chainplain Refactured at 2022-12-30 00:00:25
import re
import matplotlib.pyplot as plt
import scipy
import numpy as np
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def read_indexed_face(proto_file_name, \
                      wing_interest_phrase = 'geometry DEF LU_wing IndexedFaceSet {',  \
                      bladeNo = 40,\
                      remove_area_x_list = [[-0.02, 0.02]],\
                      remove_area_y_list = [[-0.02, 0.02]]):
    file_obj    = open(proto_file_name, 'r')
    file_lines  = file_obj.readlines()
    line_count  = 0
    for line in file_lines:
        if wing_interest_phrase in line:
            print('Finded at line ', line_count + 1)
            break
        line_count += 1

    wing_XYZ  = file_lines [ line_count + 3]
    wing_XYZ_without_space = wing_XYZ.strip()
    wing_XYZ_list = re.split(r'[,]', wing_XYZ_without_space)


    print('wing_XYZ_list', wing_XYZ_list)

    X_data = []
    Y_data = []
    Z_data = []

    for wing_XYZ_data in wing_XYZ_list:
        wing_XYZ_data_list = re.split(r'[ ]', wing_XYZ_data.strip())
        if len(wing_XYZ_data_list) == 3:
            X_data.append(float(wing_XYZ_data_list[0]))
            Y_data.append(float(wing_XYZ_data_list[1]))
            Z_data.append(float(wing_XYZ_data_list[2]))

    print('X_data: ', X_data)
    print('Y_data: ', Y_data)
    print('Z_data: ', Z_data)


    # plt.title("Raw data show", fontsize=12)
  


    plt.scatter(X_data, Y_data)
    plt.title('Raw data')
    plt.show()




    X_data_choose = []
    Y_data_choose = []
    if ( len(X_data) == len(Y_data)):
        for i in range(len(X_data)):
            choose_flag = True
            for j in range(len(remove_area_x_list)):
                if  (X_data[i] > remove_area_x_list[j][0]) and\
                    (X_data[i] < remove_area_x_list[j][1]) and\
                    (Y_data[i] > remove_area_y_list[j][0]) and \
                    (Y_data[i] < remove_area_y_list[j][1]):
                    choose_flag = False
                    break
            if  choose_flag:
                X_data_choose.append(X_data[i])
                Y_data_choose.append(Y_data[i])

    plt.scatter(X_data_choose, Y_data_choose)
    plt.title('Choosen data')
    plt.show()
    output_file_name = proto_file_name[0:-6]

    X_data_choose_min = min(X_data_choose)
    X_data_choose_max = max(X_data_choose)

    f = scipy.interpolate.interp1d(X_data_choose, Y_data_choose, kind='linear')

    X_data_interp = np.linspace(X_data_choose_min, X_data_choose_max, bladeNo)
    Y_data_interp = f(X_data_interp)
    plt.plot(X_data_interp, Y_data_interp, 'go')
    plt.title('Interped data')
    plt.show()

    np.save(output_file_name + '_' + str(bladeNo)+'_BLE_X_pos.npy', X_data_interp)
    np.save(output_file_name + '_' + str(bladeNo) + '_BLE_Y_pos.npy', Y_data_interp)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_indexed_face('SimpleFlapper0.proto')
    print('Test done')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
