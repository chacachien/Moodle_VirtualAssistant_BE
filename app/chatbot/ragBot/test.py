from sentence_transformers import SentenceTransformer
from pyvi.ViTokenizer import tokenize

sentences = ["Hà Nội là thủ đô của Việt Nam", "Đà Nẵng là thành phố du lịch"]
tokenizer_sent = [tokenize(sent) for sent in sentences]
print(tokenizer_sent)
model = SentenceTransformer('dangvantuan/vietnamese-embedding')
embeddings = model.encode(tokenizer_sent)
print(embeddings)
