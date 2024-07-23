function current-projects-month
        set month (date +%Y-%m)
        mkdir -p ~/Projects/Months/$month
        ln -nsf Months/$month ~/Projects/Current
        cd ~/Projects/Current
        echo Months/$month
end
