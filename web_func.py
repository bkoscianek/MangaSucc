import requests as req
import bs4
import re
import base_func
import os

base_url = "http://mangakakalot.com/search/"
reg1 = r'.*/chapter/.*'


def search_for_manga():
	manga_search = str(input("Enter manga name: "))
	manga_search = manga_search.replace(" ", "_")
	search_url = base_url + manga_search

	r = req.get(search_url)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')

	links = {}
	for potential_div in soup.find_all('div', class_="daily-update"):
		i = 1
		for link in potential_div.find_all('a'):
			if not re.match(reg1, link.get('href')):
				links[link.string] = link.get('href')
				print("{}. {}".format(i, link.string))
				i += 1

	links_keys = list(links.keys())
	choice = int(input("Please select: "))
	choice_url = links[links_keys[choice - 1]]

	manga_folder_name = base_func.make_valid_name(links_keys[choice - 1])
	base_func.get_to_manga_folder(manga_folder_name)

	return choice_url


def select_chapters(manga_url: str):
	r = req.get(manga_url)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')
	soup = soup.find('div', class_="chapter-list")

	chapter_list = {}
	for link in soup.find_all('a'):
		chapter_list[link.string] = link.get('href')

	chapter_names = list(chapter_list.keys())
	last_chapter = chapter_names[0]
	first_chapter = chapter_names[len(chapter_names) - 1]
	print("Available chapters: {} - {}".format(first_chapter, last_chapter))

	print(
		"You can select a single chapter by writing its name or multiple chapters by writing <name1-name2>. \nWrite 'all' to download full manga!")
	chapters_choice = str(input("Please select chapter(s): "))

	if chapters_choice == "all":
		list_of_choices = list(chapter_list.keys())
	else:
		list_of_choices = list(base_func.get_chapter_range(chapters_choice, chapter_list))

	final_list = {}

	for choice in list_of_choices:
		final_list[choice] = chapter_list[choice]

	return final_list


def download_chapters(chapter_urls: dict):
	for chapter in chapter_urls:
		download_chapter(chapter, chapter_urls[chapter])


def download_chapter(chapter_name: str, chapter_url: str):
	base_func.get_to_chapter_folder(chapter_name)

	r = req.get(chapter_url)
	chapter_soup = bs4.BeautifulSoup(r.content, 'html.parser')
	chapter_soup = chapter_soup.find('div', class_='vung-doc')

	i = 1
	for img in chapter_soup.find_all('img'):
		r = req.get(img.get('src'), stream=True)
		img_name = "{}.jpg".format(i)
		if r.status_code == 200:
			with open(img_name, "wb") as f:
				f.write(r.content)
		i += 1

	os.chdir("..")
