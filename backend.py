from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
app = Flask(__name__)
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Replace with your chosen model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message", "").lower()

    # Predefined facts about penguins
    if "penguin" in message:
        response = ("They live almost exclusively in the Southern Hemisphere: "
                    "only one species, the Galápagos penguin, is found north of the Equator. "
                    "Highly adapted for life in the ocean water, penguins have countershaded dark and white plumage and flippers for swimming."
                    " Most penguins feed on krill, fish, squid and other forms of sea life which they catch with their bills "
                    "and swallow whole while swimming. A penguin has a spiny tongue and powerful jaws to grip slippery prey.")
    else:
        # Generate response from the LLM
        inputs = tokenizer(message, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=50)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
