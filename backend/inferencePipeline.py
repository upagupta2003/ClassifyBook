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

load_dotenv()

class InferencePipeline:
    def __init__(self, model_name: str, path_to_model: str, text: str):
        self.model_name = model_name
        self.path_to_model = path_to_model
        self.text = text
    
    def HuggingFaceLogin(self):
        #this function will login to the huggingface using api key which is stored in  a env API_KEY file
        login(token=os.environ.get('API_KEY'))

    def load_model(self, model_name: str, path_to_model: str):
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
        self.predictions = self.model(**tokenized_text)
        return 
    
    def run(self):
        self.load_model(self.model_name, self.path_to_model)
        self.tokenize_the_text(self.text)
        return self.inference_from_the_model(self.text)
        


#Testing the above code using FastText Model which is used for Text Classification

if __name__ == "__main__":
    inference = InferencePipeline("openai-community/gpt2-xl", "openai-community/gpt2-xl", "Hello")
    print(inference.run())
        

