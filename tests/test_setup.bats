#!/usr/bin/env bats
#
# Need bats-core installed
# https://github.com/bats-core/bats-core
# A FULLY CONFIGURATED project is required to run tests


# Check dir

# Whether in project root dir
in_prj_root() {
    [[ -f ./docker-compose.yaml && -d ./campuscats ]]
}

# If in 'tests/', cd into project root
if ( cd ../; in_prj_root; ); then
    cd ../
fi
# Exit instantly if in the wrong dir
in_prj_root || {
    echo "# ERROR: Must in project root or 'tests' directory." >&3
    exit 1
    }

# shellcheck source=../bin/setup
source ./bin/setup    # 'load' may handle relative path again


#
# Set hooks
#

# Set backup dir. Only called before first 'setup'
setup_file() {
    bak="./.bats-backup-${RANDOM}"
    export bak

    mkdir "${bak}"
}


# Restore. Only called after last 'teardown'
teardown_file() {
    rm -r "${bak:?}"
}


# Testcase clenup. Called after every case
teardown() {
    cp -r --remove-destination "${bak:?}"/* .	# restore backup files
    rm -rf "${bak:?}"/*
}


#
# Unit tests
#

# set_doc

@test "check_set_doc" {
    doc_test=
    set_doc doc_test <<'EOF'
    test
test
EOF
    [[ "${doc_test}" == $'\n    test\ntest\n\n' ]]
}


# check_docker

@test "check_docker: pass" {
    check_docker
}

@test "check_docker: docker not installed" {
    (
        # pretend docker not installed
        # shellcheck disable=2123
        PATH=

        run check_docker

        [[ "${status}" -eq 1 ]]
        [[ "${output}" == *unavailable.\ Installed?* ]]
    )
}

@test "check_docker: can't reach docker" {
    docker-compose() {
        [[ "$1" == *v* ]]    # let 'docker-compose --version' survive
    }
    export -f docker-compose

    run check_docker

    [[ "${status}" -eq 1 ]]
    [[ "${output}" == *problem\ reaching\ docker* ]]
}

@test "check_docker: container exists" {
    docker-compose() { echo "something";}
    export -f docker-compose

    run check_docker

    [[ "${status}" -eq 1 ]]
    [[ "${output}" == *Container\ exists* ]]
}


# check_project_config

@test "check_project_config: pass" {
    check_project_config
}

@test "check_project_config: missing core settings" {
    mkdir "${bak:?}"/settings
    mv ./settings/local_settings.py "${bak}"/settings/

    run check_project_config

    [[ "${status}" -eq 1 ]]
    [[ "${output}" == *Project\ settings*not\ found* ]]
}

@test "check_project_config: missing .env file" {
    mkdir "${bak:?}"/settings
    mv ./settings/.env "${bak}"/settings/

    run check_project_config

    [[ "${status}" -eq 0 ]]
    [[ -f settings/.env ]]
    [[ "${output}" == *.env*not\ found* ]]
}

@test "check_project_config: missing password file" {
    mkdir "${bak:?}"/secrets
    mv ./secrets/mysql_password "${bak}"/secrets/

    run check_project_config

    [[ "${status}" -eq 1 ]]
    [[ "${output}" == *non-existent* ]]
}

@test "check_project_config: generate site_secret_key" {
    mkdir "${bak:?}"/secrets
    mv secrets/site_secret_key "${bak}"/secrets/ || true

    run check_project_config

    [[ "${status}" -eq 0 ]]
    [[ "${output}" == *generated*Write* ]]

    secret=$(<secrets/site_secret_key)
    (( ${#secret} ))
    printf '# Secret generated: %s\n' "${secret}" >&3
}


# wait_web_service

@test "check_wait_web_service: pass" {
    docker-compose() {
        if [[ "$1" == "exec" ]]; then
            eval "APP_HOME='.'" "${@:4}"
        fi
    }
    export -f docker-compose

    trap "rm ./.initialized" EXIT INT TERM
    { sleep 1; touch ./.initialized; } &
    run wait_web_service 2   # should block here for 1 sec

    # If ahead of bg job, i.e. fail, this eval to false
    [[ -f ./.initialized ]]

    [[ "${status}" -eq 0 ]]
    [[ "${output}" != *cleanup* ]]
    rm ./.initialized
}

@test "check_wait_web_service: timeout" {
    docker-compose() {
        [[ "$1" == "exec" ]] && false
    }
    export -f docker-compose

    test_wait_web_service() {
        run wait_web_service 1
        [[ "${status}" -eq 1 ]] \
        && [[ "${output}" == *Timeout*cleanup* ]]
    }

    TIMEFORMAT='%0R'    # as interger
    # https://unix.stackexchange.com/a/282391
    time_used=$( { time test_wait_web_service; } 2>&1 )

    # capture instantly timeout
    (( time_used >= 1 ))
}


# grant_privileges_to_test_db

@test "check_grant_privileges_to_test_db: pass" {
    mkdir "${bak:?}"/secrets
    mv ./secrets/mysql_root_password "${bak}"/secrets/
    echo "ugly  *'\password" > ./secrets/mysql_root_password

    # shellcheck disable=2016
    mysql() {
        [[ $2 == "root" ]] \
        && [[ $3 == "--password=ugly  *'\password" ]] \
        && [[ $4 == "-e" ]] \
        && [[ $5 == 'GRANT ALL ON `test\_cc\_db`.*'" TO 'user'@'%' ;" ]]
    }
    export -f mysql

    docker-compose() {
        if [[ "$1" == "exec" ]]; then
            inner_env="MYSQL_DATABASE=cc_db MYSQL_USER=user \
                MYSQL_ROOT_PASSWORD_FILE=./secrets/mysql_root_password"
            eval "${inner_env}" "${@:4}"
        fi
    }
    export -f docker-compose

    run grant_privileges_to_test_db

    [[ "${status}" -eq 0 ]]
    [[ -z "${output}" ]]
}

@test "check_grant_privileges_to_test_db: fail" {
    mysql() { false; }
    export -f mysql

    run grant_privileges_to_test_db

    [[ "${status}" -eq 1 ]]
    [[ "${output}" == *ERRO*to\ test\ database* ]]
}


# main

@test "main: wrong dir" {
    (   # cd in subshell otherwise 'teardown' makes a mess
        cd ../
        run bash ./campuscat/bin/setup
        [[ "${status}" -eq 1 ]]
        [[ "${output}" == *project\ root* ]]
    )

    (
        cd ./bin
        run bash setup
        [[ "${status}" -eq 1 ]]
        [[ "${output}" == *project\ root* ]]
    )
}


@test "check_main: set args" {
    docker-compose() { true; }
    export -f check_docker

    run main --test
    [[ "${status}" -eq 0 ]]
    [[ "${output}" == *site\ admin*Running\ tests* ]]

    run main --no-superuser
    [[ "${status}" -eq 0 ]]
    [[ "${output}" != *Running\ tests* ]]
    [[ "${output}" != *site\ admin* ]]

    # these call 'exit', so have to excute in 'run'
    run main --wrong
    [[ "${status}" -eq 1 ]]
    run main arg
    [[ "${status}" -eq 1 ]]
    run main -v
    [[ "${status}" -eq 1 ]]
}