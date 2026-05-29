import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from analisador import resumir_post_suspeito
import warnings

warnings.filterwarnings("ignore")

#carregando modelo e banco de dados vetorial
model = SentenceTransformer('intfloat/multilingual-e5-small')
dimensao = 384
index = faiss.IndexFlatIP(dimensao) 

#embedding
def verificar_e_guardar(texto_do_post):
    vetor = model.encode([f"query: {texto_do_post}"])
    novo_vetor = np.array(vetor).astype('float32')
    
    #normalizacao para o cosseno
    faiss.normalize_L2(novo_vetor)
    
    #se o banco vazio, adiciona
    if index.ntotal == 0:
        index.add(novo_vetor)
        return "Primeiro post registrado!"

    #busca post similar
    D, I = index.search(novo_vetor, k=1) 
    
    porcentagem = D[0][0] * 100
    
    #if D[0][0] > 0.90: 
        #return f"ALERTA: Similaridade de {D[0][0]*100:.2f}% detectada!"
    #else:
        #index.add(novo_vetor)
        #return f"Post original registrado no banco. (Maior similaridade no banco: {porcentagem:.2f}%)"
    
    if D[0][0] > 0.90: 
        mensagem_alerta = f"ALERTA: Similaridade de {porcentagem:.2f}% detectada!"
        print(mensagem_alerta)
        
        #llama 3.2 resume posts com similaridade >0.90
        print("Acionando Llama 3.2 para gerar resumo semantico...")
        resumo_ia = resumir_post_suspeito(texto_do_post)
        
        return f"{mensagem_alerta}\n   ↳ [Resumo da IA]: {resumo_ia}"
    else:
        index.add(novo_vetor)
        return f"Post original registrado no banco. (Maior similaridade no banco: {porcentagem:.2f}%)"

if __name__ == "__main__":
    exemplo_fluxo = [
        "Compre bitcoin agora e fique rico!",
        "O clima em Florianópolis está ótimo hoje",
        "compre BITCOIN agora e FIQUE RICO!!",
    ]
    
    for post in exemplo_fluxo:
        print(f"\nRecebendo post: {post}")
        print(verificar_e_guardar(post))