import docker
from docker.errors import ContainerError
import tempfile
import os
from pathlib import Path
import fnmatch

from ..ModelBuilder import ModelBuilder, Model


class _AbstractModelBuilder(ModelBuilder):
    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def build(self, code: str) -> str:
        # Клиент докера для создания контейнеров
        client = docker.from_env()
        # Создаю временную папку, которая удалится после выполнения функции
        with tempfile.TemporaryDirectory() as dir:
            # print(dir)
            # Имя исходного файла
            name = Path(dir) / 'main.c'
            # Записываю код
            with open(name, 'w') as file:
                file.write(code)
            try:
                # Пытаюсь запустить контейнер с установленным gcc, дополнительно соединяю контейнер с временной папкой с
                # исходным файлом
                client.containers.run(
                    'gcc:12', command=f"gcc -fdump-tree-{self.model.value}-graph main.c",
                    working_dir='/src', volumes=[f"{dir}:/src"], remove=True)
            except ContainerError as e:
                # Тут можно поймать ошибку gcc, например если программа введена неверно
                raise RuntimeError(e.stderr)
            # Ищу в папке сгенерированный граф
            files = fnmatch.filter(os.listdir(dir), f'*{self.model.value}.dot')
            # Если графа нет, то что-то произошло не так
            if len(files) < 1:
                raise RuntimeError('Something wrong')
            else:
                # Чтение .dot графа из файла
                with open(Path(dir) / files[0], 'r') as f:
                    return f.read()
