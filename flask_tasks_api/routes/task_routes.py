# Définition des routes de l'API : chaque URL est associée à une fonction du contrôleur.
from flask import Blueprint
from controllers.task_controllers import (
    get_all_tasks,
    create_task,
    get_specific_task,
    modify_task,
    delete_task,
)


# Blueprint regroupant toutes les routes liées aux tâches.
task_bp = Blueprint('tasks', __name__)


@task_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """GET /api/tasks : récupère la liste de toutes les tâches."""
    return get_all_tasks()


@task_bp.route('/api/tasks', methods=['POST'])
def post_task():
    """POST /api/tasks : crée une nouvelle tâche."""
    return create_task()


@task_bp.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    """GET /api/tasks/<id> : récupère une tâche précise par son identifiant."""
    return get_specific_task(id)


@task_bp.route('/api/tasks/<int:id>', methods=['PUT'])
def modification(id):
    """PUT /api/tasks/<id> : modifie une tâche existante."""
    return modify_task(id)


@task_bp.route('/api/tasks/<int:id>', methods=['DELETE'])
def deletion(id):
    """DELETE /api/tasks/<id> : supprime une tâche."""
    return delete_task(id)
