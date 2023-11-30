import os




def rename_file(dir:str):
    file_list = os.listdir(dir)

    for i in range(len(file_list)):
        name_space = f'{dir.split("/")[1]}_{i+1}'
        print(name_space)
        name = ''

        for j in name_space:
            if j != ' ':
                name = name + j

        os.rename(f'{dir}/{file_list[i]}', f'{dir}/{name}.jpg') if file_list[i].split('.')[1] == 'jpg' else \
            os.rename(f'{dir}/{file_list[i]}', f'{dir}/{name}.mp4')

rename_file('raboti/Чистка лица')