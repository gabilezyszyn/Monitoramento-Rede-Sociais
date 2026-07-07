import ollama

def analisar_post(texto):
    modelo_ia = 'llama3.2'
    prompt = f"""
    Você é um especialista em segurança digital.
    Analise o post abaixo e classifique-o como 'HUMANO' ou 'BOT'.
    Considere padrões de repetição, excesso de hashtags e links suspeitos.

    Post: "{texto}"

    Responda apenas no formato:
    CLASSIFICAÇÃO: [HUMANO/BOT]
    JUSTIFICATIVA: [Breve explicação]
    """

    try:
        response = ollama.chat(model=modelo_ia, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    
    except Exception as e: #caso Llama caiu ou a VRAM acabe
        return f"ERRO NA INFERÊNCIA: Ocorreu uma falha ao processar o post. Detalhe: {e}"
    
def resumir_campanha_coordenada(lista_de_posts):
    modelo_ia = 'llama3.2'
    
    #formatacao da lista de posts em texto para o llama 3.2 ler
    posts_formatados = "\n".join([f"- {p}" for p in lista_de_posts])
    
    prompt = f"""
    Você é um analista sênior de segurança digital no laboratório LaBDES.
    O nosso sistema FAISS agrupou os seguintes posts devido à altíssima similaridade semântica entre eles (>90%).
    Analise o lote de posts abaixo e identifique o tema central, a intenção da campanha e faça um resumo consolidado em até 3 linhas.

    Posts detectados na campanha:
    {posts_formatados}

    Resposta estruturada em português:
    TEMA CENTRAL DA CAMPANHA:
    RESUMO ANALÍTICO:
    """

    try:
        response = ollama.chat(model=modelo_ia, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    
    except Exception as e:
        return f"ERRO NO LLAMA (Resumo de Lote): {e}"
    
if __name__ == "__main__":
    post_teste = "GANHE DINHEIRO AGORA!!! CLIQUE NO LINK E MUDE DE VIDA #PIX #DINHEIRO"
    resultado = analisar_post(post_teste)
    print(resultado)
