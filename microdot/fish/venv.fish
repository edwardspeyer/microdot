#
# Store all UV .venvs in ~/tmp to avoid including them in backups.
#
function update_uv_env --on-variable PWD
    function get_py_root
        set cur $PWD
        while test "$cur" != /
            if test -f "$cur/pyproject.toml"
                echo $cur
                return
            end
            set cur (dirname $cur)
        end
        return 1
    end

    if ! get_py_root
        set -e UV_PROJECT_ENVIRONMENT
        return
    end

    set key (string replace -a / - -- (get_py_root))
    set key (string sub --start 2 -- $key)
    set -gx UV_PROJECT_ENVIRONMENT "$HOME/.cache/venvs/$key"
end
