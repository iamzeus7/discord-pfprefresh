from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder='')

# User Ids para serem atualizados
user_ids = ['677705088822804506', '1044371077041770577', '1145041600980992030']

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

# Rota para cada usuário
@app.route('/<user_id>')
def avatar_page(user_id):
    avatar_url = fetch_avatar(user_id)
    if avatar_url:
        return render_template('avatar.html', avatar_url=avatar_url)
    else:
        return 'Avatar não encontrado'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
