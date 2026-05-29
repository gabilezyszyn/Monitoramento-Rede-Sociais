#import warnings
#warnings.filterwarnings("ignore")

from sentence_transformers import SentenceTransformer

print("Carregando o Multilingual E5")
model = SentenceTransformer('intfloat/multilingual-e5-small') #small para nao consumir tanta RAM   

post_exemplo = "query: Este post é uma tentativa de golpe com criptomoedas"

embedding = model.encode([post_exemplo]) #texto em vetor

print(f"Vetor gerado! Tamanho do vetor: {len(embedding[0])}")