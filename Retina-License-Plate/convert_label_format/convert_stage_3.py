'''
        Convert from 5 class to 1 line
        ---
        x1c y1c
        x2c y2c
        x3c y3c
        x4c y4c
        xbb ybb w h

        # name
        xbb ybb w h x1c y1c 0.0 x2c y2c 0.0 x3c y3c 0.0 x4c y4c 0.0 1.0
        ---
    '''
from convert_init import Convert_Stage_3

labeldir_stage_2 = './label_stage_2'
labeldir_stage_3 = './label_stage_3'

stage_3 = Convert_Stage_3(label_dir = labeldir_stage_2,
                          save_dir  = labeldir_stage_3)

stage_3.get_results()