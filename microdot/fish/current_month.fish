set _CURRENT_MONTH (date +%Y-%m)
set -x CURRENT_PROJECTS_MONTH $HOME/Projects/Months/$_CURRENT_MONTH
mkdir -p $CURRENT_PROJECTS_MONTH
ln -nsf Months/$_CURRENT_MONTH ~/Projects/Current

function current-projects-month
        cd $CURRENT_PROJECTS_MONTH
        echo $CURRENT_PROJECTS_MONTH
end
