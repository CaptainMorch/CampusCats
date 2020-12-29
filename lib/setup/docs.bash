# Define doc strings

# shellcheck disable=2034    # all refered in main file
doc_welcome=
doc_usage=
doc_container_exists=
doc_all_done=


# Read a heredoc, wrap with newline, and store to doc_name
# Usage: 
#   $ set_doc doc_name <<'EOF'
#   > multi-line
#   > doc
#   > EOF
set_doc() {
    IFS='' read -r -d '' "$1" || true
    printf -v "$1" '\n%s\n' "${!1}"
}


set_doc doc_welcome <<'EOF'
              /^--^\     /^--^\     /^--^\ 
              \____/     \____/     \____/ 
             /      \   /      \   /      \ 
            |        | |        | |        | 
             \__  __/   \__  __/   \__  __/ 
|^|^|^|^|^|^|^|^\ \ |^|^|^/ /^|^|^|^|^\ \^|^|^|^|^|^|^|^|
| | | | | | | | |\ \| | |/ /| | | | | |\ \| | | | | | | |
| | | | | | | | |/ /| | |\ \| | | | | |/ /| | | | | | | |
| | | | | | | | |\/ | | | \/| | | | | |\/ | | | | | | | |
#########################################################
| | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | |

Welcome to CampusCats, an opensource web project
    for better lives of cats living in our campus!

Visit https://github.com/CaptainMorch/CampusCats
    for more infomations, reporting issues, 
    contributing or making suggestions.
EOF


set_doc doc_usage <<'EOF'
setup.sh [OPTION]...

This is the setup script for initializing the server for the
first time. DO NOT run this when project already exists.

Options:
    -h, --help             Print this message and exit
    -t, --test             Run tests before quit
    --no-superuser         Do not create a superuser interactively
EOF


set_doc doc_container_exists <<'EOF'
You may have initialized the docker service already!
This script is NOT for starting the server, and may 
CONFILCT with or even DAMAGE the existed one!

If you modified the code and want to rebuild and start, just run 
    'docker-compose up --build'
If you want to restart from scratch, remove the old one first:
    'docker-compose down'    # use -v if want to remove volumes also
EOF


set_doc doc_all_done <<'EOF'
All Done! Now the server sould be running in the background.
You can now open your browser, and enter 'localhost' to view it!

Click below to see what to do next:
https://github.com/CaptainMorch/CampusCats/blob/main/doc/manage.md

NOTE:
  This script has finished its duty and SHOULD NOT be excuted again!
EOF