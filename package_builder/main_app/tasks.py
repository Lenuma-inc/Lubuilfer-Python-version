from celery import shared_task, Task
from django.db import transaction
from .models import Build
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)

class BuildTask(Task):
    """Кастомная задача Celery с настройками повторных попыток и обработки ошибок."""
    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True
    retry_backoff_max = 60
    retry_jitter = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        build_id = args[0]
        build = Build.objects.get(id=build_id)
        build.status = 'Error'
        build.log = (build.log or '') + f'\nError: {str(exc)}'
        build.save()
        logger.error(f'Task {task_id} failed: {exc}')

@shared_task(bind=True, base=BuildTask)
def build_package(self, build_id):
    """Задача Celery для сборки пакета."""
    build = Build.objects.select_related('package').get(id=build_id)
    package = build.package
    build.status = 'Building'
    build.save()
    logger.info(f'Starting build {build_id} for package {package.name}')

    with tempfile.TemporaryDirectory() as repo_dir:
        try:
            with transaction.atomic():
                # Клонируем репозиторий
                subprocess.run(
                    ['git', 'clone', package.repository_url, repo_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Выполняем сборку (пример команды)
                result = subprocess.run(
                    ['make', 'build'],
                    cwd=repo_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Обновляем лог и статус сборки
                build.log = result.stdout + '\n' + result.stderr
                build.status = 'Success'
                build.save()
                logger.info(f'Build {build_id} succeeded')

        except subprocess.CalledProcessError as e:
            build.log = (e.stdout or '') + '\n' + (e.stderr or '')
            build.status = 'Failed'
            build.save()
            logger.error(f'Build {build_id} failed: {e}')
            raise e

        except Exception as e:
            build.log = (build.log or '') + f'\nUnexpected error: {str(e)}'
            build.status = 'Error'
            build.save()
            logger.error(f'Unexpected error in build {build_id}: {e}')
            raise e
