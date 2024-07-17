function create-current-documents-month
        set month (date +%Y-%m)
        mkdir -p ~/Projects/Months/$month
        ln -nsf Months/$month ~/Projects/Current
        cd ~/Projects/Current
end
