from typing import Tuple

class Router:
    def __init__(self, command_prefix, routes=None, fallback=None):
        self.command_prefix = command_prefix
        self.routes = routes or []
        self.fallback_fn = fallback or None
        self.descriptions = {}

    def route(self, *paths: Tuple[str]):
        def decorator(fn):
            new_route = sorted(paths, reverse=True), fn
            self.routes.append(new_route)
            return fn
        return decorator

    def fallback(self, fn):
        self.fallback_fn = fn
        return fn

    def is_command(self, text: str):
        return text.startswith(self.command_prefix)

    def resolve(self, text: str):
        if not self.is_command(text):
            raise ValueError("'this' is not a command")

        for prefixes, result in self.routes:
            for prefix in prefixes:
                full_prefix = self.command_prefix + prefix
                if text.startswith(full_prefix):
                    return result, full_prefix

        return (self.fallback_fn, self.command_prefix) if self.fallback_fn else None

    def description(self, text: str):
        def decorator(fn):
            self.descriptions[fn] = text
            return fn
        return decorator
            
    def generate_help(self):
        PREFIX = 'List of documented commands:'
        lines = [PREFIX]
        for prefixes, fn in sorted(self.routes):
            line = ' ' * 4 + f'{"/".join(self.command_prefix + x for x in prefixes)} - {self.descriptions[fn]}'
            lines.append(' ' * 4 + line)
        return '\n'.join(lines)