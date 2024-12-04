# Mailstral
Development of an email reply suggestion app, designed to be trained on personnal emails. It is using Mistral7B as it is opensource and can me used locally (and it's French !). 

*Steps :*
1. Scrape personnal emails with gmail API
2. Create a dataset from the emails
3. Download [Mistral7B from HuggingFace](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) onto a Colab Notebook
4. Fine-tune the model using [Mistral's opensource fine-tune tool](https://github.com/mistralai/mistral-finetune/)
5. Implement the app

# 1. Email Scraper
I started by writing (well... some General Purpose Transformer wrote) a quick python script to scrape personnal emails through Gmail's API. The API can be activated through the Google Cloud Console. In order to skip the verification process, the state of the app is set to "test" and all email adresses I want to scrape from are added to the "test users" list.
The scraper was already working at that point, but data wasn't clean enough to use as a dataset. The scraper had a hard time correctly handling the threads to separate received emails (input) and reply emails (labels). I modified the code to clearly separate inputs and labels.
