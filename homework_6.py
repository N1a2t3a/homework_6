import sys
import os
import shutil

# коментар


def normalize(filename):
    normalized_filename = filename.replace(" ", "_")
    return normalized_filename

def process_folder(folder_path):
    ignored_folders = ['archives', 'video', 'audio', 'documents', 'images']
    extensions = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'music': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'RAR', '7Z']  
    }


    # Отримання поточної директорії, з якої запускається скрипт
    script_dir = os.path.abspath(folder_path)


    # Створення папок images та documents у поточній директорії
    for folder in ['images', 'documents']:
        target_folder_path = os.path.join(script_dir, folder)
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)


    # Створення папки archives у поточній директорії
    archives_folder = os.path.join(script_dir, 'archives')
    if not os.path.exists(archives_folder):
        os.makedirs(archives_folder)

    known_extensions = set()
    unknown_extensions = set()

    def process_file(file_path):
        filename = os.path.basename(file_path)
        file_extension = filename.split('.')[-1].upper()
        normalized_filename = normalize(filename)

        moved = False

        if file_extension in extensions.get('archives', []):
            # Обробка архівів
            dest_folder = os.path.join(archives_folder, os.path.splitext(normalized_filename)[0])
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            shutil.unpack_archive(file_path, dest_folder)
            moved = True
        elif file_extension == 'AUDIO':
            # Обробка аудіо файлів
            dest_folder = os.path.join(script_dir, 'audio')
            dest_path = os.path.join(dest_folder, normalized_filename)
            shutil.move(file_path, dest_path)
            moved = True
            known_extensions.add(file_extension)
        elif file_extension == 'VIDEO':
            # Обробка відео файлів
            dest_folder = os.path.join(script_dir, 'video')
            dest_path = os.path.join(dest_folder, normalized_filename)
            shutil.move(file_path, dest_path)
            moved = True
            known_extensions.add(file_extension)
        elif file_extension not in extensions['images'] and file_extension not in extensions['videos'] and file_extension not in extensions['documents'] and file_extension not in extensions['music']:
            # Обробка файлів з невідомим розширенням
            unknown_extensions.add(file_extension)
        else:
            # Обробка файлів з відомими розширеннями
            for category, ext_list in extensions.items():
                if file_extension in ext_list:
                    dest_folder = os.path.join(script_dir, category)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    dest_path = os.path.join(dest_folder, normalized_filename)
                    shutil.move(file_path, dest_path)
                    moved = True
                    known_extensions.add(file_extension)
                    break

        if not moved:
            # Якщо файл не було переміщено, залишаємо його без змін
            shutil.move(file_path, os.path.join(script_dir, normalized_filename))
            known_extensions.add(file_extension)

    for root, dirs, files in os.walk(script_dir):
        for ignored_folder in ignored_folders:
            if ignored_folder in dirs:
                dirs.remove(ignored_folder)  # Видалення ігнорованих папок зі списку обробки
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)

    # Видалення порожніх папок
    for root, dirs, files in os.walk(script_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

    # Формування звіту
    report = "Known Extensions:\n" + ', '.join(known_extensions) + "\n\n"
    report += "Unknown Extensions:\n" + ', '.join(unknown_extensions) + "\n\n"
    report += "Files in Categories:\n"
    for category, ext_list in extensions.items():
        report += category + ": " + str(len(os.listdir(os.path.join(script_dir, category)))) + " files\n"

    return report

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py /path/to/folder")
        sys.exit(1)

    folder_path = sys.argv[1]
    report = process_folder(folder_path)
    print(report)

