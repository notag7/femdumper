################## IMPORT #########################
from colorama import init, Fore
import os
import time
import sys
import re
import shutil
import ctypes
import msvcrt
import string
import random
import threading
import psutil
import concurrent.futures
################## Colorama #######################
init()

################## Functions #######################
def generate_random_title():
    while True:
        random_title = ''.join(random.choice(string.ascii_letters) for _ in range(20))
        ctypes.windll.kernel32.SetConsoleTitleW(f"{random_title}")
        time.sleep(0.1) 

def terminate():
    print(f"{Fore.RED} Programm will terminate in 3 sec!")
    time.sleep(3)
    current_system_pid = os.getpid()

    ThisSystem = psutil.Process(current_system_pid)
    ThisSystem.terminate()
    sys.exit()

def display_title():
    colorama_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    random_color = random.choice(colorama_colors)

    title = f"""
###################################################################### 
  ______             _____                                  
 |  ____|           |  __ \\                                 
 | |__ ___ _ __ ___ | |  | |_   _ _ __ ___  _ __   ___ _ __ 
 |  __/ _ \\ '_ ` _ \\| |  | | | | | '_ ` _ \\| '_ \\ / _ \\ '__|
 | | |  __/ | | | | | |__| | |_| | | | | | | |_) |  __/ |   
 |_|  \\___|_| |_| |_|_____/ \\__,_|_| |_| |_| .__/ \\___|_|   
                                           | |              
                                           |_|              

                                                Made by Femscripts.de    
######################################################################                                                      
    """
    print(random_color + title + Fore.RESET)

hwnd = ctypes.windll.kernel32.GetConsoleWindow()
TriggerPath = "None"
WebhookFilePath = os.path.join(os.path.expanduser("~/Desktop"), "discord_webhooks.txt")
VarFilePath = os.path.join(os.path.expanduser("~/Desktop"), "variables.txt")
tiggerFilePath = os.path.join(os.path.expanduser("~/Desktop"), "trigger_events.txt")
ac_keywords_file_path = os.path.join(os.path.expanduser("~/Desktop"), "anticheat_keywords.txt")
acs_founds_file_path = os.path.join(os.path.expanduser("~/Desktop"), "acs_founds.txt")
AnticheatKeywords = ["Anticheat", "Godmode", "Noclip", "Eulen", "Detection", "Shield", "Fiveguard", "Noclip", "deltax", "waveshield", "spaceshield", "mixas", "protected", "cheater", "cheat", "banNoclip", "Detects", "GetHashKey('", "blacklisted", "CHEATER BANNED:", "core_shield", "freecam"]
folders_to_ignore = ["monitor", "easyadmin"]
extensions_to_search = [".lua", ".html", ".js", ".json"]
anticheat_found = False  

def clear_screen():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ("nt", "dos", "ce"):
        os.system("cls")

def type_writer_animation(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def check_directory(path):
    if os.path.exists(path):
        contents = os.listdir(path)
        if contents:
            global TriggerPath
            TriggerPath = path
            type_writer_animation(Fore.GREEN + f"Path set to: ")
            print(f"{TriggerPath}")
        else:
            type_writer_animation(Fore.RED + "The specified directory is empty.")
    else:
        type_writer_animation(Fore.RED + "The specified path does not exist.")

def loadingscreen2():
    clear_screen()
    print("Loading:")
    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for i in range(len(animation)):
        time.sleep(0.2)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")
    clear_screen()

def loadingscreen():
    type_writer_animation(Fore.GREEN + "Boooting Tool.......")
    loadingscreen2()
    clear_screen()
    type_writer_animation(Fore.MAGENTA + "Made by FemScripts.de !")
    clear_screen()

def find_and_list_trigger_events(path, output_file):
    trigger_events = []
    total_files = sum([len(files) for _, _, files in os.walk(path)])
    processed_files = 0

    with open(output_file, "w", encoding="utf-8") as output:
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith(".lua"):
                    file_path = os.path.join(root, filename)
                    folder_name = os.path.basename(os.path.dirname(file_path))
                    try:
                        with open(file_path, "r", encoding="latin-1") as file:
                            for line_number, line in enumerate(file, start=1):
                                if re.search(r"\b(TriggerServerEvent|TriggerEvent)\b", line):
                                    trigger_events.append((folder_name, line_number, line.strip()))
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
                    
                    processed_files += 1
                    print(f"\rProcessing files: {processed_files}/{total_files}", end='', flush=True)

        for event in trigger_events:
            output.write(f"\n{'='*25} [{event[0]} - Line {event[1]}] {'='*25}\n")
            output.write(f"{event[2]}\n")

    print("\nProcessing complete.")

def find_discord_webhooks(path, output_file):
    webhook_urls = []
    webhook_pattern = re.compile(r"https://discord\.com/api/webhooks/\w+/\w+")

    total_files = sum([len(files) for _, _, files in os.walk(path)])
    processed_files = 0

    print(Fore.CYAN + "-------------------------------------------------------------------------------" + Fore.RESET)
    print(Fore.CYAN + "Searching for Discord webhooks..." + Fore.RESET)
    print(Fore.CYAN + "-------------------------------------------------------------------------------" + Fore.RESET)

    def process_file(full_path):
        nonlocal processed_files
        with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            matches = webhook_pattern.findall(content)
            if matches:
                webhook_urls.extend([(full_path, match) for match in matches])
            processed_files += 1
            print(f"\r{Fore.CYAN}Progress: {processed_files}/{total_files}{Fore.RESET}", end='', flush=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                full_path = os.path.join(root, filename)
                if os.path.isfile(full_path):
                    futures.append(executor.submit(process_file, full_path))
        for future in concurrent.futures.as_completed(futures):
            future.result()
    print("\n" + Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
    print(Fore.GREEN + "Webhook search complete." + Fore.RESET)
    print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)

    with open(output_file, "w", encoding="utf-8") as output:
        output.write(f"File Path| Webhook URL")
        output.write(f"{'-'*80}\n")
        for webhook_url in webhook_urls:
            output.write(f"{webhook_url[0]:<60} | {webhook_url[1]}\n")

    return webhook_urls


def print_separator():
    print(Fore.WHITE + "-" * 50)

def print_header(title):
    print(Fore.YELLOW + title.center(50))
    print_separator()

def find_and_list_variables(path, output_file):
    variables_list = []

    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".lua"):
                file_path = os.path.join(root, filename)
                folder_name = os.path.basename(os.path.dirname(file_path))
                with open(file_path, "r", encoding="latin-1") as file:
                    for line_number, line in enumerate(file, start=1):
                        if re.search(r'\bvar_\w+\b', line):
                            variables_list.append((folder_name, line_number, line.strip()))

    with open(output_file, "a", encoding="utf-8") as output:
        output.write("\nVariables:\n")
        for variable in variables_list:
            output.write(f"[{variable[0]}] - [Line {variable[1]}] {variable[2]}\n")

def check_for_acs_in_path(path, output_file):
    files_to_check = {
        "shared_fg-obfuscated.lua": "FiveGuard",
        "fini_events.lua": "FiniAC",
        "c-bypass.lua": "Reaper-AC",
        "waveshield.lua": "WaveShield"
    }

    with open(output_file, "a", encoding="utf-8") as output:
        for file_to_check, detection_name in files_to_check.items():
            output.write(f"#######################################################################################\n")
            output.write(f"\nChecking for {file_to_check}:\n")
            output.write(f"#######################################################################################\n")
            for root, dirs, files in os.walk(path):
                for filename in files:
                    if filename == file_to_check:
                        file_path = os.path.join(root, filename)
                        folder_name = os.path.basename(os.path.dirname(file_path))
                        output.write(f"#######################################################################################\n")
                        output.write(f"{detection_name} Detected AC: ( {folder_name} )\n")
                        output.write(f"#######################################################################################\n")

def save_anticheat_found_files(path, extensions, ignored_folders, output_file):
    anticheat_events = []

    for root, dirs, files in os.walk(path):
        for folder in ignored_folders:
            if folder in dirs:
                dirs.remove(folder)

        for filename in files:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, filename)
                folder_name = os.path.basename(os.path.dirname(file_path))
                with open(file_path, "r", encoding="latin-1") as file:
                    for line_number, line in enumerate(file, start=1):
                        for keyword in AnticheatKeywords:
                            if keyword in line:
                                anticheat_events.append((folder_name, line_number, line.strip()))

    with open(output_file, "w", encoding="utf-8") as output:
        for event in anticheat_events:
            output.write(f"[{event[0]}] - [Line {event[1]}] {event[2]}\n")

def check_for_anticheat_keywords():
    print("-------------------------------------------------------------------------------")
    print(f"Keywords: {AnticheatKeywords}")
    print("-------------------------------------------------------------------------------")
    type_writer_animation(Fore.RED + "Keep in mind that an anticheat may inject into all resources. The result could be spammed!")
    anticheat_found = False
    total_files = sum([len(files) for _, _, files in os.walk(TriggerPath)])
    processed_files = 0

    with open(ac_keywords_file_path, "w", encoding="utf-8") as output:
        for root, dirs, files in os.walk(TriggerPath):
            for filename in files:
                if filename.endswith(".lua"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, "r", encoding="latin-1") as file:
                        for line in file:
                            for keyword in AnticheatKeywords:
                                if keyword in line:
                                    anticheat_found = True
                                    output.write(f"\n{'='*25} Anticheat Keywords Found in [{file_path}] {'='*25}\n")
                                    output.write(f"{line.strip()}\n")
                                    break
                    processed_files += 1
                    print(f"\r{Fore.CYAN}Progress: {processed_files}/{total_files}{Fore.RESET}", end='', flush=True)
                    if anticheat_found:
                        break

    if not anticheat_found:
        print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
        type_writer_animation(Fore.RED + "No Anticheat found.")
    else:
        clear_screen()
        print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
        type_writer_animation(Fore.WHITE + "Anticheat Keywords found! File saved to Desktop.")
    time.sleep(1)

title_thread = threading.Thread(target=generate_random_title)
title_thread.start()
loadingscreen()
while True:
    clear_screen()
    display_title()
    print(Fore.CYAN + "Current Path: " + Fore.WHITE + TriggerPath + Fore.RESET)
    print("\n")
    print("######################################")
    print(Fore.WHITE + "1. Select Path")
    print(Fore.WHITE + "2. Find Triggers")
    print(Fore.WHITE + "3. Find Discord Webhooks")
    print(Fore.WHITE + "4. Try to Find Anticheat")
    print(Fore.WHITE + "5. Find Variables")  
    print(Fore.WHITE + "6. Run All Scans")  
    print(Fore.WHITE + "7. Exit")  
    print("######################################")
    print("\n")
    prompt = "[>] "
    choice = input(Fore.YELLOW + prompt + Fore.RESET)

    if choice == "1":
        clear_screen()
        print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
        path = input(Fore.BLUE + "Input Server dump folder: ")
        print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
        check_directory(path)
    elif choice == "2":
        print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
        type_writer_animation(Fore.BLUE + "Finding Triggers......")
        print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
        if TriggerPath != "None":
            find_and_list_trigger_events(TriggerPath, tiggerFilePath)
            clear_screen()
            print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
            type_writer_animation(Fore.GREEN + "Done! You can find the txt on your Desktop!")
            print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
        else:
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
            type_writer_animation(Fore.RED + "Set the path first!")
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
    elif choice == "3":
        clear_screen()
        print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
        type_writer_animation(Fore.GREEN + "Finding Discord Webhooks...... (This may take a moment!)")
        print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
        if TriggerPath != "None":
            webhook_urls = find_discord_webhooks(TriggerPath, WebhookFilePath)
            if webhook_urls:
                print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
                type_writer_animation(Fore.WHITE + "Discord Webhooks found. Check it out on your Desktop")
                print(Fore.GREEN + "-------------------------------------------------------------------------------" + Fore.RESET)
            else:
                type_writer_animation(Fore.RED + "Done. If nothing is there. Then no webhook found!")
                print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
                type_writer_animation(Fore.BLUE + "Press any key to continue...")
                msvcrt.getch()
        else:
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
            type_writer_animation(Fore.RED + "Set the path first!")
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
    elif choice == "4":
            clear_screen()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.WHITE + "Trying to find Anticheat using keywords...")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            check_for_anticheat_keywords()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.WHITE + "Trying to find popular AC's")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            check_for_acs_in_path(path, acs_founds_file_path)
    elif choice == "5":
        print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
        type_writer_animation(Fore.GREEN + "Working on it..................................................")
        print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
        find_and_list_variables(TriggerPath, VarFilePath)  
        clear_screen()
        print("-------------------------------------------------------------------------------")
        type_writer_animation(Fore.GREEN + "Done! Variables listed in the txt on your Desktop!")
        print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
        time.sleep(1)

    elif choice == "6":
        if TriggerPath != "None":
            clear_screen()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.GREEN + "Running ALL options...")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            time.sleep(0.1)

            clear_screen()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.BLUE + "Finding Triggers...")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            find_and_list_trigger_events(TriggerPath, tiggerFilePath)


            clear_screen()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.GREEN + "Finding Discord Webhooks...")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            find_discord_webhooks(TriggerPath, WebhookFilePath)


            clear_screen()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.WHITE + "Trying to find Anticheat using keywords...")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            check_for_anticheat_keywords()
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            type_writer_animation(Fore.WHITE + "Trying to find popular AC's")
            print(Fore.RED + "-------------------------------------------------------------------------------"+ Fore.RESET)
            check_for_acs_in_path(path, acs_founds_file_path)


            clear_screen()
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
            type_writer_animation(Fore.GREEN + "Finding Variables...")
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
            find_and_list_variables(TriggerPath, VarFilePath)

            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
            type_writer_animation(Fore.GREEN + "ALL options completed! Check your Desktop for the Results")
            print(Fore.RED + "-------------------------------------------------------------------------------" + Fore.RESET)
        else:
            print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
            type_writer_animation(Fore.RED + "Set the path first!")
            print(Fore.YELLOW + "-------------------------------------------------------------------------------" + Fore.RESET)
    elif choice == "7":
        print(Fore.MAGENTA + "-------------------------------------------------------------------------------" + Fore.RESET)
        type_writer_animation(Fore.MAGENTA +"Bye <3 ! ")
        print(Fore.MAGENTA + "-------------------------------------------------------------------------------" + Fore.RESET)
        title_thread.join()
        exit(0)

    else:
        type_writer_animation(Fore.RED + "You Serious?")

    if anticheat_found:
        anticheat_found = False

