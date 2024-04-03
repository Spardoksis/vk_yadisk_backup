"""
More info: README.md
"""
import datetime
import json
import pprint
import time


from vk import VK
from yandex import Yandex


def get_tokens(config_path="default_config.txt"):
    with open(config_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        vk_data = lines[0].strip().split(":")[1].strip()
        vk_user_id = vk_data.split(" ")[0]
        vk_token = vk_data.split(" ")[1]

        yandex_data = lines[1].strip().split(":")[1].strip()
        yandex_token = yandex_data.split(" ")[0]

        return vk_user_id, vk_token, yandex_token


def test_api_working(config_path="config.txt"):
    print("\nTests_api_working...")

    print("\tInit_api_objects...", end="")
    try:
        vk_user_id, vk_token, yandex_token = get_tokens(config_path)
        vk = VK(access_token=vk_token, user_id=vk_user_id)
        yandex = Yandex(access_token=yandex_token)
    except Exception as e:
        print("Error: ", end="")
        print(e)
        print("Tests_FAILED\n")
        exit(1)
    print("OK")

    ok = True
    print("\tVK:...", end="")
    vk_data = vk.users_info()
    if "error" in vk_data:
        ok = False
        print("Error: ", end="")
        print(vk_data)
    else:
        print("OK")

    print("\tYandex...", end="")
    yandex_data = yandex.users_info()
    if "error" in yandex_data:
        ok = False
        print("Error: ", end="")
        print(yandex_data)
    else:
        print("OK")

    if ok:
        print("Tests_OK\n")
    else:
        print("Tests_FAILED\n")
        exit(1)


def do_backup(
    config_path="config.txt", photoes_save_count_max=5, album_name="profile"
):
    if photoes_save_count_max < 1:
        print("Error: photoes_save_count_max must be > 0")
        exit(1)

    vk_user_id, vk_token, yandex_token = get_tokens(config_path)
    vk = VK(access_token=vk_token, user_id=vk_user_id)
    yandex = Yandex(access_token=yandex_token)

    # get the list of photos from vk album_name with likes info and size info
    print("\nGet_photoes_info_from_vk...", end="")
    vk_data_info = vk.photos_get(
        owner_id=vk_user_id, extended=1, photo_sizes=1, album_id=album_name
    )
    if "error" in vk_data_info:
        print("Error: ", end="")
        print(vk_data_info["error"])
        exit(1)
    else:
        print("..ok")

    # create json with userid, albumname, photos, likes, size, url, dates
    print("\nProcessing_photoes_info...", end="")
    vk_photoes_data = {}
    try:
        vk_photoes_data["vk_user_id"] = vk_user_id
        vk_photoes_data["album"] = "profile"
        vk_photoes_data["photoes"] = []
        vk_photoes_data["count"] = vk_data_info["response"]["count"]
        if photoes_save_count_max < vk_data_info["response"]["count"]:
            vk_photoes_data["count"] = photoes_save_count_max
        if vk_photoes_data["count"] == 0:
            print("Error: no photos found")
            exit(1)
        photo_count = photoes_save_count_max
        for photo_info in vk_data_info["response"]["items"]:
            if photo_count == 0:
                break
            biggest_photo = photo_info["sizes"][-1]
            vk_photoes_data["photoes"].append(
                {
                    "url": biggest_photo["url"],
                    "likes": photo_info["likes"]["count"],
                    "size": biggest_photo["type"],
                    "date": photo_info["date"],
                }
            )
            photo_count -= 1
    except Exception as e:
        print("Error: ", end="")
        print(e)
        exit(1)
    print("..ok")

    # create vk_backup folder in yadisk, not error if exists
    print("\nCreate_vk_backup_folder...", end="")
    vk_backup_path_info = yandex.create_dir("disk:", "vk_backup")
    if "error" in vk_backup_path_info:
        possible_yandisk_errors = ["DiskPathPointsToExistentDirectoryError"]
        if vk_backup_path_info["error"] in possible_yandisk_errors:
            print(vk_backup_path_info["error"])
        else:
            print("Error: ", end="")
            print(vk_backup_path_info["error"])
            exit(1)
    else:
        print("..ok")

    # create profile_id folder in vk_backup, not error if exists
    print("\nCreate_profile_id_folder...", end="")
    path = "disk:/vk_backup"
    profile_id_path_info = yandex.create_dir(path, "id_" + str(vk_user_id))
    if "error" in profile_id_path_info:
        possible_yandisk_errors = ["DiskPathPointsToExistentDirectoryError"]
        if profile_id_path_info["error"] in possible_yandisk_errors:
            print(profile_id_path_info["error"])
        else:
            print("Error: ", end="")
            print(profile_id_path_info["error"])
            exit(1)
    else:
        print("..ok")

    # create album name folder in profile_id, not error if exists
    print("\nCreate_album_name_folder...", end="")
    path = path + "/id_" + str(vk_user_id)
    album_name_path_info = yandex.create_dir(path,
                                             str(vk_photoes_data["album"]))
    if "error" in album_name_path_info:
        possible_yandisk_errors = ["DiskPathPointsToExistentDirectoryError"]
        if album_name_path_info["error"] in possible_yandisk_errors:
            print(album_name_path_info["error"])
        else:
            print("Error: ", end="")
            print(album_name_path_info["error"])
            exit(1)
    else:
        print("..ok")

    # create dir with date_time name in profile_id dir
    print("\nCreate_date_time_folder...", end="")
    dt_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    path = path + "/" + str(vk_photoes_data["album"])
    date_time_path_info = yandex.create_dir(path, str(dt_name))
    if "error" in date_time_path_info:
        print("Error: ", end="")
        print(date_time_path_info["error"])
        exit(1)
    else:
        print("..ok")

    # create uploading photoes tasks to yadisk
    print("\nCreate_uploading_tasks...")
    yadisk_photoes_data = {}
    yadisk_photoes_data["photoes"] = []
    path = path + "/" + str(dt_name)
    yadisk_photoes_data["path"] = path
    yadisk_photoes_data["count"] = vk_photoes_data["count"]
    photo_number = 1
    processed_names = []
    for photo in vk_photoes_data["photoes"]:
        photo_name = str(photo["likes"]) + ".jpg"
        if photo_name in processed_names:
            photo_name =\
                str(photo["likes"]) + "_" + str(photo["date"]) + ".jpg"
        print(
            f'\tTask_{photo_number}_of_{yadisk_photoes_data["count"]}: ' +
            photo_name,
            end="",
        )
        upload_task_result = yandex.upload_file_by_href(
            photo["url"], path + "/" + photo_name
        )
        if "error" in upload_task_result:
            print("\tError: ", end="")
            print(upload_task_result["error"])
            yadisk_photoes_data["count"] -= 1
            photo_number += 1
            continue
        operataion_id = upload_task_result["href"].split("/")[-1]
        yadisk_photoes_data["photoes"].append(
            {
                "file_name": photo_name,
                "size": photo["size"],
                "upload_status": operataion_id,
            }
        )
        print("..ok")
        processed_names.append(photo_name)
        photo_number += 1
    print("..ok")

    # check uplod status
    print("\nCheck_operations_id...")
    photo_number = 1
    for photo in yadisk_photoes_data["photoes"]:
        status = "error"
        tryes = 5
        print(
            f'\tCheck_status_{photo_number}_of_' +
            f'{yadisk_photoes_data["count"]}: ' +
            f'{photo["file_name"]}...',
            end="",
        )
        while tryes > 0:
            operation_info =\
                yandex.get_operation_status(photo["upload_status"])
            if "error" in operation_info:
                print("Error: ", end="")
                print(operation_info["error"])
                status = "error"
                break
            else:
                status = operation_info["status"]
                if status == "in-progress":
                    time.sleep(1)
                    print("..", end="")
                else:
                    print("..ok")
                    # print(operation_info)
                    break
            tryes -= 1
        if tryes == 0:
            status = "get_status_timout_error"
            print(status)
        photo["upload_status"] = status
        photo_number += 1
    print("..ok")

    # return json with status
    print("\n\nResult:")
    pprint.pprint(yadisk_photoes_data, indent=2, width=120)
    with open("result.json", "w", encoding="utf-8") as outfile:
        json.dump(yadisk_photoes_data, outfile)


if __name__ == "__main__":
    test_api_working()
    do_backup()
