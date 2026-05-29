print("Carregando Atproto...")
from atproto import Client
print("Carregando verificacao do modelo....")
from monitor_bluesky import verificar_e_guardar
print("Quase la...")
import time

HANDLE = "ggabigol.bsky.social"
PASSWORD = "rouw-cee7-niyt-eai6"

client = Client()

def iniciar_monitoramento():
    try:
        print(f"Conectando ao BlueSky como {HANDLE}")
        client.login(HANDLE, PASSWORD)
        #print("Conectado com sucesso! Monitorando posts..\n")
        print("Conectado com sucesso! Monitorando posts e injetando testes...\n")
        
        posts_teste_semantico = [
            "O trânsito na Mauro Ramos está completamente travado hoje por causa da chuva.", #post 1
            "Estou estudando inteligência artificial e processamento de linguagem natural no laboratório.", #post 2
            "Compre criptomoedas agora com desconto usando o meu link!", #post 3
            
            "Que engarrafamento horrível no centro de Floripa, não sai do lugar e tá chovendo muito.", #liga alerta com o post 1
            "Desenvolvendo modelos de NLP e IA para a faculdade.", #liga o alerta com o post 2
            "Invista em bitcoin hoje mesmo e mude de vida, clique aqui.", #liga o alerta com o post 3
            "O dia está bonito para caminhar na Beira-Mar Norte." #registra como post original
        ]

        print("--- INICIANDO TESTE SEMÂNTICO CONTROLADO ---")
        for post_falso in posts_teste_semantico:
            resultado = verificar_e_guardar(post_falso)
            print(f"[TESTE INDUZIDO]: {post_falso[:60]}...")
            print(f"↳ Resultado: {resultado}")
            print("-" * 30)
            time.sleep(4) 

        print("\n--- TESTE SEMÂNTICO CONCLUÍDO. ENTRANDO NO FLUXO REAL DA TIMELINE ---")

        while True:
            #puxa os posts da timeline "folowing"
            timeline = client.get_timeline(limit=100)
            
            for item in timeline.feed:
                post_texto = item.post.record.text
                autor = item.post.author.handle
                
                #verificacao do Llama3.2
                resultado = verificar_e_guardar(post_texto)
                
                print(f"[@{autor}]: {post_texto[:50]}...")
                print(f"↳ Resultado: {resultado}")
                print("-" * 30)

            #espera x segundos para nao ser bloqueado por excesso de requisicoes
            time.sleep(10)

    except Exception as e:
        print(f"Erro na conexao: {e}")

if __name__ == "__main__":
    iniciar_monitoramento()