from os import listdir
from os.path import join
from tqdm import tqdm
from PIL import Image


class Convert_Stage_1:
    '''
        Convert from 5 class (0 -> 1) to 5 class (0 -> w, h)
    '''
    def __init__(self, label_dir: str, image_dir: str, save_dir: str):
        self.label_dir       = label_dir
        self.image_dir       = image_dir
        self.save_dir        = save_dir
        self.results         = []
        self.image_extension = 'jpg'


    def get_results(self):
        for labelfn in tqdm(listdir(self.label_dir)):
            self.results = []

            imgfn = labelfn[:-3] + self.image_extension

            label_link = join(self.label_dir, labelfn)
            img_link = join(self.image_dir, imgfn)
            save_link = join(self.save_dir, labelfn)

            w, h = self.get_size(img_link)

            self.process_informations(label_link = label_link,
                                      w          = w,
                                      h          = h)
            self.save_label(save_link = save_link)
    

    def process_informations(self, label_link: str, w: int, h: int):
        with open(label_link, mode = 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_infos = line[:-1].split()
                line_infos_converted = self.list_mul(line_infos, w, h)
                self.results.append(' '.join(line_infos_converted))


    def save_label(self, save_link: str):
        with open(save_link, mode = 'w') as f:
            for line in self.results:
                f.writelines(line + '\n')


    @staticmethod
    def get_size(image_link: str):
        with Image.open(image_link) as img:
            w, h = img.size
        return w, h


    @staticmethod
    def list_mul(init_list: list, w: int, h: int):
        '''
            init_list: ['0', 'x', 'y', 'w', 'h'] (normalized) (float)
            -> return ['0', 'x_', 'y_', 'w_', 'h_'] (based) (int)
        '''
        results = []
        results.append(init_list[0])
        results.append(str((float(init_list[1]) * w)))
        results.append(str((float(init_list[2]) * h)))
        results.append(str((float(init_list[3]) * w)))
        results.append(str((float(init_list[4]) * h)))
        
        return results


class Convert_Stage_2:
    '''
        Convert from 5 class to 1 line
        ---
        0 x1c y1c w1 h1
        1 x2c y2c w2 h2
        2
        3
        4 xbbc ybbc w h


        x1c y1c
        x2c y2c
        x3c y3c
        x4c y4c
        xbb ybb w h

        ---
    '''
    def __init__(self, label_dir: str, save_dir: str):
        self.label_dir       = label_dir
        self.save_dir        = save_dir
        self.results         = []


    def get_results(self):
        for labelfn in tqdm(listdir(self.label_dir)):
            self.results = []

            label_link = join(self.label_dir, labelfn)
            save_link = join(self.save_dir, labelfn)


            self.process_informations(label_link = label_link)
            self.save_label(save_link)


    def process_informations(self, label_link):
        with open(label_link, mode = 'r') as f:
            lines = f.readlines()
            for line in lines[:-1]:
                infos = line[:-1].split()
                center = infos[1:3]
                self.results.append(' '.join(center))
            
            save_list = self.calculate_bbox(lines[-1][:-1].split())

            self.results.append(' '.join(save_list))


    def save_label(self, save_link: str):
        with open(save_link, mode = 'w') as f:
            for line in self.results:
                f.writelines(line + '\n')



    @staticmethod
    def calculate_bbox(init_list: list):
        '''
            ['0', 'x1c', 'y1c', 'w1', 'h1'] -> ['x1', 'y1', 'w1', 'h1']
        '''
        x_ = str(int(float(init_list[1]) - float(init_list[3]) / 2.0))
        y_ = str(int(float(init_list[2]) - float(init_list[4]) / 2.0))

        return [x_, y_, str(int(float(init_list[3]))), str(int(float(init_list[4])))]


class Convert_Stage_3:
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
    def __init__(self, label_dir: str, save_dir: str):
        self.label_dir       = label_dir
        self.save_dir        = save_dir
        self.image_extension = 'jpg'
        self.filenames       = {'label_links': [],
                                'save_links' : []}
        self.save_string     = ''

    def get_results(self):
        self.get_filenames()
        for idx, label_link in tqdm(enumerate(self.filenames['label_links'])):
            self.process_informations(label_link)
            self.save_label(self.filenames['save_links'][idx])
        
    
    def get_filenames(self):
        for labelfn in listdir(self.label_dir):
            self.filenames['label_links'].append(join(self.label_dir, labelfn))
            self.filenames['save_links'].append(join(self.save_dir, labelfn))

    
    def process_informations(self, label_link):
        with open(label_link, mode = 'r') as f:
            infos = f.readlines()
            self.save_string = self.save_string + infos[-1][:-1]
            for info in infos[:-1]:
                self.save_string = self.save_string + ' ' + info[:-1] + ' 0.0'
            self.save_string = self.save_string + ' 1.0'


    def save_label(self, save_link: str):
        with open(save_link, mode = 'w') as f:
            f.writelines(self.save_string)
        self.save_string = ''


class Convert_Stage_4:
    '''
        concat
        # name
        xbb ybb w h x1c y1c 0.0 x2c y2c 0.0 x3c y3c 0.0 x4c y4c 0.0 1.0
        ---
    '''
    def __init__(self, label_dir: str, save_dir: str):
        self.label_dir       = label_dir
        self.save_dir        = save_dir
        self.infos           = []
        self.image_extension = 'jpg'
        

    def get_results(self):
        self.get_filenames()
        self.save_label()


    def get_filenames(self):
        for labelfn in tqdm(listdir(self.label_dir)):
            with open(join(self.label_dir, labelfn), mode = 'r') as f:
                self.infos.append('# ' + labelfn[:-3] + self.image_extension + '\n' + f.read()  + '\n')
        

    def save_label(self):
        with open(join(self.save_dir, 'label.txt'), mode = 'w+') as f:
            f.writelines(self.infos)
