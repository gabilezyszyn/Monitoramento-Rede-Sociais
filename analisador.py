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
    
def resumir_post_suspeito(texto):
    modelo_ia = 'llama3.2'
    prompt = f"""
    Você é um assistente de IA especialista em análise de redes sociais no laboratório LaBDES.
    O sistema de monitoramento detectou que este post possui uma similaridade vetorial muito alta com posts anteriores.
    Escreva um resumo analítico bem curto (no máximo 2 linhas) explicando qual é o assunto ou a principal intenção desse texto.

    Post Suspeito: "{texto}"

    Resposta resumida (direta e em português):
    """

    try:
        response = ollama.chat(model=modelo_ia, messages=[
            {'role': 'user', 'content': prompt},
        ])
        return response['message']['content']
    
    except Exception as e:
        return f"ERRO NO LLAMA (Resumo): {e}"
    
if __name__ == "__main__":
    post_teste = "GANHE DINHEIRO AGORA!!! CLIQUE NO LINK E MUDE DE VIDA #PIX #DINHEIRO"
    resultado = analisar_post(post_teste)
    print(resultado)
