import csv
import keras
import numpy as np
import matplotlib.pyplot as plt
from SerbianStemmer import stem_sentence

def clean_word(word):
	word = word.lower()
	word = word.replace("š", "sx")
	word = word.replace("č", "cx")
	word = word.replace("ć", "cy")
	word = word.replace("đ", "dx")
	word = word.replace("ž", "zx")
	return "".join(filter(str.isalnum, word))

def read_dictionary(word_count):
	word_list = []
	
	with open("word_dictionary.txt", "r", encoding="utf-8") as file:
		for	index, line in enumerate(file):
			word, count = line.split()			
			word_list.append(word)
			if index + 1>= word_count:
				break
	word_dictionary = {}
	for index, word in enumerate(word_list):
		word_dictionary[word] = index
	return word_dictionary


def one_hot(story, word_dictionary):
	encoded_story = np.zeros(len(word_dictionary), dtype=np.int8)
	word_list = list(map(clean_word, story.split()))
	word_list = stem_sentence(word_list)
	
	for word in word_list:
		if word not in word_dictionary:
			continue
		index = word_dictionary[word]
		encoded_story[index] += 1
	return encoded_story
	
def read_stories():
	data = []
	labels = []
	with open('ispovesti.csv', encoding='utf-8') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			data.append(row[0])
			likes = float(row[1])
			dislikes = float(row[2])
			if likes > dislikes:
				labels.append(1)
			else:
				labels.append(0)
			
	return data, labels


word_dictionary = read_dictionary(5000)
data, labels = read_stories()
encoded_data = np.array([one_hot(x, word_dictionary) for x in data])
labels = np.array(labels)

split = int(encoded_data.shape[0] * 0.85)

train_data = encoded_data[0:split, :]
train_labels = labels[0:split]

test_data = encoded_data[split:, :]
test_labels = labels[split:]



input_size = len(word_dictionary)
model = keras.Sequential()
model.add(keras.layers.InputLayer(input_shape=(input_size,)))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))
model.compile(optimizer="adam", loss="binary_crossentropy",  metrics=['accuracy'])

model.summary()
history = model.fit(train_data, train_labels, validation_split=0.1, batch_size=128, epochs=6)

score = model.evaluate(test_data, test_labels)

#print("Test accuracy:", score)
#print(history.history.keys())


komentari = [
"Imam najljepsu mater na svetu.",
"Prevario sam ženu.",
"Prevarila sam dečka.",
"Joj kako ne mogu kada mi u kafanu dođe dijaspora pa se nešta pravi kao da je neko i nešta."
]


test = np.array([one_hot(x, word_dictionary) for x in komentari])

predictions = model.predict(test)
print(predictions)

for prediction in predictions:
	if prediction[0]>= 0.5:
		print("Ispovijest ima pozitivan sadrzaj")
	else:
		print("Ispovijest ima negativan sadrzaj")








