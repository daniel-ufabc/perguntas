from flask import Flask, request, render_template, redirect
import uuid as uu
import csv

app = Flask(__name__)


questionario = {
    1: {
        'texto': 'Você é palmeirense?',
        'respostas': {
            'sim': 2,
            'nao': 3
            }
        },
    2: {
        'texto': 'Você sabe o nome do goleiro do Palmeiras?',
        'respostas': {
            'sim': 4,
            'nao': 5
            }
        },
    3: {
        'texto': 'Então você não é porco.',
        'respostas': dict(),
        },
    4: {
        'texto': 'Então você é muito porco!',
        'respostas': dict(),
        },
    5: {
        'texto': 'Então você não é tão porco assim!',
        'respostas': dict(),
        }  
}

respostas = {}

@app.route('/hello')
def hello():
    return 'Hello'


@app.route('/', methods=['GET'])
def pergunta():
    data = request.args
    if 'id' not in data:
        uuid = uu.uuid1()
        return render_template('pergunta.html',
                               id_pergunta='1',
                               texto_pergunta=questionario[1]['texto'],
                               respostas=questionario[1]['respostas'],
                               uuid=uuid)

    id_atual = int(data['id'])
    uuid = data['uuid']

    if 'resposta' not in data:
        with open('mycsvfile.csv', 'a') as f:  
            w = csv.DictWriter(f, list(questionario.keys()) + ['uuid'])
            w.writerow(respostas[uuid])

        return redirect('/')

    target = int(data['resposta'])
    comment = data['comment']
    if uuid not in respostas:
        respostas[uuid] = {'uuid': 'uuid: ' + uuid}

    possiveis = questionario[id_atual]['respostas']
    for key in possiveis:
        if possiveis[key] == target:
            respostas[uuid][id_atual] = str(id_atual) + ':' + str(key)
            break

    return render_template('pergunta.html',
                           id_pergunta=data['resposta'],
                           texto_pergunta=questionario[target]['texto'],
                           respostas=questionario[target]['respostas'],
                           uuid=uuid)
    
    


        



    

app.run(debug=True)
    
