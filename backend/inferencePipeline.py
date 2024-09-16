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
from dotenv import load_dotenv
import torch

class InferencePipeline:
    def __init__(self, model_name: str, path_to_model: str):
        self.model_name = model_name
        self.path_to_model = path_to_model
        self.load_env()
    
    def load_env(self):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")

    def HuggingFaceLogin(self):
        # Use the API key loaded from .env
        login(token=self.api_key)

    def load_model(self):
        self.HuggingFaceLogin()
        self.model = AutoModel.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.config = AutoConfig.from_pretrained(self.model_name)

    def inference_from_the_model(self, text: str):
        # Tokenize the input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        
        # Get the model's output
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Process the output (this will depend on your specific model and task)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        
        return predicted_class
    
    def run(self, text: str):
        self.load_model()
        return self.inference_from_the_model(text)


#Testing the above code using FastText Model which is used for Text Classification

if __name__ == "__main__":
    inference = InferencePipeline("microsoft/Multilingual-MiniLM-L12-H384", "microsoft/Multilingual-MiniLM-L12-H384")
    result = inference.run("Sample text for inference")
    print(result)

