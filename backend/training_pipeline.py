import os
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch
from dotenv import load_dotenv
from huggingface_hub import login


load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables")

login(token=api_key)

# Load the dataset
dataset = load_dataset("AlekseyKorshuk/romance-books")

# Load tokenizer and model
model_name = "microsoft/MiniLM-L12-H384-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Prepare labels (binary classification: romance or not)
num_labels = 2
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

# Tokenize and encode labels function
def tokenize_and_encode_labels(examples):
    tokenized = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
    tokenized["labels"] = [1] * len(examples["text"])  # All examples are romance books
    return tokenized

# Tokenize and encode the dataset
encoded_dataset = dataset["train"].map(tokenize_and_encode_labels, batched=True)

# Prepare dataset for training
encoded_dataset = encoded_dataset.remove_columns(["text", "url"])
encoded_dataset.set_format("torch")

# Split the dataset
train_testvalid = encoded_dataset.train_test_split(test_size=0.2, seed=42)
train_dataset = train_testvalid['train']
eval_dataset = train_testvalid['test']

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    evaluation_strategy="epoch",
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("./genre_classifier")
tokenizer.save_pretrained("./genre_classifier")

# Save the label encoder
import joblib
joblib.dump(["Not Romance", "Romance"], './genre_classifier/label_encoder.joblib')