from datetime import datetime, timedelta, timezone
import time
from PIL import Image
import configparser
import requests
import wget
import os
import csv
import shutil
from UTC_time_stamp import UTC_time_stamp
from file_prefixes import file_prefixes
from supersleep import supersleep
from countdown import countdown

try:
    #Uses wget Python module for the download process.
    #Checks which directory the program is running in and uses that to locate the .cfg file with settings.
    connection = requests.get("https://cdn.star.nesdis.noaa.gov/", timeout=10)
    print("Internet Connection is working.")    

    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = current_dir.replace("\\", "/")
    cfg = configparser.RawConfigParser()
    cfg.read(current_dir + "/goes_image_settings.cfg")
    if shutil.disk_usage(cfg["image_file_paths"]["partial_save_path"]).free == 0:
        raise shutil.Error
    
    if os.path.exists(cfg["image_file_paths"]["partial_save_path"]) == False or os.path.exists(cfg["image_file_paths"]["save_path"]) == False:
        raise FileNotFoundError()

    start_prog = datetime.now(timezone.utc)
    while True:
        goes_sat = input("Select which satellite to download images from (GOES-16 or GOES-17) by typing its name, e.g. GOES16: ")
        if goes_sat == "GOES16" or goes_sat == "goes16" or goes_sat == "GOES17" or goes_sat == "goes17":
            break
        else:
            print("Invalid satellite name, please try 'GOES16' or 'GOES17'.")

    goes_dir = input("Set the name of the directory that will contain the images from " + goes_sat + ": ")
    if goes_dir == "":
        goes_dir = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H-%M-%S_UTC")

    if goes_sat == "GOES16" or goes_sat == "goes16":
        goes_sat_dir = "GOES_16"
    elif goes_sat == "GOES17" or goes_sat == "goes17":
        goes_sat_dir = "GOES_17"

    mkdir_command = str(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir)
    os.mkdir(mkdir_command)
    print("A directory called", goes_dir, "has been created for the image download.")
    print("The path is:", mkdir_command)
    os.chdir(mkdir_command)

    while True:
        start = UTC_time_stamp(input("Set a start time in UTC for the download of the first image, e.g. 2020-05-11 22:20:00: "))
        if (datetime.now(timezone.utc) - start) <= timedelta(days=3):
            break
        elif (datetime.now(timezone.utc) - start) >= timedelta(days=3):
            print("Too old a date, must be less than 3 days ago.")

    while True:
        stop = UTC_time_stamp(input("Set a stop time in UTC for the download of the final image, e.g. 2020-05-11 22:30:00: "))
        if stop > start:
            break
        elif stop < start:
            print("Stop time is earlier than start time, please try another stop time.")

    start_date = start.strftime("%Y-%m-%d")

    while True:
        image_res = int(input("These are the image resolutions available:\n339x339 pixels\n678x678 pixels\n1808x1808 pixels\n5424x5424 pixels\n10848x10848 pixels\nSelect a resolution by typing either of these values, e.g. 10848: "))
        if image_res == 339 or image_res == 678 or image_res == 1808 or image_res == 5424 or image_res == 10848:
            break
        else:
            print("Invalid resolution value, please try one of the listed values.")

    recording_time = timedelta.total_seconds(stop - start)
    while True:
        image_freq = int(input("For " + goes_sat + " set number to be skipped: "))
        if image_freq < 0:
            print("The number of images to be skipped cannot be a negative value, please try again.")
        else:
            break

    image_interval = 600 * (1 + image_freq)
    number_of_images = int(recording_time/image_interval)
    print("The number of images to be downloaded is: " + str(number_of_images))
    exit_com = str(input("Do you wish to proceed with the download? [Y/n]: "))
    if exit_com == "Y" or exit_com == "y":
        pass
    elif exit_com == "n" or exit_com == "N":
        os.rmdir(mkdir_command)
        exit()
    img_dict = {}
    ts_dict  = {}
    for i in range(number_of_images):
        year_start = datetime(start.year, 1, 1, tzinfo=timezone.utc)
        timestamp = timedelta(minutes = (i * image_interval/60)) + start 
        image_date = str(timestamp.year) + '{0:03d}'.format(timestamp.toordinal() - year_start.toordinal() + 1) + '{0:02d}'.format(timestamp.hour) + '{0:02d}'.format(timestamp.minute)
        print("Image_date: " + image_date)
        img_dict[i] = image_date
        ts_dict[i]  = timestamp

    wait = max(0, 1200 + timedelta.total_seconds(start - datetime.now(timezone.utc)))
    print("The wait time is: " + countdown(wait))
    supersleep(wait)

    dummy_counter = 0
    speed_list = []
    with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "a", newline="") as csv_index:
                field_names = ["file_name", "file_size", "time", "download_speed"]
                writer = csv.DictWriter(csv_index, fieldnames=field_names)
                writer.writeheader()

    for no, img in img_dict.items():
        wait = max(0, 1200 + timedelta.total_seconds(ts_dict[no] - datetime.now(timezone.utc)) + int(cfg["pause_times"]["server_wait_time"]))
        supersleep(wait)
        file_name = img + "_" + goes_sat + "-ABI-FD-GEOCOLOR-" + str(image_res) + "x" + str(image_res) + ".jpg"
        file_path = cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + file_name
        url = "https://cdn.star.nesdis.noaa.gov/" + goes_sat + "/ABI/FD/GEOCOLOR/" + img + "_" + goes_sat + "-ABI-FD-GEOCOLOR-" + str(image_res) + "x" + str(image_res) + ".jpg"
        exists = requests.get(url)
        if len(exists.content) >= shutil.disk_usage(cfg["image_file_paths"]["partial_save_path"]).free:
            raise shutil.Error
        if exists:
            print("-- " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") + " --  " + url)
            print("Downloading image number " + str(no + 1) + " of " + str(number_of_images) + " (" + str(round((((no + 1)/number_of_images) * 100), 4)) + "%). Dummy images: " + str(dummy_counter) + " of " + str(number_of_images) + " (" + str(round(((dummy_counter/number_of_images) * 100), 4)) + "%).\nLength: " + str(len(exists.content)) + " (" + file_prefixes(len(exists.content)) + ") [image/jpeg]\nSaving to: " + file_name)
            speed_start = time.time()
            wget.download(url, file_name)
            speed_stop = time.time()
            print("\n")
            speed_total = speed_stop - speed_start
            avg = len(exists.content)/speed_total
            speed_list.append(avg)
            with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "a", newline="") as csv_index:
                field_names = ["file_name", "file_size", "time", "download_speed"]
                writer = csv.DictWriter(csv_index, fieldnames=field_names)
                writer.writerow({"file_name": file_name, "file_size": len(exists.content), "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "download_speed": str(int(avg))})
            print(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + file_prefixes(avg) + "/s)" + " - " + file_name + " saved [" + str(os.path.getsize(file_path)) + "/" + str(len(exists.content)) + "]\n")
        else:
            img_ex = Image.new("RGB", (image_res, image_res), color = "black")
            img_ex.save(file_path)
            with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "a", newline="") as csv_index:
                field_names = ["file_name", "file_size", "time", "download_speed"]
                writer = csv.DictWriter(csv_index, fieldnames=field_names)
                writer.writerow({"file_name": file_name, "file_size": os.path.getsize(file_path), "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "download_speed": "N/A"})
            dummy_counter += 1
            print("Image not found, generating dummy image. Image number " + str(no + 1) + " of " + str(number_of_images) + ".\n")

    file_size_list = []

    with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "r", newline="") as csv_index:
        reader = csv.DictReader(csv_index)
        for row in reader:
            file_size_list.append(int(row["file_size"]))

    min_size = file_prefixes(min(file_size_list))
    max_size = file_prefixes(max(file_size_list))
    avg_size = file_prefixes(sum(file_size_list)/len(file_size_list))
    total_size = file_prefixes(sum(file_size_list))

    if not speed_list:
        min_speed = "None"
        max_speed = "None"
        avg_speed = "None"
    else:
        min_speed = file_prefixes(min(speed_list)) + "/s"
        max_speed =  file_prefixes(max(speed_list)) + "/s"
        avg_speed = file_prefixes(sum(speed_list)/len(speed_list)) + "/s"

    for i, img in img_dict.items():
        filename = img + "_" + goes_sat + "-ABI-FD-GEOCOLOR-" + str(image_res) + "x" + str(image_res) + ".jpg"
        file = cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + filename
        print("Checking: " + file)
        if os.path.exists(file) == False:
            print("File does not exist, generating dummy image.")
            img_ex = Image.new("RGB", (image_res, image_res), color = "black")
            img_ex.save(file)
            with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "a", newline="") as csv_index:
                field_names = ["file_name", "file_size", "time", "download_speed"]
                writer = csv.DictWriter(csv_index, fieldnames=field_names)
                writer.writerow({"file_name": filename, "file_size": os.path.getsize(file), "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "download_speed": "N/A"})
            dummy_counter += 1
        elif os.path.getsize(file) == 0:
            print("File has size 0 bytes, generating dummy image.")
            with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "r", newline="") as csv_index:
                reader = csv.DictReader(csv_index)
                for row in reader:
                    size = int(row["file_size"])
                    if size == 0:
                        img_ex = Image.new("RGB", (image_res, image_res), color = "black")
                        img_ex.save(file)
                        with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_file_index_" + start_prog.strftime("%Y-%m-%d") + ".csv", "a", newline="") as csv_index:
                            field_names = ["file_name", "file_size", "time", "download_speed"]
                            writer = csv.DictWriter(csv_index, fieldnames=field_names)
                            writer.writerow({"file_name": filename, "file_size": os.path.getsize(file), "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "download_speed": "N/A"})
                        dummy_counter += 1

    print("Exiting program...")
    supersleep(5)

    stop_prog = datetime.now(timezone.utc)
    with open(cfg["image_file_paths"]["save_path"] + goes_sat_dir + "/" + goes_dir + "/" + goes_dir + "_download_info_" + start_prog.strftime("%Y-%m-%d") + ".txt", "wt") as info:
        info.write("UTC Start Time Image Download: " + start.strftime("%Y-%m-%d %H:%M:%S") + "\n" + "UTC Stop Time Image Download: " + stop.strftime("%Y-%m-%d %H:%M:%S") + "\n" + "UTC Program Start Time: " + start_prog.strftime("%Y-%m-%d %H:%M:%S.%f") + "\n" + "UTC Program Stop Time: " + stop_prog.strftime("%Y-%m-%d %H:%M:%S.%f") + "\n" + "Program runtime: " + countdown(timedelta.total_seconds(stop_prog - start_prog) - 5) + "\n" + "Image interval in seconds, default being 600: " + str(image_interval) + "\n" + "Total recording time: " + countdown(recording_time) + "\n" + "The image file size min/avg/max: " + min_size + "/" + avg_size + "/" + max_size + "\n" + "The download speed for the image files min - avg - max: " + min_speed + " - " + avg_speed + " - " + max_speed + "\n" + "The total amount of downloaded data: " + total_size + "\n" + "The number of images is: " + str(number_of_images) + "\n" + "The number of dummy images is: " + str(dummy_counter) + "\n" + "The image resolution in pixels is: " + str(image_res) + "x" + str(image_res) + "\n" + "The satellite is: " + goes_sat)

except (requests.ConnectionError, requests.Timeout) as exception:
    print("No internet connection.")

except FileNotFoundError:
    print("The gathering directory 'GOES_17' or 'GOES_16' appears not to exist. \nPlease check if the storage device where the folder is located is properly mounted or physically connected.")

except shutil.Error:
    print("Not enough storage space on the drive.")

except KeyboardInterrupt:
    print()
    print("User interrupted program by Ctrl + C.")

finally:
    print("Program exited.")
    supersleep(5)