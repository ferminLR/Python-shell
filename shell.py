import sys
import os
import re


def export(args):
    for spec in args[1:]:
        key, value = spec.split("=")
        os.environ[key] = value


BUILTINS = {
    "cd": lambda args: os.chdir(args[1]),
    "exit": lambda args: exit(0),
    "export": export
}


def expand_user(input):
    return [os.path.expanduser(s) for s in input]


def expand_env_var(s):
    return re.sub(
        "\$\((.*)\)",
        lambda m: os.environ[m.group(1)],
        s
    )


def expand_env_vars(input):
    return [expand_env_var(s) for s in input]


def process_input(input):
    user_expanded = expand_user(input)
    env_var_expanded = expand_env_vars(user_expanded)
    return env_var_expanded


def execute(program_or_builtin, args):
    if BUILTINS.get(program_or_builtin):
        BUILTINS[program_or_builtin](args)
    else:
        pid = os.fork()
        if pid == 0:
            os.execvp(program_or_builtin, args)
        else:
            os.waitpid(pid, 0)


def shell():
    while True:
        sys.stdout.write("$ ")
        input = raw_input()
        split_input = input.split()
        processed_input = process_input(split_input)
        execute(processed_input[0], processed_input)


if __name__ == "__main__":
    shell()