import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from SerbianStemmer import stem_sentence
import sys

def clean_word(word):
	word = word.lower()
	word = word.replace("š", "sx")
	word = word.replace("č", "cx")
	word = word.replace("ć", "cy")
	word = word.replace("đ", "dx")
	word = word.replace("ž", "zx")
	return "".join(filter(str.isalnum, word))
	
word_count = {}

with open('ispovesti.csv', encoding='utf-8') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		words = list(map(clean_word, row[0].split()))
		words = stem_sentence(words)
		for word in words:
			if word not in word_count:
				word_count[word] = 0
			
			word_count[word] += 1


wc = WordCloud().generate_from_frequencies(word_count)
plt.figure()
plt.imshow(wc)
plt.show()
plt.imsave("word_cloud.png", wc)
sys.exit()
list_of_words = reversed(sorted(list(word_count.items()), key=lambda x: x[1]))

with open("word_dictionary.txt", "w", encoding="utf-8") as file:
	for word in list_of_words:
		if word[0] == "":
			continue
		file.writelines("%s %d\n" % (word[0],word[1]))

		

		
		