# Point d'entrée de l'application : crée l'instance Flask et enregistre les routes.
from flask import Flask
from routes.task_routes import task_bp

# Création de l'application Flask et enregistrement du blueprint des tâches.
app = Flask(__name__)
app.register_blueprint(task_bp)


@app.route('/')
def home():
    """Route racine : message d'accueil de l'API."""
    return "Bievenue sur l'API Tasks"


# Lancement du serveur de développement uniquement si le fichier est exécuté directement.
if __name__ == '__main__':
    app.run(debug=True, port=5000)