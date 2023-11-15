import fnmatch
import logging
import os
import tempfile
from pathlib import Path

import docker
from docker.errors import ContainerError

# Доступные модели
MODELS = ['ast', 'cfg']


def make(code: str, model='ast'):
    if model not in MODELS:
        raise RuntimeError(f"There only {' '.join(MODELS)} models available")
    # Клиент докера для создания контейнеров
    #client = docker.from_env()
    # Создаю временную папку, которая удалится после выполнения функции
    with tempfile.TemporaryDirectory() as dir:
        # print(dir)
        # Имя исходного файла
        name = Path(dir) / 'main.go'
        # Записываю код
        with open(name, 'w') as file:
            file.write(code)

        client = docker.from_env()

        try:
            client.containers.run(
                'nikiens/st-dot',
                command=f'main.go --{model} -o {model}.dot',
                working_dir='/tmp', remove=True,
                volumes=[f'{Path(dir)}:/tmp']
            )
        except ContainerError as e:
            logging.warn(e)
            raise RuntimeError('Something wrong')

        # Ищу в папке сгенерированный граф
        files = fnmatch.filter(os.listdir(dir), f'{model}.dot')
        # Если графа нет, то что-то произошло не так
        if len(files) < 1:
            raise RuntimeError('Something wrong')
        else:
            # Чтение .dot графа из файла
            with open(Path(dir) / f'{model}.dot', 'r') as f:
                return f.read()