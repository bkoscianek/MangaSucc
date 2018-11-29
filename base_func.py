import getpass
import os
import re



def get_to_dnl_folder():
	base_folder = "C:/Users/" + getpass.getuser() + "/Downloads"
	os.chdir(base_folder)

	try:
		os.makedirs("MangaGrab Download")
		os.chdir("./MangaGrab Download")
	except OSError:
		os.chdir("./MangaGrab Download")


def get_to_manga_folder(manga_name: str):
	get_to_dnl_folder()
	try:
		os.chdir("./" + manga_name)
	except OSError:
		os.makedirs("./" + manga_name)
		os.chdir("./" + manga_name)


def get_to_chapter_folder(chapter_name: str):
	folder_name = make_valid_name(" ", chapter_name)
	try:
		os.chdir("./" + folder_name)
	except OSError:
		os.makedirs("./" + folder_name)
		os.chdir("./" + folder_name)


def make_valid_name(target: str):
	red = ['/', '\\', '?', '*', ':', '|', '<', '>']
	for rep in red:
		target.replace(rep, " ")

	return target


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
			isok = 0
			break

	return out_list
