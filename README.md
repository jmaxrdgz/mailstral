# mailstral
Development of an email reply suggestion app, designed to be trained on personnal emails. It is using Mistral7B as it is opensource and can me used locally (and it's French !). 

Workflow :
1. Download [Mistral7B from HuggingFace](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) onto a Colab Notebook
2. Scrap personnal emails with gmail API
3. Create a dataset from the emails
4. Fine-tune the model using [Mistral's opensource fine-tune tool](https://github.com/mistralai/mistral-finetune/)
5. Implement the app
