from flask import jsonify, request
from datetime import datetime

task1 = {"id": 1, "titre": "tâche 1", "description": "réalisation de la tâche 1", "done": False, "created_at": datetime.now(), "updated_at": None}
task2 = {"id": 2, "titre": "tâche 2", "description": "réalisation de la tâche 2", "done": False, "created_at": datetime.now(), "updated_at": None}
task3 = {"id": 3, "titre": "tâche 3", "description": "réalisation de la tâche 3", "done": True, "created_at": datetime.now(), "updated_at": None}

tasks = [task1, task2, task3]

def filter_tasks(done):
    done_tasks = []
    for t in tasks:
        if t["done"] == (done == "true"):
            done_tasks.append(t)
    return done_tasks


def get_all_tasks():
    done = request.args.get("done")
    if done is None:
        return jsonify({"data": tasks, "count": len(tasks)})
    else:
        result = filter_tasks(done)
        return jsonify({"data": result, "count": len(result)})


def create_task():
    data = request.get_json(silent=True)
    if data is None or "titre" not in data:
        return jsonify({"message": "Titre est nécessaire"}), 400
    new_task = {"id": len(tasks) + 1, "titre": data["titre"], "description": data["description"], "done": False, "created_at": datetime.now(), "updated_at": None}
    tasks.append(new_task)
    return jsonify({"message": "nouvelle tâche ajoutée", "tâche": new_task}), 201

def get_specific_task(id):
    for i in tasks:
        if id == i["id"]:
            return jsonify(i)
    else:
        return jsonify({"message" : "Cette tâche n'existe pas"}), 404
    
def modify_task(id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"message" : "Veuillez fournir des données !"}), 400
    else:
        for i in tasks:
            if id == i["id"]:
                i["done"] = data.get("done", i["done"])
                i["titre"] = data.get("titre", i["titre"])
                i["description"] = data.get("description", i["description"])
                i["updated_at"] = datetime.now()
                return jsonify(i)
        return jsonify({"message" : "Tâche non trouvée"}), 404
    
def delete_task(id):
    for i in tasks:
        if id == i["id"]:
            tasks.remove(i)
            return jsonify({"message" : f'Tâche {i["id"]} supprimée avec succès'})
    return jsonify({"message" : "Cette tâche n'existe pas"}), 404