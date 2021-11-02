## NLP_Project

### Project 18: Climate Change News Analysis. Discovering Arguments  

1.	Identify a hot topic in climate change of your choice which has been extensively commented in the media. You are free to phrase the topic as a set of keywords or single phrase or any combination of the above (e.g., pollution, emissions, water contamination…) and motivate your answer based on your observations and heuristic (literature, personal opinion,..,)  (no need to do any programming task here)

2.	Use news sources that offer APIs (https://en.wikipedia.org/wiki/List_of_news_media_APIs) for conducting automatic search (e.g., guardian news paper, BBC news, etc.) and input your suggested topic as a search phrase. Design a program that retrieves the first 20 search outcomes (see examples in NLTK online book for crawling html documents, and also examples in https://pypi.org/project/google-search-results-serpwow/#simple-example for creating and using Google API for the purpose of retrieving query snippets). You can also manually check the retrieved search to include only those documents (search results) which contain high proportion of user’s generated content in terms of comments on the news or topic raised by another user. For each outputted document, generate a separate document that includes only comments related to that document. 

3.	We would like to test the extent of overlapping between the original document and the user-generated document. For this purpose, for each search output, use standard preprocessing including stopword removal and tokenization strategy and then draw the histogram of the most frequent words (outside stopword list) for both the original document and its corresponding user-comments. Calculate Jacquard index (ratio of number of common frequent words (among the top 20 most frequent terms) over the total number of distinct words in the top 20 frequent words) for each search result.  

4.	Similarly to Jacquard coefficient, run LDA model for identifying the topics of original search document (without user comment) and its associated user’s generated document. Use LDA with three topics and 5 words per topic. Create the list L1 of words generated by LDA for original document (without user’s comments) and the list L2 of words generated by LDA for the user’s generated document. Calculate the associated Jacquard index between L1 and L2. 

5.	Repeat reasoning 4) for sentiment analysis. For this purpose, use sentistrength, for calculating the vector positive and negative sentiment for both original and user’s generated document (each vector is two component vector corresponding to positive and negative sentiment value). Calculate Pearson correlation to calculate the statistical correlation between sentiment associated to original document (without comment) and that of user’s generated comment. Repeat this process for each search result.  

6.	We would like to evaluate the extent to which the users agree and/or disagree with policy-maker or public organization. For this purpose, identify the list of negative emotion wording using a corpus of your choice (e.g., Empath ..), then use parser tree to identify, in each user’s generated document, the entity the negative sentiment word is associated with. Generate the histogram of these entities in overall. 

7.	We now would like to investigate the behavior of users who make comments on the original document. For this purpose, elaborate a list of your own for agreement act (e.g., agree, OK, sure, right…) and another list of disagreement, and draw a histogram of agreement act and disagreement (just by counting number of agreement act related words and number of disagreement act related words). 

8.	Design and implement a simple GUI interface that would allow you to demonstrate and exemplify your reasoning.


### How to run the project

To run the project, you must clone the git repository, install all the libraries needed (specified in Appendix in the report) and be sure that Java is installed. Then, you can open "gui.py" in an ide and execute it.
