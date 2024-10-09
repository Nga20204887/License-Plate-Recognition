# Convert from 5 class (0 -> 1) to 5 class (0 -> w, h)

from convert_init import Convert_Stage_1

labeldir_raw = './label_raw'
imgdir = './images'
labeldir_stage_1 = './label_stage_1'

stage_1 = Convert_Stage_1(label_dir = labeldir_raw, 
                          image_dir = imgdir,
                          save_dir  = labeldir_stage_1)

stage_1.get_results()