#!/bin/bash

infn=$1
if [[ ! -e $infn ]]; then
    echo no input file $infn
    exit 1
fi

cat <<EOF
import sys
todos = []
for arg in sys.argv:
    if arg.startswith('todo='):
        todo = arg.replace('todo=', '')
        todo_args = []
        if ',' in todo:
            todo, todo_args_ex = todo.split(',', 1)
            for x in todo_args_ex.split(','):
                try:
                    x = eval(x)
                except NameError:
                    pass
                todo_args.append(x)
        todos.append((todo, todo_args))

################################################################################
EOF

cat $infn

cat <<EOF
################################################################################

if todos:
    import modify
    for todo, todo_args in todos:
        getattr(modify, 'set_' + todo)(process, *todo_args)
EOF
