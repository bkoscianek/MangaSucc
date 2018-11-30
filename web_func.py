import os
import re

import bs4
import requests as req

import base_func

base_url = "http://mangakakalot.com/search/"
reg1 = r'.*/chapter/.*'


def search_for_manga(name: str):
	manga_search = name.replace(" ", "_")
	search_url = base_url + manga_search

	r = req.get(search_url)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')

	mangas = {}
	for potential_div in soup.find_all('div', class_="daily-update"):
		i = 1
		for link in potential_div.find_all('a'):
			if not re.match(reg1, link.get('href')):
				mangas[link.string] = link.get('href')
				i += 1

	return mangas


def get_chapters(manga_url: str):
	r = req.get(manga_url)
	soup = bs4.BeautifulSoup(r.content, 'html.parser')
	soup = soup.find('div', class_="chapter-list")

	chapters = {}
	for link in soup.find_all('a'):
		chapters[link.string] = link.get('href')

	return chapters


def get_list_of_chapters(chapters: dict, first: str, last: str):
	chapters_choice = "<" + first + "-" + last + ">"
	list_of_choices = list(base_func.get_chapter_range(chapters_choice, chapters))

	final_list = {}

	for choice in list_of_choices:
		final_list[choice] = chapters[choice]

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
