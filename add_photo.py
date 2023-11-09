import os
from db_config import convert_to_binary_data, add_photo



new_name = 1
directory = 'foto_proceduri'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):

        name_photo = f.split("\\")[1]
        id_foto = int(name_photo.split('.')[0])
        blob_foto = convert_to_binary_data(f)
        new_foto = (blob_foto, id_foto)
        add_photo(new_foto)
