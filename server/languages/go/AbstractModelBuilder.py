import fnmatch
import logging
import os
import tempfile
from pathlib import Path

import docker
from docker.errors import ContainerError

from ..ModelBuilder import ModelBuilder, Model

class _AbstractModelBuilder(ModelBuilder):
    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def build(self, code: str) -> str:
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
                    command=f'main.go --{self.model.value} -o {self.model.value}.dot',
                    working_dir='/tmp', remove=True,
                    volumes=[f'{Path(dir)}:/tmp']
                )
            except ContainerError as e:
                logging.warn(e)
                raise RuntimeError('Something wrong')

            # Ищу в папке сгенерированный граф
            files = fnmatch.filter(os.listdir(dir), f'{self.model.value}.dot')
            # Если графа нет, то что-то произошло не так
            if len(files) < 1:
                raise RuntimeError('Something wrong')
            else:
                # Чтение .dot графа из файла
                with open(Path(dir) / f'{self.model.value}.dot', 'r') as f:
                    return f.read()