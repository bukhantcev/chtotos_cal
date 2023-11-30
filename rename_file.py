import os




def rename_file(dir:str):
    file_list = os.listdir(dir)

    for i in range(len(file_list)):
        os.rename(f'{dir}/{file_list[i]}', f'{dir}/{dir}_{i}.jpg') if file_list[i].split('.')[1] == 'jpg' else \
            os.rename(f'{dir}/{file_list[i]}', f'{dir}/{dir}_{i}.mp4')

rename_file('raboti/Фракционная мезотерапия')