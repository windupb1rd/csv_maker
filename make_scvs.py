import os
import datetime
import database


def start_making_csv_from_web(data):  # строки подаются через браузер, на выходе скачиваются файлы в зип архиве
    f = sorted(set(data.splitlines()))
    path_to_output_files = 'files/output'

    if os.path.exists(path_to_output_files):
        os.system(f'rm -r {path_to_output_files}')
        os.system(f'mkdir {path_to_output_files}')
    elif not os.path.exists(f'{path_to_output_files}'):
        os.system(f'mkdir {path_to_output_files}')

    creation_time = str(datetime.datetime.now())
    filename = creation_time.replace(' ', '-').replace(':', '-').replace('.', '-')
    source_query_file = open(f"files/source-{filename}.txt", 'w')
    source_query_file.write(data)
    source_query_file.close()

    number_of_output_files = (len(f) // 40) + 1 if len(f) % 40 != 0 else len(f) // 40
    cut_left, cut_right = 0, 40
    for file_number in range(1, number_of_output_files + 1):
        output = open(f'files/output/output{file_number}.csv', 'w')
        output.write(','.join(f[cut_left:cut_right]))
        output.close()
        cut_left += 40
        cut_right += 40 if len(f) >= 40 * file_number else (len(f) - (40 * file_number))

        os.system(f'cd {path_to_output_files}')
        os.system(f"7z a -tzip files/{filename}.zip ./{path_to_output_files}/*")  # точка в начале пути не включает дерево каталогов в архив

    database.add_to_db(creation_time, filename)

    return (filename,
            creation_time,
            f'Всего уникальных записей {len(f)},<br><br>Создано {number_of_output_files} файлов<br><br>{"-" * 50}')
