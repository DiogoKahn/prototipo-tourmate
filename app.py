import os
import requests
from flask import Flask, render_template, request

# Ajuste das pastas de template e assets
app = Flask(__name__, template_folder='template', static_folder='template/assets')

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
    if clima.lower() == "inverno":
        clima = "Winter"
    elif clima.lower() == "verão":
        clima = "Summer"
    estado = request.form.get('Estado')
    tipo_viagem = request.form.get('tipo_viagem')
    if tipo_viagem.lower() == "turismo":
        tipo_viagem = "tourist"
    elif tipo_viagem.lower() == "religioso":
        tipo_viagem = "religious"

    prefs = {"Clima": clima, "Estado": estado, "tipo_viagem": tipo_viagem}

    return prefs

def recomendacao(prefs):
    OPENAI_API_KEY = "API-KEY"
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"}
    messages = []
    messages.append({"role": "system", 
                    "content": '''You are travel guide assistant that responds all travel recomendation in a python dictonary
                      with each key being a place or city and its contents being a list of strings of recomendations of things 
                      to do in that place or city. Respond with code only.'''
                      })
    
    messages.append({"role": "user", "content": 

                    f"Give me travel recomendations in {prefs['Estado']} state in {prefs['Clima']} with {prefs['tipo_viagem']} porposes. Translate the text to portuguese."})

    data = {"model": "gpt-3.5-turbo", "messages": messages}
    response = requests.post(url, headers=headers, json=data)
    reply = response.json()["choices"][0]["message"]["content"]

    reply = str(reply)
    resp = reply[reply.find("{"): reply.find("}")+1]
    resp = resp.replace("\n", "").replace("\t", "").replace("  ", "")

    resp = eval(resp)

    # Dados Mocados
    # resp = {'São Paulo': 
    #         ['Visit the São Paulo Museum of Art (MASP) and see works by famous artists like Van Gogh, Picasso and Monet.',
    #          'Explore the trendy Vila Madalena neighborhood, known for its street art, restaurants and nightlife.',
    #          "Take a walk around Ibirapuera Park, which is São Paulo's largest park and has several attractions including museums and a Japanese garden.",
    #          "Visit the Municipal Market of São Paulo, one of the city's main attractions where you can find several typical foods from Brazil and the world."
    #         ],
    #         'Campos do Jordão': 
    #          ['Enjoy the cold weather in the charming winter wonderland of Campos do Jordão.',
    #           'Visit the Frei Baraúna Convent, a historic building with beautiful architecture and stunning views of the surrounding mountains.',
    #           'Take a ride on the cable car to the top of the Elephant Hill for breathtaking views of the region.',
    #           'Explore the Campos do Jordão State Park, which has over 8,000 hectares of stunning nature and wildlife to discover.'
    #         ],
    #         'Ilhabela': 
    #          ["Relax on the island's beautiful beaches and swim in the turquoise waters.",
    #           'Hike to the top of the Baepi Hill for panoramic views of the island and surrounding seascape.',
    #           'Visit the Toca Waterfall, a stunning natural attraction with beautiful pools and surrounding rainforest.',
    #           'Take a boat tour around the island to explore its many coves, beaches and crystal-clear waters.'
    #          ]
    #         }

    return resp

## Renderiza o resultado predito pelo modelo ML na Webpage
@app.route('/send', methods=['POST'])
def show_data():

    prefs = get_preferencias()
    
    result = recomendacao(prefs)
    
    return render_template('result.html', result=result)


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))


