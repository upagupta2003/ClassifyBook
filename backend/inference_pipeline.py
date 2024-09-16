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


from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from pydantic import BaseModel
from huggingface_hub import login
import os
from dotenv import load_dotenv

class InferencePipeline:
    def __init__(self, model_name: str, path_to_model: str):
        self.model_name = model_name
        self.path_to_model = path_to_model
        self.load_env()
        self.load_model()
    
    def load_env(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")

    def HuggingFaceLogin(self):
        login(token=self.api_key)

    def load_model(self):
        self.HuggingFaceLogin()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
        # Define genre labels (update these based on your specific classification task)
        self.genre_labels = ["Fiction", "Non-fiction", "Science Fiction", "Mystery", "Romance", "Biography", "Fantasy", "Thriller", "Historical Fiction", "Horror"]

    def inference_from_the_model(self, text: str, threshold: float = 0.3, top_n: int = 3):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        probabilities = torch.sigmoid(logits)  # Convert logits to probabilities
        
        predicted_genres = []
        for i, prob in enumerate(probabilities[0]):
            if prob > threshold:
                predicted_genres.append({
                    "genre": self.genre_labels[i],
                    "probability": float(prob)
                })
        
        # Sort genres by probability in descending order
        predicted_genres.sort(key=lambda x: x["probability"], reverse=True)
        
        return predicted_genres[:top_n]
    
    def run(self, text: str, threshold: float = 0.3):
        return self.inference_from_the_model(text, threshold)

# For testing
if __name__ == "__main__":
    inference = InferencePipeline("microsoft/Multilingual-MiniLM-L12-H384", "microsoft/Multilingual-MiniLM-L12-H384")
    result = inference.run("This is a sample text about a detective solving a murder mystery in a small town with supernatural elements.")
    print("Predicted genres:")
    for genre in result:
        print(f"{genre['genre']}: {genre['probability']:.2f}")

