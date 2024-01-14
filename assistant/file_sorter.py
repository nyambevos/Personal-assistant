""" Модуль сортування файлів """
# для роботи модуля додати до парсерара рядки:
#    folder = Path(val) val - шлях до файлу у форматі рядок
#    init_folder(folder) init_folder - метод модуля file_sorter

from pathlib import Path
import re
import shutil
import os

folders = ['images', 'documents', 'audio', 'video', 'archives', 'other'] # папки для файлів
list_of_bad_folders = list()
folders_absolute = []


def init_folder(val):
    global folder 
    folder = val
    main()


def main():
    global folder, folders_absolute
    try:        
        if not folder.exists():                               # Перевірка чи існує папка           
            raise FileNotFoundError        
    except FileNotFoundError:
        print('\nПомилка: папка не знайдена\n')
        exit(1)
    else:
        print(f"\nCортуємо файли у папці {folder}\n")
    
    folder_absolute = folder.absolute()         # створення абсолютного шляху для папки
    
    for i in folders:                       # Створення абсолютних шляхів для папок категорій
        folders_absolute.append(folder_absolute.joinpath(i))
        
    for i in folders_absolute:                       # Перевірка на наявність папок категорій та створення якщо відсутні
        if not os.path.exists(i):
            os.mkdir(i)
            print(f'Створено папку {i.name}')
                
    find_files(folder)                      # пошук файлів у заданій папці
        
    list_of_bad_folders.reverse()                   
    for i in list_of_bad_folders:                                       # Видалення пустих папок
        try:
            print(f'Видаляємо пусту папку {i.name}')
            os.rmdir(i)
        except:
            find_files(i)


def find_files(path):

    for files in path.iterdir():
        
        if files.is_file():            
            if files.suffix.upper() in ('.JPEG', '.PNG', '.JPG', '.SVG'):
                norm_name = normalize(files.name)       # перейменування файлу
                shutil.move(files.absolute(), Path(folders_absolute[0]).joinpath(norm_name)) # переміщення файлу           
            elif files.suffix.upper() in  ('.AVI', '.MP4', '.MOV', '.MKV'):
                norm_name = normalize(files.name)      
                shutil.move(files.absolute(), Path(folders_absolute[3]).joinpath(norm_name))
            elif files.suffix.upper() in ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'):
                norm_name = normalize(files.name)
                shutil.move(files.absolute(), Path(folders_absolute[1]).joinpath(norm_name))
            elif files.suffix.upper() in ('.MP3', '.OGG', '.WAV', '.AMR'):
                norm_name = normalize(files.name)
                shutil.move(files.absolute(), Path(folders_absolute[2]).joinpath(norm_name))
            elif files.suffix.upper() in  ('.ZIP', '.GZ', '.TAR'):
                norm_name = normalize(files.name)
                name_without = re.sub('\.\w+$', '', norm_name)                
                try:
                    shutil.unpack_archive(files.absolute(), Path(folders_absolute[4]).joinpath(name_without))
                except:
                    print(f'неможливо розпакувати архів {files.name}, видалення')
                finally:
                    os.remove(files.absolute())   
            else:
                shutil.move(files.absolute(), Path(folders_absolute[5]).joinpath(files.name))                
             
        elif files.is_dir():            
            if files.name in folders:
                continue                       
            else:                              
                list_of_bad_folders.append(files)
                find_files(files)


def normalize(not_normal_name): # функція перейменування 
    map = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G', 33: '_', 64: '_', 35: '_', 36: '_', 37: '_', 94: '_', 38: '_', 40: '_', 41: '_', 45: '_', 43: '_', 59: '_', 46: '_', 44: '_', 32: '_'}    
    suffix = re.search('\.\w+$', not_normal_name)                   # визначення розширення файлу
    name_without_suf = re.sub(suffix.group(), '', not_normal_name)  # видалення розширення 
    name_without_suf2 = name_without_suf.translate(map)             # перейменування файлу
    norm_name = name_without_suf2 + suffix.group()                  # повернення розширення

    return norm_name

if __name__ == '__main__':
    main()