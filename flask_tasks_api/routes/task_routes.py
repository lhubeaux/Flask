from flask import Blueprint
from controllers.task_controllers import (
    get_all_tasks,
    create_task,
    get_specific_task,
    modify_task,
    delete_task,
)


task_bp = Blueprint('tasks', __name__)

@task_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    return get_all_tasks()


@task_bp.route('/api/tasks', methods=['POST'])
def post_task():
    return create_task()


@task_bp.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    return get_specific_task(id)

@task_bp.route('/api/tasks/<int:id>', methods=['PUT'])
def modification(id):
    return modify_task(id)

@task_bp.route('/api/tasks/<int:id>', methods=['DELETE'])
def deletion(id):
    return delete_task(id)
