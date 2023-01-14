function last_history_item
        echo $history[1]
end

function last_history_word
        string split ' ' --right --max 1 --fields 2 $history[1]
end

abbr -a '!!' --position anywhere --function last_history_item
abbr -a '!#' --position anywhere --function last_history_word
