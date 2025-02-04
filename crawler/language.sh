#!/usr/bin/env bash
set -eou pipefail

log_fatal() {
    local msg
    msg="$1"

    printf "%s\n" "$msg" >&2
    exit 1
}

log_error_to_file() {
    local msg
    msg="$1"
    local file
    file="$2"

    printf "%s\n" "$msg" >>"$file"
}

assert_command() {
    local cmd
    cmd="$1"
    local err_msg
    err_msg="$2"

    if ! command -v "$cmd" >/dev/null 2>&1; then
        log_fatal "$err_msg"
    fi
}

clean_up() {
    local dir
    dir="$1"

    rm -r "$dir"
}

main() {
    local directory="repo"
    local input="urls.txt"
    local error_log="error.log"
    local out="languages"

    assert_command "tr" "\`tr\` must be installed"
    assert_command "git" "\`git\` must be installed"
    assert_command "github-linguist" "\`github-linguist\` must be installed"

    if [ ! -f "$input" ]; then
        log_fatal "cannot find file: $input"
    fi

    mkdir -p "$out"

    while read -r url; do
        if [ -z "$url" ]; then continue; fi
        IFS="/" read -ra components <<<"$url"

        local file_name="${components[${#components[@]} - 2]}---${components[${#components[@]} - 1]}"
        if ! git clone "$url" "$directory"; then
            log_error_to_file "$url" "$error_log"
            continue
        fi

        (
            cd "$directory"
            local path="../$out/$file_name.json"
            github-linguist --json >"$path"
        )
        clean_up "$directory"
    done < <(tr -d "\r" <"$input")
}

main "$@"
