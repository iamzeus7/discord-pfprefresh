from flask import Flask, render_template, send_from_directory
import requests
import os

app = Flask(__name__, template_folder='')

# Diretório onde os avatares serão salvos
avatar_directory = ''

# Criar o diretório se não existir
if not os.path.exists(avatar_directory):
    os.makedirs(avatar_directory)

# IDs dos usuários do Discord cujos avatares queremos buscar
user_ids = ['ID_DO_USUARIO_1', 'ID_DO_USUARIO_2', 'ID_DO_USUARIO_3']

# Função para buscar o avatar de um usuário específico
def fetch_avatar(user_id):
    try:
        url = f"https://pfpfinder.com/api/discord/user/{user_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('avatar')  # Assume que a API retorna o link direto para o avatar
        else:
            print(f"Erro ao buscar avatar para o usuário {user_id}. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao buscar avatar para o usuário {user_id}: {str(e)}")
        return None

# Função para salvar o avatar no servidor
def save_avatar(user_id, avatar_url):
    try:
        # Remover avatar anterior se existir
        avatar_path = os.path.join(avatar_directory, f"{user_id}.gif")
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
        
        # Baixar o novo avatar
        response = requests.get(avatar_url)
        if response.status_code == 200:
            with open(avatar_path, 'wb') as f:
                f.write(response.content)
            return True
        else:
            print(f"Erro ao salvar avatar para o usuário {user_id}. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro ao salvar avatar para o usuário {user_id}: {str(e)}")
        return False

# Rota para a página inicial (home)
@app.route('/')
def home():
    return render_template('index.html')

# Rota para cada usuário
@app.route('/<user_id>')
def avatar_page(user_id):
    avatar_url = fetch_avatar(user_id)
    if avatar_url:
        # Salvar o avatar no servidor
        save_avatar(user_id, avatar_url)
        return render_template('avatar.html', user_id=user_id)
    else:
        return 'Avatar não encontrado'

# Rota para servir os avatares estáticos
@app.route('/avatars/<filename>')
def serve_avatar(filename):
    return send_from_directory(avatar_directory, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
