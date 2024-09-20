from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from Consultacep import consultar_cep  # Importar a função de consulta do CEP

# Inicializar as opções do WebDriver do Edge
options = webdriver.EdgeOptions()
options.add_argument('--ignore-certificate-errors')  # Desativar a verificação SSL

# Inicializar o WebDriver do Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# Abrir o WhatsApp Web
driver.get("https://web.whatsapp.com")
print("Escaneie o QR code para logar no WhatsApp Web.")
time.sleep(20)  # Aguardar o login manual via QR Code

# Função para enviar uma mensagem de boas-vindas e solicitar o CEP
def enviar_bem_vindo(contato):
    # Buscar o contato
    search_box = driver.find_element("xpath", '//div[@role="textbox"][@contenteditable="true"]')
    search_box.click()
    search_box.send_keys(contato)
    time.sleep(2)  # Espera o contato ser encontrado
    search_box.send_keys(Keys.ENTER)

    # Enviar a mensagem de boas-vindas
    campo_input = driver.find_element("xpath", '//div[@role="textbox"][@contenteditable="true"]')
    campo_input.click()
    campo_input.send_keys("Bem-vindo(a) ao Matfy! Por favor, me envie o seu CEP para consulta.")
    campo_input.send_keys(Keys.ENTER)

# Função para monitorar novas mensagens e consultar o CEP
def monitorar_mensagens():
    while True:
        # Captura todas as mensagens na conversa ativa
        mensagens = driver.find_elements("xpath", '//div[contains(@class, "message-in")]//span[@dir="ltr"]')
        ultima_mensagem = mensagens[-1].text if mensagens else ""
        
        # Verifica se a última mensagem contém um CEP
        if len(ultima_mensagem) == 8 or len(ultima_mensagem) == 9:
            # Verifica se é um CEP no formato correto (número com ou sem hífen)
            if ultima_mensagem.isdigit() or (ultima_mensagem.count('-') == 1 and ultima_mensagem.replace("-", "").isdigit()):
                print(f"CEP recebido: {ultima_mensagem}")
                
                # Chama a função consultar_cep e envia a resposta
                resultado_cep = consultar_cep(ultima_mensagem)
                enviar_mensagem(resultado_cep)
        
        time.sleep(5)  # Aguardar alguns segundos antes de verificar novamente

# Função para enviar uma mensagem de volta ao usuário
def enviar_mensagem(mensagem):
    # Localizar a caixa de texto de mensagem
    campo_input = driver.find_element("xpath", '//div[@role="textbox"][@contenteditable="true"]')
    campo_input.click()
    campo_input.send_keys(mensagem)
    campo_input.send_keys(Keys.ENTER)

# Nome do contato para enviar a mensagem de boas-vindas
contato = "Nome do Contato"  # Troque pelo nome do contato ou grupo

# Enviar mensagem de boas-vindas ao contato
enviar_bem_vindo(contato)

# Iniciar a monitoração de mensagens
monitorar_mensagens()

# Encerrar o WebDriver (se necessário em algum ponto)
# driver.quit()
