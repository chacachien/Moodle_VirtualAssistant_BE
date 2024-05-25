# from sentence_transformers import SentenceTransformer
# from pyvi.ViTokenizer import tokenize

# sentences = ["Hà Nội là thủ đô của Việt Nam", "Đà Nẵng là thành phố du lịch"]
# tokenizer_sent = [tokenize(sent) for sent in sentences]
# print(tokenizer_sent)
# model = SentenceTransformer('dangvantuan/vietnamese-embedding')
# embeddings = model.encode(tokenizer_sent)
# print(embeddings)
import json

# Your JSON list (replace with your actual data)
json_list = [
    {'name': 'Computer vision', 'summary': 'Học về máy tính nhìn nhận...'},
    {'name': 'Test Sort Test', 'summary': 'Test course 1...\nLorem ipsum...'}
]

# Convert the list to a JSON string
json_string = json.dumps(json_list)

# Print the JSON string
print(type(json_string))
