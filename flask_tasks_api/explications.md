# Explications Flask - API Tasks

---

## Table des matières

- [1. Fonctions du fichier app.py](#1-fonctions-du-fichier-apppy)
  - [Initialisation](#initialisation)
  - [Fonction home()](#fonction-home)
  - [Lancement de l'application](#lancement-de-lapplication)
- [2. Qu'est-ce qu'une route ?](#2-quest-ce-quune-route-)
  - [Exemple concret](#exemple-concret)
  - [Analogie simple](#analogie-simple)
  - [Les méthodes HTTP](#les-méthodes-http)
- [3. Implémentation du CRUD](#3-implémentation-du-crud)
  - [Les données en mémoire](#les-données-en-mémoire)
  - [GET /api/tasks — Lister toutes les tâches](#get-apitasks--lister-toutes-les-tâches)
  - [POST /api/tasks — Créer une tâche](#post-apitasks--créer-une-tâche)
  - [GET /api/tasks/<id> — Récupérer une tâche](#get-apitasksid--récupérer-une-tâche)
  - [PUT /api/tasks/<id> — Modifier une tâche](#put-apitasksid--modifier-une-tâche)
  - [DELETE /api/tasks/<id> — Supprimer une tâche](#delete-apitasksid--supprimer-une-tâche)
- [4. Les deux sources d'information dans une route](#4-les-deux-sources-dinformation-dans-une-route)
- [5. Les query parameters avec request.args](#5-les-query-parameters-avec-requestargs)
  - [Qu'est-ce qu'un query parameter ?](#quest-ce-quun-query-parameter-)
  - [Comment le lire dans Flask ?](#comment-le-lire-dans-flask-)
  - [Différence avec les paramètres de chemin](#différence-avec-les-paramètres-de-chemin)
  - [Attention : string vs booléen](#attention--string-vs-booléen)
- [6. Partie 3 — Améliorations](#6-partie-3--améliorations)
  - [Validation du champ titre](#validation-du-champ-titre)
  - [get_json(silent=True)](#get_jsonsilenttrue)
  - [Codes HTTP de réponse](#codes-http-de-réponse)
  - [Filtrage avec filter_tasks()](#filtrage-avec-filter_tasks)
  - [Champ updated_at](#champ-updated_at)
- [7. Partie bonus — Architecture routes / controllers](#7-partie-bonus--architecture-routes--controllers)
  - [Le problème : tout dans un seul fichier](#le-problème--tout-dans-un-seul-fichier)
  - [La répartition des rôles](#la-répartition-des-rôles)
  - [Le dossier controllers/](#le-dossier-controllers)
  - [Le dossier routes/ et le Blueprint](#le-dossier-routes-et-le-blueprint)
  - [app.py et register_blueprint()](#apppy-et-register_blueprint)
  - [Comment la connexion se fait réellement](#comment-la-connexion-se-fait-réellement)
  - [La chaîne d'imports](#la-chaîne-dimports)

---

## 1. Fonctions du fichier app.py

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

## 2. Qu'est-ce qu'une route ?

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

## 3. Implémentation du CRUD

### Les données en mémoire

Les tâches sont stockées dans une liste Python. Chaque tâche est un **dictionnaire** avec les champs suivants :

```python
task1 = {
    "id": 1,
    "titre": "tâche 1",
    "description": "réalisation de la tâche 1",
    "done": False,
    "created_at": datetime.now(),
    "updated_at": None
}
```

- `datetime.now()` génère automatiquement la date et l'heure actuelles
- `done` vaut `False` par défaut (la tâche n'est pas encore terminée)
- `updated_at` vaut `None` tant que la tâche n'a jamais été modifiée

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
    data = request.get_json(silent=True)
    new_task = {
        "id": len(tasks) + 1,
        "titre": data["titre"],
        "description": data["description"],
        "done": False,
        "created_at": datetime.now(),
        "updated_at": None
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
    data = request.get_json(silent=True)
    for i in tasks:
        if id == i["id"]:
            i["done"] = data.get("done", i["done"])
            i["titre"] = data.get("titre", i["titre"])
            i["description"] = data.get("description", i["description"])
            i["updated_at"] = datetime.now()
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

## 4. Les deux sources d'information dans une route

| Source | Récupéré via | Contient |
|--------|-------------|---------|
| L'URL `/api/tasks/1` | Paramètre `id` de la fonction | Quelle ressource cibler |
| Le body (Postman) | `data = request.get_json()` | Les données à traiter |
| L'URL `?done=true` | `request.args.get("done")` | Filtres ou options |

---

## 5. Les query parameters avec `request.args`

### Qu'est-ce qu'un query parameter ?

Un **query parameter** est une information optionnelle ajoutée à la fin d'une URL après le `?` :

```
http://localhost:5000/api/tasks?done=true
                               ^^^^^^^^^^^
                               query parameter
```

- La **clé** est `done`
- La **valeur** est `"true"` (toujours une chaîne de caractères)

On peut en chaîner plusieurs avec `&` : `/api/tasks?done=true&titre=urgent`

---

### Comment le lire dans Flask ?

Flask capture automatiquement les query parameters via `request.args`. Tu n'as **pas besoin** de les indiquer dans le décorateur `@app.route` — la route reste la même.

```python
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    done_param = request.args.get("done")  # lit ?done=...
```

- Si l'URL est `/api/tasks?done=true` → `done_param = "true"`
- Si l'URL est `/api/tasks?done=false` → `done_param = "false"`
- Si l'URL est `/api/tasks` (sans paramètre) → `done_param = None`

---

### Différence avec les paramètres de chemin

| Type | Exemple d'URL | Récupéré via |
|------|--------------|-------------|
| Paramètre de chemin | `/api/tasks/1` | `<int:id>` dans `@app.route` + paramètre de fonction |
| Query parameter | `/api/tasks?done=true` | `request.args.get("done")` à l'intérieur de la fonction |

---

### Attention : string vs booléen

`request.args.get("done")` retourne toujours une **string**, jamais un booléen Python.

```python
done_param = "true"      # string, pas un booléen
i["done"] == True        # booléen Python

# Pour les comparer :
i["done"] == (done_param == "true")   # convertit implicitement
```

---

## 6. Partie 3 — Améliorations

### Validation du champ `titre`

Le champ `titre` est obligatoire à la création d'une tâche. Sans validation, Python lève une `KeyError` si le champ est absent.

```python
data = request.get_json(silent=True)
if data is None or "titre" not in data:
    return jsonify({"message": "Titre est nécessaire"}), 400
```

- `data is None` → couvre le cas où le client n'envoie pas de body JSON
- `"titre" not in data` → couvre le cas où le body existe mais sans le champ `titre`
- Les deux conditions sont combinées avec `or` pour retourner une seule réponse `400`

---

### `get_json(silent=True)`

Par défaut, `request.get_json()` lève une erreur `400` si le body n'est pas du JSON valide ou si le header `Content-Type: application/json` est absent.

Avec `silent=True`, il retourne simplement `None` au lieu de planter :

```python
# Sans silent=True → peut planter avec une erreur 400 Flask
data = request.get_json()

# Avec silent=True → retourne None proprement
data = request.get_json(silent=True)
```

C'est une bonne pratique pour toute API publique, car le contrôle de l'erreur revient à ton code.

---

### Codes HTTP de réponse

| Code | Signification | Quand l'utiliser |
|------|--------------|-----------------|
| `200` | OK | Succès (réponse par défaut de Flask) |
| `201` | Created | Ressource créée avec succès (POST) |
| `400` | Bad Request | Données invalides ou manquantes |
| `404` | Not Found | Ressource inexistante |

```python
return jsonify({"message": "Titre est nécessaire"}), 400  # données invalides
return jsonify({"message": "Tâche non trouvée"}), 404     # ressource absente
```

---

### Filtrage avec `filter_tasks()`

Pour filtrer les tâches selon leur statut, on sépare la logique en deux fonctions :

```python
# Fonction helper — logique de filtrage pure
def filter_tasks(done):
    done_tasks = []
    for t in tasks:
        if t["done"] == (done == "true"):
            done_tasks.append(t)
    return done_tasks

# Route — gère la requête et appelle le helper
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    done = request.args.get("done")
    if done is None:
        return jsonify({"data": tasks, "count": len(tasks)})
    else:
        result = filter_tasks(done)
        return jsonify({"data": result, "count": len(result)})
```

**Pourquoi `(done == "true")` ?**

`done` est la string `"true"` ou `"false"`, mais `t["done"]` est un booléen `True` ou `False`. L'expression `done == "true"` convertit la string en booléen implicitement :

| `done` reçu | `done == "true"` | `t["done"]` attendu |
|------------|-----------------|-------------------|
| `"true"` | `True` | `True` |
| `"false"` | `False` | `False` |

---

### Champ `updated_at`

Ce champ enregistre la date de la dernière modification d'une tâche.

**À la création** — initialisé à `None` (jamais modifiée) :
```python
new_task = {
    ...
    "created_at": datetime.now(),
    "updated_at": None
}
```

**À chaque modification** — mis à jour avec l'heure actuelle :
```python
i["updated_at"] = datetime.now()
```

Ainsi, si `updated_at` est `None`, la tâche n'a jamais été modifiée depuis sa création.

---

## 7. Partie bonus — Architecture routes / controllers

### Le problème : tout dans un seul fichier

Au départ, tout vit dans `app.py` : la création de l'app, les données, la logique métier et les routes — le tout mélangé dans un seul fichier. Ça fonctionne, mais plus le projet grandit, plus c'est difficile à lire et à maintenir.

La partie bonus consiste à **séparer les responsabilités** (*separation of concerns*) en plusieurs dossiers, où chaque dossier a **un seul rôle**.

---

### La répartition des rôles

| Couche | Dossier | Répond à la question | Contenu |
|--------|---------|---------------------|---------|
| **Routes** | `routes/` | *« Quelle URL → quelle fonction ? »* | les associations URL ↔ fonction, rien d'autre |
| **Controllers** | `controllers/` | *« Que faire concrètement ? »* | la logique métier + les données |
| **App** | `app.py` | *« Assembler le tout »* | crée l'app, enregistre les routes, lance le serveur |

Le sens des dépendances est important — chaque niveau ne connaît que celui en dessous :

```
app.py  ──importe──>  routes/task_routes.py  ──importe──>  controllers/task_controllers.py
(assemble)            (branche les URLs)                   (fait le travail + données)
```

---

### Le dossier `controllers/`

Le controller contient **la logique métier** : lire les données, filtrer, créer une tâche, valider le titre, renvoyer le bon code HTTP… C'est tout ce qui était *à l'intérieur* des fonctions de route.

Points importants :
- On n'importe **plus `Flask`** ici — le controller ne connaît pas l'application, il ne fait que de la logique. On importe seulement `jsonify` et `request`.
- La liste `tasks` vit **dans le controller**, parce que c'est lui qui la manipule.
- Les fonctions portent des noms qui décrivent **l'action** (`get_all_tasks`, `create_task`…), pas l'URL. Le décorateur `@...route` n'apparaît **pas** ici.

```python
from flask import jsonify, request
from datetime import datetime

tasks = [task1, task2, task3]

def get_all_tasks():
    done = request.args.get("done")
    if done is None:
        return jsonify({"data": tasks, "count": len(tasks)})
    else:
        result = filter_tasks(done)
        return jsonify({"data": result, "count": len(result)})
```

---

### Le dossier `routes/` et le Blueprint

#### Pourquoi un Blueprint ?

Dans `app.py`, on écrivait `@app.route(...)`. Mais `app`, l'objet Flask, **n'existe que dans `app.py`**. Si on écrit `@app.route` dans `routes/task_routes.py`, Python ne sait pas ce qu'est `app` → erreur.

Un **Blueprint** est la solution officielle de Flask : un *« carnet de routes »* indépendant qu'on remplit sans avoir besoin de l'objet `app`. Plus tard, `app.py` viendra le brancher.

```python
from flask import Blueprint
from controllers.task_controllers import get_all_tasks, create_task, get_specific_task, modify_task, delete_task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    return get_all_tasks()

@task_bp.route('/api/tasks/<int:id>', methods=['PUT'])
def modification(id):
    return modify_task(id)        # l'id capté dans l'URL est transmis au controller
```

Deux changements par rapport à `app.py` :
1. `@app.route` devient **`@task_bp.route`** (on accroche la route au carnet, pas à l'app).
2. Le corps de la fonction ne fait plus le travail → il **appelle le controller**.

> **Attention** : pour les routes avec `<int:id>`, l'`id` doit voyager **URL → fonction de route → controller**. Il faut donc bien écrire `modify_task(id)` et non `modify_task()`, sinon Python lève `missing 1 required positional argument: 'id'`.

---

### `app.py` et `register_blueprint()`

`app.py` n'a plus besoin de contenir les données, la logique ou les routes. Son seul rôle : **créer l'app et y brancher le blueprint**.

```python
from flask import Flask
from routes.task_routes import task_bp

app = Flask(__name__)
app.register_blueprint(task_bp)

@app.route('/')
def home():
    return "Bievenue sur l'API Tasks"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

- `from routes.task_routes import task_bp` → récupère le carnet de routes déjà rempli.
- `app.register_blueprint(task_bp)` → **ligne clé** : colle toutes les routes du carnet dans l'application. Sans elle, les routes existeraient mais Flask ne les connaîtrait pas → `404` partout.

---

### Comment la connexion se fait réellement

C'est le point le plus subtil : **si l'URL n'est pas déclarée avec `@app.route`, comment peut-elle fonctionner ?**

Réponse : **au final, elle l'est.** `register_blueprint` finit par inscrire chaque URL dans la table de `app`, exactement comme `@app.route` l'aurait fait. Le `@task_bp.route` n'est qu'une façon **différée** d'écrire `@app.route`.

#### Un blueprint, c'est un objet qui contient une liste

En version simplifiée, un blueprint n'est qu'un objet avec une liste à l'intérieur :

```python
class Blueprint:
    def __init__(self, nom):
        self.nom = nom
        self.routes = []          # une simple liste, vide au départ

    def route(self, url, methods):
        def decorateur(fonction):
            self.routes.append((url, methods, fonction))   # AJOUTE à la liste
            return fonction
        return decorateur
```

Un décorateur n'a **rien de magique** : `@task_bp.route('/api/tasks', methods=['GET'])` au-dessus de `get_tasks` revient exactement à exécuter :

```python
task_bp.routes.append(('/api/tasks', ['GET'], get_tasks))
```

#### Après l'import, le blueprint est rempli

Une fois `task_routes.py` entièrement lu (les décorateurs exécutés), l'attribut `.routes` de `task_bp` contient les routes sous forme de **données rangées dans une liste** — aucune n'est encore active :

```python
task_bp.routes = [
    ('/api/tasks',          ['GET'],    get_tasks),
    ('/api/tasks',          ['POST'],   post_task),
    ('/api/tasks/<int:id>', ['GET'],    get_task),
    ('/api/tasks/<int:id>', ['PUT'],    modification),
    ('/api/tasks/<int:id>', ['DELETE'], deletion),
]
```

#### `register_blueprint` verse cette liste dans `app`

L'objet `app` a sa **propre liste** de routes — la vraie, celle que le serveur consulte. `register_blueprint` ne fait que parcourir la liste du blueprint et recopier chaque élément dans celle de `app` :

```python
def register_blueprint(app, blueprint):
    for (url, methods, fonction) in blueprint.routes:
        app.add_url_rule(url, fonction.__name__, fonction, methods=methods)  # AJOUTE à app
```

C'est **seulement à cet instant** que les routes deviennent réelles. Ces deux versions produisent rigoureusement le même résultat dans la table de `app` :

```python
# Version directe
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return get_all_tasks()

# Version blueprint (la nôtre)
@task_bp.route('/api/tasks', methods=['GET'])   # range dans task_bp.routes
def get_tasks():
    return get_all_tasks()
app.register_blueprint(task_bp)                 # rejoue la note sur app
```

#### Résumé

| Moment | Ce qui se passe | Où sont les URLs |
|--------|-----------------|------------------|
| `task_bp = Blueprint(...)` | crée un objet avec `.routes = []` | liste vide |
| les `@task_bp.route` | font `.routes.append(...)` | dans la liste du **blueprint** |
| `app = Flask(...)` | crée l'app avec sa propre liste | app : juste `/` |
| `register_blueprint(task_bp)` | recopie les éléments dans la liste de l'app | dans la liste de **app** ✅ |

---

### La chaîne d'imports

Le détail invisible : **importer un module = exécuter son code**. La ligne `from routes.task_routes import task_bp` ne « copie pas juste une variable » — elle oblige Python à exécuter `task_routes.py` en entier, ce qui fait tourner les décorateurs et remplit `task_bp`.

```
1. python app.py
2. ligne "from routes.task_routes import task_bp"
      → met app.py en pause, exécute task_routes.py en entier
3. task_routes.py s'exécute :
      → "from controllers..." exécute task_controllers.py (crée tasks, définit les fonctions)
      → crée task_bp
      → les @task_bp.route remplissent task_bp.routes
4. task_bp (REMPLI) revient dans app.py → app.py reprend
5. app = Flask(__name__)            → table de routes : juste "/"
6. app.register_blueprint(task_bp)  → ajoute les routes /api/tasks à la table de app
```

> **Piège classique** : un blueprint qu'on **oublie d'importer** ne sera jamais exécuté par Python. Le fichier existe, le code a l'air correct, mais comme rien ne l'importe, les décorateurs ne tournent jamais et les routes restent invisibles (`404`).

Pour visualiser la table de routage finale et vérifier que tout est branché : la commande `flask routes` liste toutes les routes réellement enregistrées dans `app`.
