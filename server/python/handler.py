from server.python import python_ast, python_cfg


def handler(code: str, model: str):
    if model == 'ast':
        return python_ast.make(code, format='dot')
    elif model == 'cfg':
        return python_cfg.make(code)
    pass
