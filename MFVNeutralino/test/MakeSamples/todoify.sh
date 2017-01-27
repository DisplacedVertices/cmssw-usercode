#!/bin/bash

infn=$1
if [[ ! -e $infn ]]; then
    echo no input file $infn
    exit 1
fi

cat <<EOF
import sys
todo, todo_args = None, []
for arg in sys.argv:
    if arg.startswith('todo='):
        todo = arg.replace('todo=', '')
        if ',' in todo:
            todo, todo_args_ex = todo.split(',', 1)
            for x in todo_args_ex.split(','):
                try:
                    x = eval(x)
                except NameError:
                    pass
                todo_args.append(x)

################################################################################
EOF

cat $infn

cat <<EOF
################################################################################

if todo is not None:
    import modify
    getattr(modify, 'set_' + todo)(process, *todo_args)
EOF
