import configparser
import json
import os
import subprocess
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import random

config_path = os.path.join(os.path.dirname(__file__), "config")
notes_path = os.path.join(os.path.dirname(__file__), "notes")
settings = configparser.ConfigParser()
with open(config_path, encoding="utf-8") as config_file:
    settings.read_file(config_file)

# this is not a good program bro


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


print("pythet v0.1")
print("this thing sucks")
print("love from p3isc <3")
print("hold on")
detach_flags = {}
if os.name != 'nt':
    detach_flags['start_new_session'] = True

time.sleep(1.5)
clear()
time.sleep(1)
clear()

time.sleep(1)


def show_cat(message):
    print('   ／l、             ')
    print(f' （ﾟ､ ｡ ７  {message}')
    print('   l  ~ヽ  ')
    print('   じしf_,)ノ  ')

msg = random.randint(1, 6)
if msg == 1:
    cat_message = "what do you want to do today?"
elif msg == 2:
    cat_message = "meow :3"
elif msg == 3:
    cat_message = "guess what?"
elif msg == 4:
    cat_message = "hey, you would connect to spotatui right?"
elif msg == 5:
    cat_message = "choom"
elif msg == 6:
    cat_message = "nya~"

def a():
    global cat_message
    show_cat(cat_message)
    query = input('pythet >> ')
    clear_after_command = True

    if query.startswith('play '):
        song_name = query.replace('play ', '', 1)
        play_result = subprocess.run(
            ["spotatui", "play", "--track", "--name", song_name, "--format", "%s|%t"],
            capture_output=True,
            text=True
        )
        if play_result.returncode == 0:
            status, separator, title = play_result.stdout.strip().partition("|")
            if status == "▶" and separator and title:
                cat_message = f"playing... {title}"
            else:
                cat_message = "playing..."
        elif play_result.stderr:
            print(play_result.stderr.strip())
    elif query == 'stop song':
        print("stopping song")
        cat_message = "what do you want to do today?"
        subprocess.Popen(
            ["spotatui", "pb", "--toggle"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    elif query in ('exit', 'quit'):
        print("just press ctrl + c dum dum")
        time.sleep(3)
        clear()
        sys.exit()

    elif query == 'what':
        if cat_message == "guess what?":
            print('chicken butt')
            time.sleep(2)

#test to see if commit works

    elif query.startswith('what is '):
        search_text = query[len('what is '):].strip()
        if search_text:
            params = urlencode({
                "action": "query",
                "generator": "search",
                "gsrsearch": search_text,
                "gsrlimit": 1,
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
                "format": "json"
            })
            url = "https://simple.wikipedia.org/w/api.php?" + params
            request = Request(url, headers={"User-Agent": "pythet/0.1"})

            with urlopen(request) as response:
                pages = json.load(response).get("query", {}).get("pages", {})
            if pages:
                summary = next(iter(pages.values())).get("extract")
                if summary:
                    print(summary)
                    clear_after_command = False
        input("you would press enter right? well i wouldnt if i were in your shoes!")
        clear()

    elif query.startswith('was ist '):
            search_text = query[len('was ist '):].strip()
            if search_text:
                params = urlencode({
                    "action": "query",
                    "generator": "search",
                    "gsrsearch": search_text,
                    "gsrlimit": 1,
                    "prop": "extracts",
                    "exintro": 1,
                    "explaintext": 1,
                    "format": "json"
                })
                url = "https://de.wikipedia.org/w/api.php?" + params
                request = Request(url, headers={"User-Agent": "pythet/0.1"})
    
                with urlopen(request) as response:
                    pages = json.load(response).get("query", {}).get("pages", {})
                if pages:
                    summary = next(iter(pages.values())).get("extract")
                    if summary:
                        print(summary)
                        clear_after_command = False
            input("you would press enter right? well i wouldnt if i were in your shoes!")
            clear()

    elif query == 'status':
        status_result = subprocess.run(
            ["spotatui", "playback", "--status"],
            capture_output=True,
            text=True,
            **detach_flags
        )
        if status_result.returncode == 0:
            print(status_result.stdout.strip())
        elif status_result.stderr:
            print(status_result.stderr.strip())

    elif query == 'settings':
        settingquery = input("settings >> ").strip()
        if settingquery == 'browserurl':
            browser_url_choice = input("browserurl >> ").strip()
            if browser_url_choice:
                new_browser_url = settings["settings"].get(
                    browser_url_choice.lower(),
                    browser_url_choice
                )
                settings["settings"]["browserurl"] = new_browser_url
                with open(config_path, "w", encoding="utf-8") as config_file:
                    settings.write(config_file)
        if settingquery == 'help':
            print('browserurl: set the default browser search url')
            print('help: show this help message')
            input("press enter, NOW!")
            clear()

    elif query == 'shutdown':
        answer = input("shut down computer? >> ").strip().lower()
        if answer in ('y', 'yes'):
            subprocess.run(['sudo', 'shutdown', 'now'])

    elif query.startswith('remember '):
        note = query[len('remember '):].strip()
        if note:
            with open(notes_path, "a", encoding="utf-8") as notes_file:
                notes_file.write(note + "\n")

    elif query == 'recall':
        subprocess.run(['cat', 'notes'])
        input("press enter, NOW!")
    
    elif query.startswith('search url '):
        search_url = query[len('search url '):].strip()
        if search_url:
            subprocess.Popen(["firefox", search_url])
        else:
            print("enter a URL after 'search url'")

    elif query.startswith('search '):
        search_query = query[len('search '):].strip()
        if search_query:
            url = settings["settings"]["browserurl"] + urlencode({"q": search_query})
            subprocess.Popen(["firefox", url])
        else:
            print("enter a search term after 'search'")

    if clear_after_command:
        clear()


while True:
    a()
