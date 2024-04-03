# Reserve_vk_yandex

Run to save photoes with the biggest available size from VK profile <vk_id\> to YaDisk path: "disk:/vk_backup/id_\<vk_id\>/\<album_name\>/\<date\>/"  

- By default \<album_name\>="profile"  
- By default photoes_save_count_max=5  

- Photoes are saved with names which respond their likes count  
- If there is photo with likes count as the other one then name also contaions unix timestamp

## Run on Windows (tested)
- create "config.txt" like "default_config.txt" in project_root_dir and edit token values to be valid
- install python 3.9.10 with pip3 and module "venv"
- python3 -m venv venv
- venv/Scripts/activate
- pip install requierments.txt
- python main.py

## Where you can get tokens
- https://yandex.ru/dev/disk/poligon
- https://id.vk.com/about/business

## Example of execution
```
python main.py

Tests_api_working...
        Init_api_objects...OK
        VK:...OK
        Yandex...OK
Tests_OK


Get_photoes_info_from_vk.....ok

Processing_photoes_info.....ok

Create_vk_backup_folder.....ok

Create_profile_id_folder.....ok

Create_album_name_folder.....ok

Create_date_time_folder.....ok

Create_uploading_tasks...
        Task_1_of_7: 26.jpg..ok
        Task_2_of_7: 20.jpg..ok
        Task_3_of_7: 29.jpg..ok
        Task_4_of_7: 22.jpg..ok
        Task_5_of_7: 35.jpg..ok
        Task_6_of_7: 26_1503304269.jpg..ok
        Task_7_of_7: 8.jpg..ok
..ok

Check_operations_id...
        Check_status_1_of_7: 26.jpg.....ok
        Check_status_2_of_7: 20.jpg.....ok
        Check_status_3_of_7: 29.jpg.........ok
        Check_status_4_of_7: 22.jpg.....ok
        Check_status_5_of_7: 35.jpg.....ok
        Check_status_6_of_7: 26_1503304269.jpg.....ok
        Check_status_7_of_7: 8.jpg.....ok
..ok


Result:
{ 'count': 7,
  'path': 'disk:/vk_backup/id_111111/profile/2024_04_04_14_36_35',
  'photoes': [ {'file_name': '26.jpg', 'size': 'y', 'upload_status': 'success'},
               {'file_name': '20.jpg', 'size': 'y', 'upload_status': 'success'},
               {'file_name': '29.jpg', 'size': 'z', 'upload_status': 'success'},
               {'file_name': '22.jpg', 'size': 'z', 'upload_status': 'success'},
               {'file_name': '35.jpg', 'size': 'z', 'upload_status': 'success'},
               {'file_name': '26_1503304269.jpg', 'size': 'z', 'upload_status': 'success'},
               {'file_name': '8.jpg', 'size': 'z', 'upload_status': 'success'}]}
```