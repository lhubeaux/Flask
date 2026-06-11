# Explications Flask - API Tasks

## Fonctions du fichier app.py

### Initialisation

```python
from flask import Flask, jsonify
app = Flask(__name__)
```

- Importe Flask et `jsonify` (non utilisé pour l'instant)
- Crée l'instance de l'application Flask

---

### Fonction `home()`

```python
@app.route('/')
def home():
    return "Bievenue sur l'API Tasks"
```

- **Route** : `GET /`
- **Rôle** : Répond à la racine de l'API avec un message de bienvenue en texte brut
- Le décorateur `@app.route('/')` lie l'URL `/` à cette fonction

---

### Lancement de l'application

```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

- Lance le serveur uniquement si le fichier est exécuté directement (pas importé comme module)
- `debug=True` : active le rechargement automatique et les messages d'erreur détaillés
- `port=5000` : le serveur écoute sur le port 5000

---

## Qu'est-ce qu'une route ?

Une **route** est l'association entre une **URL** et une **fonction Python** dans votre application.

Concrètement, c'est la réponse à la question : *"Quand l'utilisateur visite cette adresse, que doit faire l'application ?"*

---

### Exemple concret

```python
@app.route('/taches')
def get_taches():
    return "Liste des tâches"
```

Ici :
- L'URL `/taches` → appelle automatiquement la fonction `get_taches()`
- Si quelqu'un visite `http://localhost:5000/taches`, il reçoit `"Liste des tâches"`

---

### Analogie simple

Imaginez un standard téléphonique :
- Vous tapez le **numéro de poste** (l'URL)
- Vous êtes redirigé vers la **bonne personne** (la fonction)

---

### Les méthodes HTTP

Une route peut aussi réagir différemment selon le **type de requête** :

| Méthode | Usage typique |
|---------|--------------|
| `GET` | Lire des données |
| `POST` | Créer une ressource |
| `PUT` | Modifier une ressource |
| `DELETE` | Supprimer une ressource |

```python
@app.route('/taches', methods=['GET', 'POST'])
def taches():
    ...
```

---

## Implémentation du CRUD

### Les données en mémoire

Les tâches sont stockées dans une liste Python. Chaque tâche est un **dictionnaire** avec les champs suivants :

```python
task1 = {
    "id": 1,
    "titre": "tâche 1",
    "description": "réalisation de la tâche 1",
    "done": False,
    "created_at": datetime.now()
}
```

- `datetime.now()` génère automatiquement la date et l'heure actuelles
- `done` vaut `False` par défaut (la tâche n'est pas encore terminée)

Pour ajouter des éléments à la liste :
```python
tasks.append(task1)   # ajoute un seul élément
tasks.extend([task1, task2, task3])  # ajoute plusieurs éléments
```

---

### GET /api/tasks — Lister toutes les tâches

```python
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"data": tasks, "count": len(tasks)})
```

- `jsonify()` convertit un objet Python en réponse JSON
- `len(tasks)` retourne le nombre d'éléments dans la liste
- La réponse est structurée avec `"data"` (la liste) et `"count"` (le nombre de tâches)

---

### POST /api/tasks — Créer une tâche

```python
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "titre": data["titre"],
        "description": data["description"],
        "done": False,
        "created_at": datetime.now()
    }
    tasks.append(new_task)
    return jsonify({"message": "nouvelle tâche ajoutée", "tâche": new_task})
```

- `request.get_json()` lit le **body** de la requête envoyé par le client (ex: Postman) et le convertit en dictionnaire Python
- L'`id` est généré automatiquement avec `len(tasks) + 1`
- Le client envoie dans Postman un body JSON comme :
```json
{
    "titre": "Ma nouvelle tâche",
    "description": "Une description"
}
```

---

### GET /api/tasks/\<id\> — Récupérer une tâche

```python
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_specific_task(id):
    for i in tasks:
        if id == i["id"]:
            return jsonify(i)
    return jsonify({"message": "Cette tâche n'existe pas"}), 404
```

- `<int:id>` dans l'URL indique que `id` est un entier — Flask le passe automatiquement comme paramètre à la fonction
- Dans une boucle `for i in tasks`, `i` est directement **le dictionnaire de la tâche** (pas un index)
- Le `return 404` doit être **après** la boucle, pas à l'intérieur, sinon il s'exécute dès la première itération qui ne correspond pas
- `, 404` après `jsonify()` définit le code HTTP de la réponse

---

### PUT /api/tasks/\<id\> — Modifier une tâche

```python
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def modify_task(id):
    data = request.get_json()
    for i in tasks:
        if id == i["id"]:
            i["done"] = data.get("done", i["done"])
            i["titre"] = data.get("titre", i["titre"])
            i["description"] = data.get("description", i["description"])
            return jsonify(i)
    return jsonify({"message": "Tâche non trouvée"}), 404
```

- L'`id` vient de l'URL, le body contient uniquement les **champs à modifier**
- `data.get("done", i["done"])` signifie : *"prends `done` dans data, et si il n'existe pas, garde l'ancienne valeur"*
- Cela permet une **mise à jour partielle** — le client peut modifier un seul champ sans renvoyer tous les autres
- Différence entre `data["done"]` et `data.get("done", i["done"])` :
  - `data["done"]` → erreur si le champ est absent du body
  - `data.get("done", i["done"])` → garde l'ancienne valeur si le champ est absent

---

### DELETE /api/tasks/\<id\> — Supprimer une tâche

```python
@app.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for i in tasks:
        if id == i["id"]:
            tasks.remove(i)
            return jsonify({"message": f"Tâche {i['id']} supprimée avec succès"})
    return jsonify({"message": "Cette tâche n'existe pas"}), 404
```

- `tasks.remove(i)` supprime l'élément `i` de la liste `tasks`
- Comme pour le GET par id, le `return 404` doit être **après** la boucle

---

## Les deux sources d'information dans une route

| Source | Récupéré via | Contient |
|--------|-------------|---------|
| L'URL `/api/tasks/1` | Paramètre `id` de la fonction | Quelle ressource cibler |
| Le body (Postman) | `data = request.get_json()` | Les données à traiter |
