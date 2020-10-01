from datetime import timedelta, date
import csv

import requests
from bs4 import BeautifulSoup

content = []
dislikes = []
likes = []
comment_count = []

def get_page(url, page_number):
	page = requests.get(url + str(page_number)).content
	soup = BeautifulSoup(page, 'html.parser')

	results = soup.findAll("div",{"class": "confession" })
	number_of_confessions = 0
	for confession in results:
		page_content = confession.find("div",{"class": "confession-text"})
		values = confession.findAll("div", {"class": "confession-value"})
		comment = confession.find("a", {"class": "confession-value"})
		
		
		content.append(page_content.text)
		likes.append(values[0].text)
		dislikes.append(values[1].text)
		comment_count.append(comment.text)
		number_of_confessions += 1
	
	return number_of_confessions



def main():
	url_base = "http://ispovesti.com/sort/calendar"
	max_days = 730

	today = date.today()
	one_day = timedelta(days=1)

	for number_of_days in range(0, max_days):
		
		query_date = today - number_of_days*one_day
		
		url = "%s/%d/%d/%d/" % (url_base, query_date.day, query_date.month, query_date.year)
		
		page_number = 1
		number_of_confessions = 10
		
		while number_of_confessions == 10:
			number_of_confessions = get_page(url, page_number)
			page_number += 1
		
	with open("ispovesti.csv", "w", newline='\n', encoding='utf-8') as  file:
		csv_writer = csv.writer(file)
		csv_writer.writerows(zip(content, likes, dislikes, comment_count))

if __name__ == "__main__":
	main()

	