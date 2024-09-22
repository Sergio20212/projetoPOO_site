import re

# URLs válidas e histórico de navegação
sitemap = {}
visit_history = []
current_page = None


def is_valid_url(url):
    # Expressão regular para validar URLs com ou sem http:// ou https://
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http://, https://, ftp:// (opcional)
        r'|(?:'  # ou
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domínio...
        r'localhost|'  # ...ou localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...ou endereço IP
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...ou IPv6
        r'(?::\d+)?'  # porta opcional
        r'(?:/?|[/?]\S+)?$', re.IGNORECASE)  # caminho opcional

    return re.match(regex, url) is not None

def load_urls(filename):
    
    try:
        with open(filename, 'r') as file:
            for url in map(str.strip, file):
                if is_valid_url(url):
                    sitemap[url] = []
        print("URLs carregadas.")
    except FileNotFoundError:
        print(f"Erro: {filename} não encontrado.")



# Mostra o histórico de navegação
def show_history():
    print(f"Histórico de Visitas: {' -> '.join(visit_history) if visit_history else '[ ]'}")

# Navega para uma nova URL
def navigate(url):
    global current_page
    full_url = current_page + url if url.startswith("/") and current_page else url
    if full_url in sitemap:
        visit_history.append(current_page) if current_page else None
        current_page = full_url
        print(f"Página encontrada! Home: [{current_page}]")
    else:
        print("Página não encontrada.")

# Adiciona uma nova URL
def add_url(url):
    if is_valid_url(url):
        if url not in sitemap:
            sitemap[url] = []
            print(f"URL {url} adicionada.")
        else:
            print("URL já existente.")
    else:
        print("Formato de URL inválido.")

# Retorna à última página visitada
def back():
    global current_page
    current_page = visit_history.pop() if visit_history else None
    print(f"Retornando à página: {current_page}" if current_page else "Não há páginas anteriores.")

# Interface de interação do navegador
def run_browser():
    load_urls('urls.txt')
    while True:
        print(f"\nHome: [{current_page if current_page else ' '}]")
        user_input = input("Digite a url ou #back, #sair, #showhist, #add <url>: ").strip()

        if user_input.startswith("#add "):
            add_url(user_input[5:].strip())
        elif user_input == "#back":
            back()
        elif user_input == "#showhist":
            show_history()
        elif user_input == "#sair":
            break
        else:
            navigate(user_input)

# Inicia o navegador
run_browser()
