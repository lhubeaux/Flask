from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


task1={"id" : 1, "titre" : "tâche 1", "description" : "réalisation de la tâche 1","done" : False, "created_at" : datetime.now()}
task2={"id" : 2, "titre" : "tâche 2", "description" : "réalisation de la tâche 2","done" : False, "created_at" : datetime.now()}
task3={"id" : 3, "titre" : "tâche 3", "description" : "réalisation de la tâche 3","done" : False, "created_at" : datetime.now()}

tasks = []
tasks.append(task1)
tasks.append(task2)
tasks.append(task3)

@app.route('/')
def home():
    return "Bievenue sur l'API Tasks"

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"data" : tasks, "count": len(tasks)})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    titre = data["titre"]
    descrip = data["description"]
    new_task = {"id": len(tasks)+1,"titre" : titre, "description" : descrip, "done" : False,"created_at" : datetime.now()}
    tasks.append(new_task)
    
    return jsonify({"message" : "nouvelle tâche ajoutée", "tâche" : new_task})


@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_specific_task(id):
    for i in tasks:
        if id == i["id"]:
            return jsonify(i)
    else:
        return jsonify({"message" : "Cette tâche n'existe pas"}), 404
    
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def modify_task(id):
    data = request.get_json()
    for i in tasks:
        if id == i["id"]:
            i["done"] = data.get("done", i["done"])
            i["titre"] = data.get("titre", i["titre"])
            i["description"] = data.get("description", i["description"])
            return jsonify(i)
    return jsonify({"message" : "Tâche non trouvée"}), 404

@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for i in tasks:
        if id == i["id"]:
            tasks.remove(i)
            return f'Tâche {i["id"]} supprimée avec succès'
    return jsonify({"message" : "Cette tâche n'existe pas"}), 404





if __name__ == '__main__':
    app.run(debug=True, port=5000)