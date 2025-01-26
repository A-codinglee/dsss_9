from flask import Flask, request, jsonify
from transformers import pipeline
import torch

app = Flask(__name__)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Initialize the pipeline for text generation
print("Loading TinyLlama model and tokenizer. Please wait...")
pipe = pipeline("text-generation", model=MODEL_NAME, tokenizer=MODEL_NAME, torch_dtype=torch.bfloat16, device_map="auto")
print("Model and tokenizer loaded successfully.")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    # Split the input into individual questions by new lines
    questions = [q.strip() for q in message.split("\n") if q.strip()]

    try:
        for question in questions:
            # Format the message as per the chat template
            messages = [
                {"role": "system", "content": "You are a friendly chatbot."},
                {"role": "user", "content": question}
            ]
            # Apply chat template to the input
            prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
            response = outputs[0]["generated_text"]
            split_response = response.split("<|assistant|>")[1].strip() if "<|assistant|>" in response else response.strip()

        return jsonify({"response": split_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
