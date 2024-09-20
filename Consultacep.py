import requests

def consultar_cep(cep):
    # Limpa o CEP removendo traços e espaços
    cep = cep.replace("-", "").strip()

    # URL da API ViaCEP
    url = f"https://viacep.com.br/ws/{cep}/json/"

    # Fazendo a requisição GET
    response = requests.get(url)

    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        dados = response.json()
        
        # Verifica se o CEP é válido
        if "erro" in dados:
            return "CEP inválido. Tente novamente."
        else:
            # Retorna o endereço formatado
            return f"CEP: {dados['cep']}, Logradouro: {dados['logradouro']}, Bairro: {dados['bairro']}, Cidade: {dados['localidade']}, Estado: {dados['uf']}"
    else:
        return "Erro ao consultar o CEP. Tente novamente mais tarde."

# Testando a função (se executado diretamente)
if __name__ == "__main__":
    cep_input = input("Digite o CEP para consulta: ")
    resultado = consultar_cep(cep_input)
    print(resultado)
