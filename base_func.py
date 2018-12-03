import getpass
import os
import platform
import re


def get_to_dnl_folder():
    ops = platform.system()
    base_folder = ""

    if ops == 'Linux':
        base_folder = "/home/" + getpass.getuser() + "/Downloads"
    elif ops == 'Windows':
        base_folder = "C:/Users/" + getpass.getuser() + "/Downloads"

    os.chdir(base_folder)

    try:
        os.makedirs("MangaSucc Download")
        os.chdir("./MangaSucc Download")
    except OSError:
        os.chdir("./MangaSucc Download")


def get_to_manga_folder(manga_name: str):
    get_to_dnl_folder()
    manga_folder_name = make_valid_name(manga_name)

    print(manga_folder_name)

    try:
        os.chdir("./" + manga_folder_name)
    except OSError:
        os.makedirs("./" + manga_folder_name)
        os.chdir("./" + manga_folder_name)


def get_to_chapter_folder(chapter_name: str):
    chapter_folder_name = make_valid_name(chapter_name)

    try:
        os.chdir("./" + chapter_folder_name)
    except OSError:
        os.makedirs("./" + chapter_folder_name)
        os.chdir("./" + chapter_folder_name)


def make_valid_name(target: str):
    red = ['/', '\\', '?', '*', ':', '|', '<', '>']
    replace = ""

    for i in range(0, len(target)):
        if target[i] in red:
            replace = replace + " "
        else:
            replace = replace + target[i]

    return replace


def get_chapter_range(dnl_chapters: str, chapter_list: dict):
    re1 = r'\<.*-'
    re2 = r'-.*>'

    first_chapter = re.search(re1, dnl_chapters)
    first_chapter = first_chapter.group(0)
    first_chapter = first_chapter[1:len(first_chapter) - 1]

    last_chapter = re.search(re2, dnl_chapters)
    last_chapter = last_chapter.group(0)
    last_chapter = last_chapter[1:len(last_chapter) - 1]

    isok = 0
    out_list = list()
    for chapter in chapter_list:
        if chapter == last_chapter:
            isok = 1
        if isok == 1:
            out_list.append(chapter)
        if chapter == first_chapter:
            break

    return out_list
