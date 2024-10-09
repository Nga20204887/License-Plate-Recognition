'''
        concat
        # name
        xbb ybb w h x1c y1c 0.0 x2c y2c 0.0 x3c y3c 0.0 x4c y4c 0.0 1.0
        ---
    '''
from convert_init import Convert_Stage_4

labeldir_stage_3 = './label_stage_3'
labeldir_stage_4 = './label_stage_4'

stage_4 = Convert_Stage_4(label_dir = labeldir_stage_3,
                          save_dir  = labeldir_stage_4)

stage_4.get_results()