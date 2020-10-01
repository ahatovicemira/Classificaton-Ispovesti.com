# Classificaton-Ispovesti.com


*Do you want to know if your post on Ispovest.com would have more likes or dislikes? Try this project.*

The downloaded data is then cleaned and prepared. We clean the data by removing all invalid characters, fixing extra whitespace, and diving the sentences into individual words.  Since the posts are mainly in Bosnian/Serbian/Croatian, we use a Serbian based stemmer. After the data is cleaned, one hot encoding is used to format our data. The formated data can then be passed into the neural network as input.
This project was made for my University course. 

Dependencies:
- numpy
- SerbianStemmer (repository [link](https://github.com/nikolamilosevic86/SerbianStemmer.git)
- matplotlib
- keras


