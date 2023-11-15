import tempfile
from pathlib import Path

import docker

from ..ModelBuilder import ModelBuilder


class ASTModelBuilder(ModelBuilder):
    
    def build(self, code: str) -> str:
        with tempfile.TemporaryDirectory() as dir:
            name = Path(dir) / 'code.js'
            with open(name, 'w') as file:
                file.write(code)

            client = docker.from_env()

            return client.containers.run(
                "artmsd/js_ast",
                ["java", "-jar", "/home/compiler.jar", "--js", 'code/code.js', "--print_ast"],
                remove=True,
                working_dir='/home',
                volumes=[f'{Path(dir)}:/home/code']
            ).decode('utf-8')