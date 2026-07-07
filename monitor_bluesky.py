import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from analisador import resumir_campanha_coordenada
import warnings

warnings.filterwarnings("ignore")

# carregando modelo e banco de dados vetorial
model = SentenceTransformer('intfloat/multilingual-e5-small')
dimensao = 384
index = faiss.IndexFlatIP(dimensao) 

balde_posts_suspeitos = []

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
    
    #retem posts acima de 90% e guarda para analisar depois
    if D[0][0] > 0.90: 
        mensagem_alerta = f"ALERTA: Similaridade de {porcentagem:.2f}% detectada!"
        
        #guarda no balde para chamar o llama 3.2 depois
        balde_posts_suspeitos.append(texto_do_post)
        
        #add o vetor ao banco para ele continuar a cruzar com os próximos
        index.add(novo_vetor) 
        
        return f"{mensagem_alerta} -> Post retido para análise de lote posterior."
    else:
        index.add(novo_vetor)
        return f"Post original registrado no banco. (Maior similaridade no banco: {porcentagem:.2f}%)"

#funcao coletor chama para rodar o llama 3.2
def gerar_relatorio_final_campanha():
    if len(balde_posts_suspeitos) > 0:
        print(f"\nAnalisando lote de {len(balde_posts_suspeitos)} posts com o Llama 3.2...")
        relatorio = resumir_campanha_coordenada(balde_posts_suspeitos)
        return relatorio
    return "Nenhuma campanha coordenada (similaridade >90%) foi detectada no período."


if __name__ == "__main__":
    exemplo_fluxo = [
        "Compre bitcoin agora e fique rico!",
        "O clima em Florianópolis está ótimo hoje",
        "compre BITCOIN agora e FIQUE RICO!!",
    ]
    
    for post in exemplo_fluxo:
        print(f"\nRecebendo post: {post}")
        print(verificar_e_guardar(post))
        
    print("\n--- Testando Relatório em Lote ---")
    print(gerar_relatorio_final_campanha())