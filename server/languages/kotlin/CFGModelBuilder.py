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
            name = 'Main.kt'
            abs_name = Path(dir) / name
            package = get_package(code)
            with open(abs_name, 'w') as file:
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

                container.exec_run(f'kotlinc {name} -d main.jar')
                container.exec_run(f'java -jar /usr/lib/kt_cfg-v0.jar {package}')

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


def get_package(code: str):
    clear_code = code.strip()
    pattern = re.compile('(?<=^(package ))\s*\S+(?=\s*\n)')
    res = re.search(pattern, clear_code)
    if not res:
        return ""
    else:
        return res.group(0).strip()
