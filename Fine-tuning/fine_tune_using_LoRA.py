## LoRA can only be used on models where you have access to the full architecture (like Hugging Face models), and not through OpenAI's API.

## 1- Install dependencies
## pip install transformers datasets peft accelerate

##2- _________ prepare the dataset_______________
from datasets import load_dataset

# Load the IMDB dataset
dataset = load_dataset('imdb')
train_data = dataset['train']
test_data = dataset['test']

# Example data structure
print(train_data[0])

## 3- Load pretrained model and tokenizer.

from transformers import AutoTokenizer, AutoModelForCausalLM

# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


## 4- _____________ set up LoRA for Fine-Tunning_____________________
# Here I used peft library to fine-tune the model with LoRan, focusing on the specific layers to adapt using low-rank updates

from peft import LoraConfig, get_peft_model

# Define LoRa configuration
lora_config = LoraConfig(
    r=8,  # Rank (number of LoRa parameters), determine how much information LoRa adds
    lora_alpha=16,  # Scaling factor for LoRa parameters
    lora_dropout=0.1,  # Dropout for LoRa layers
    target_modules=['c_attn'],  # The GPT-2 attention layers to adapt. the layer in the model we want to modify
    bias='none'  # Bias handling (can be "none", "all", or "lora_only")
)

## Add LoRA modules to the pre-trained model
model = get_peft_model(model, lora_config)

# Print model with LoRA layers
print(model)

## 5- ___________Tokenize the Dataset________________
## We need to tokenize the dataset and prepare it for training by converting the text data into input IDs

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True, max_length=512)

## Tokenize dataset
tokenized_train = train_data.map(tokenize_function, batched=True)
tokenized_test = test_data.map(tokenize_function, batched=True)

## 6- _________Fine-Tune the model______________________
## Now we can fine-tune the model using the LoRA-adapted layers. use Hugging Face’s Trainer class to handle training

from transformers import Trainer, TrainingArguments

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_total_limit=1
)

## Create Trainer instance, Trainer is a high-level API provided by Hugging Face to handle model training.
## Only the LoRA layers are fine-tuned, the rest of the model remains frozen. save memory and computer power

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test
)

# Train the model
trainer.train()

## 7- _________________Evaluate the model______________________
eval_results = trainer.evaluate()
print(f"Evaluation Results: {eval_results}")

## ## 8-_______________ save the fine tuned model________________
trainer.save_model("./lora_finetuned_gpt2")

# Inform the user
print("Fine-tuning with LoRA is complete! The model has been saved.")
