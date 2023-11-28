import os
import shutil
import time


def delete_foto(path:str):

        folder = '/'.join(path.split('/')[:len(path.split('/'))-1])
        file_name = path.split('/')[len(path.split('/'))-1].split('.')[0].split('_')[0]
        file_type = path.split('/')[len(path.split('/'))-1].split('.')[1]
        file_index = int(path.split('/')[len(path.split('/'))-1].split('.')[0].split('_')[1])
        print(f'{folder}/{file_name}_{file_index}.{file_type}')
        count = file_index

        os.remove(path)
        time.sleep(1)
        for file in os.listdir(folder)[file_index-1:]:
            shutil.move(f'{folder}/{file_name}_{count+1}.{file_type}', f'{folder}/{file_name}_{count}.{file_type}')
            count += 1








# delete_foto('sertificat_file_test/sert_2.jpg')