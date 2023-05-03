import os
import requests
from flask import Flask, render_template, request

# Ajuste das pastas de template e assets
app = Flask(__name__, template_folder='template', static_folder='template/assets')

# Import do modelo já treinado e salvo (essa parte foi feita no jupyter notebook)
# modelo_pipeline = pickle.load(open('./models/models.pkl', 'rb'))


# Pagina principal
@app.route('/')
def home():
    return render_template("homepage.html")

# Pagina Forms que é preenchido pelo usuario
@app.route('/dados_pref')
def dados_pref():
    return render_template("form_pref.html")

def get_preferencias():

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    clima = request.form.get('Clima')
    estado = request.form.get('Estado')
    tipo_viagem = request.form.get('tipo_viagem')

    # string = 'Nome: '+ nome+ '| Email: '+ email+ '\n'+ 'clima: '+ clima + '| região: '+ regiao+ '| local: '+ local+ '| Tipo de Viagem: '+tipo_viagem
    
    prefs = {"Clima": clima, "Estado": estado, "tipo_viagem": tipo_viagem}

    return prefs

## Renderiza o resultado predito pelo modelo ML na Webpage
@app.route('/send', methods=['POST'])
def show_data():

    prefs = get_preferencias()
    
    result = recomendacao(prefs)
    
    return render_template('result.html', result=result)

@app.route('/results',methods=['POST'])
def recomendacao(prefs):
    OPENAI_API_KEY = "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"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"}
    messages = []
    messages.append({"role": "system", 
                    "content": "You are travel guide assistant that responds all travel recomendation in a python dictonary with each key being a place or city and its contents being a list of strings of recomendations of things to do in that place or city. Respond with code only."})
    
    messages.append({"role": "user", "content": 
                    f"Give me travel recomendations in {prefs['Estado']}'s state in {prefs['Clima']} with {prefs['tipo_viagem']} porposes."})
    data = {"model": "gpt-3.5-turbo", "messages": messages}
    response = requests.post(url, headers=headers, json=data)
    reply = response.json()["choices"][0]["message"]["content"]

    reply = str(reply)
    resp = reply[reply.find("{"): reply.find("}")+1]
    resp = resp.replace("\n", "").replace("\t", "").replace("  ", "")

    resp = eval(resp)

    return resp

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
