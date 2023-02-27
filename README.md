# medical_nlp

This project was my undergraduate research project at NC State. This project was the initial attempt to an end-to-end 
medical search tool that, similar to Google Search, gives the user a list of suggested string of words to complete
their inquiry. However, I was only to create a simple implementation of it, where the model can only give the user 2 rounds of 
single-word suggestion.

Although this was not a completed project, the main contributions of my project are follows:
  - Used BeatifulSoup to scrape contents of WebMD
  - Created classes that can be used to create profiles of diseases, containing all info and the link to it
  - Used a pre-trained Spacy model to vectorize words and find the closest words between two given words
  - Implemented a simple interfacing code, using Tinker, to ask for two initial words and give user an initial list of
  suggested words
  
For more details and step-by-step implementation, see "User_Manual.docx".
