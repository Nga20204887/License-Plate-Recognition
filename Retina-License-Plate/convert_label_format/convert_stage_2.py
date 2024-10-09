'''
        Convert from 5 class to 1 line
        ---
        0 x1 y1 w1 h1
        1 x2 y2 w2 h2
        2
        3
        4 xbb ybb w h


        # name
        xbb ybb w h x1c y1c 0.0 x2c y2c 0.0 x3c y3c 0.0 x4c y4c 0.0 1.0
        ---
    '''
from convert_init import Convert_Stage_2

labeldir_stage_1 = './label_stage_1'
labeldir_stage_2 = './label_stage_2'

stage_2 = Convert_Stage_2(label_dir = labeldir_stage_1,
                          save_dir  = labeldir_stage_2)

stage_2.get_results()