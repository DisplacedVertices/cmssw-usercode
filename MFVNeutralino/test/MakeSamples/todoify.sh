#!/bin/bash

infn=$1
if [[ ! -e $infn ]]; then
    echo no input file $infn
    exit 1
fi

cat <<EOF
import sys
todo, todo_args = None, None
for arg in sys.argv:
    if arg.startswith('todo='):
        arg = arg.replace('todo=', '')
        todo, todo_args = arg.split(',', 1)
        y = []
        for x in todo_args.split(','):
            try:
                x = eval(x)
            except NameError:
                pass
            y.append(x)
        todo_args = y

################################################################################
EOF

cat $infn

cat <<EOF
################################################################################

if todo is not None:
    import modify
    getattr(modify, 'set_' + todo)(process, *todo_args)
EOF
