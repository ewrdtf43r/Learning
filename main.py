import os
from zipfile import ZipFile


def found_file_count(path):
    archive_format = ("zip", "iso", "7z", "dmg")
    rez = os.listdir(path)
    count = 0
    for elem in rez:
        if len(elem.split(".")) == 1:
            count += found_file_count(f"{path}/{elem}")
            count += 1
        elif len(elem.split(".")) == 2:
            if elem.split(".")[1] in archive_format:
                count += zip_file_count_file(f"{path}/{elem}")
                count += 1
            else:
                count += 1
    return count


def zip_file_count_file(path):
    archive_format = ("zip", "iso", "7z", "dmg")
    count = 0
    curr_path = None
    with ZipFile(path) as zf:
        for elem in zf.namelist():
            if len(elem.split(".")) == 2 and len(elem.split("/")) >= 2:
                for item in elem.split("/")[:-1]:
                    if curr_path != item:
                        curr_path = item
                        count += 1

    count += len(zf.namelist())
    return count


if __name__ == "__main__":
    archive_format = ("zip", "iso", "7z", "dmg")
    list_dir = []
    print("A Script for finding the most 'littered' files in some directory")
    root_dir = input("Enter the directory: ")
    kb = " KB"
    bt = " BT"

    for local_dir in os.listdir(root_dir):
        if len(local_dir.split(".")) == 2:
            if local_dir.split(".")[1] in archive_format:
                list_dir.append([local_dir, zip_file_count_file(f"{root_dir}/{local_dir}"),
                                 os.path.getsize(f"{root_dir}"f"/{local_dir}")])
            else:
                continue
        else:
            list_dir.append([local_dir, found_file_count(f"{root_dir}/{local_dir}"),
                             os.path.getsize(f"{root_dir}/{local_dir}")])

    for elem in sorted(sorted(list_dir, key=lambda x: -x[1])[:10], key=lambda x: -x[2]):
        print(f"Directory - '{elem[0]}' | Number of files - {elem[1]} | Size - "
              f"{str(elem[2]) + bt if elem[2] < 1024 else str(elem[2] / 1024) + kb}")
