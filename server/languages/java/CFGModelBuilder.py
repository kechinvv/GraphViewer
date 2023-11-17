import fnmatch
import os
import re
import tempfile
from pathlib import Path

import docker
from docker.errors import ContainerError

from ..ModelBuilder import ModelBuilder


class CFGModelBuilder(ModelBuilder):

    def build(self, code: str) -> str:
        client = docker.from_env()
        with tempfile.TemporaryDirectory() as dir:
            class_name = get_class(code)
            name = Path(dir) / f'{class_name}.java'
            with open(name, 'w') as file:
                file.write(code)
            try:
                container = client.containers.run(
                    'strgss/kt_with_jar',
                    working_dir='/src',
                    volumes=[f'{dir}:/src'],
                    command='/bin/sh',
                    tty=True,
                    detach=True
                )

                container.exec_run(f'javac {class_name}.java')
                container.exec_run(f'jar cvf main.jar {class_name}.class')
                container.exec_run('java -jar /usr/lib/kt_cfg-v0.jar')

                container.stop()
                container.remove()
            except ContainerError as e:
                raise RuntimeError(e.stderr)
            files = fnmatch.filter(os.listdir(dir), f'dot.txt')
            if len(files) < 1:
                raise RuntimeError('Something wrong')
            else:
                with open(Path(dir) / files[0], 'r') as f:
                    return f.read()


def get_class(code: str):
    clear_code = code.strip()
    pattern = re.compile('(?<=class )\s*[^\s{]+(?=\s*|\s*{)')
    res = re.search(pattern, clear_code)
    if not res:
        return ""
    else:
        return res.group(0).strip()
