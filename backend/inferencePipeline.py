# Inference Class:
# 	ModelName:
# 	PathToModel: (S3 Path or Local Path)

# 	func loadModel (ModelName, PathToModel):
# 		#this funtion will load the model from huggingface and check whether the model is loaded or not

# 	func InferenceFromtheModel:
# 		predict the genre of the book

# 	func Run:
# 		to run the above funtions and return the output

# TestRun Code: #to test the above class


from pydantic import BaseModel
from transformers import AutoModelForCausalLM, GPT2Tokenizer, GPT2Model
from huggingface_hub import login
import os
from dotenv import load_dotenv
import torch

class InferencePipeline:
    def __init__(self, model_name: str, path_to_model: str, text: str):
        self.model_name = model_name
        self.path_to_model = path_to_model
        self.load_env()
    
    def load_env(self):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")
        self.text = text

    def HuggingFaceLogin(self):
        # Use the API key loaded from .env
        login(token=self.api_key)

    def load_model(self):
        self.HuggingFaceLogin()
        #self.model = AutoModel.from_pretrained(model_name)
        self.model = GPT2Model.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name, clean_up_tokenization_spaces=True)
        #self.config = AutoConfig.from_pretrained(model_name)

    #function to tokenize the input text
    def tokenize_the_text(self, text: str):
        self.tokenized_text = self.tokenizer(text, return_tensors='pt')
        return self.tokenized_text
   
    def inference_from_the_model(self, text: str):
        tokenized_text = self.tokenize_the_text(text)
        with torch.no_grad():
            outputs = self.model(**tokenized_text)
        
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        return predicted_class
    
    def run(self):
        self.load_model(self.model_name, self.path_to_model)
        return self.inference_from_the_model(self.text)
        


#Testing the above code using FastText Model which is used for Text Classification

if __name__ == "__main__":
    inference = InferencePipeline("microsoft/Multilingual-MiniLM-L12-H384", "microsoft/Multilingual-MiniLM-L12-H384")
    inference.run()
        

