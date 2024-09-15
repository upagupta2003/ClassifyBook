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
from transformers import AutoModel, AutoTokenizer, AutoConfig
from huggingface_hub import login
import os
#from dotenv import load_dotenv

class InferencePipeline:
    def __init__(self, model_name: str, path_to_model: str):
        self.model_name = model_name
        self.path_to_model = path_to_model
    
    def HuggingFaceLogin(self):
        #this function will login to the huggingface using api key which is stored in  a env API_KEY file
        login(token=os.getenv("API_KEY"))

    def load_model(self, model_name: str, path_to_model: str):
        self.HuggingFaceLogin()
        self.model = AutoModel.from_pretrained(model_name)
        #self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        #self.config = AutoConfig.from_pretrained(model_name)

    def inference_from_the_model(self, text: str):
        self.text = text
        self.predictions = self.model.generate(self.text)
        return self.predictions
    
    def run(self):
        self.load_model(self.model_name, self.path_to_model)
        self.inference_from_the_model(self.text)
        return self.predictions


#Testing the above code using FastText Model which is used for Text Classification

if __name__ == "__main__":
    inference = InferencePipeline("microsoft/Multilingual-MiniLM-L12-H384", "microsoft/Multilingual-MiniLM-L12-H384")
    inference.run()
        

