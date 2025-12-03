aws-profile () {
        local AWS_PROFILES
        AWS_PROFILES=$(cat ~/.aws/credentials | sed -n -e 's/^\[\(.*\)\]/\1/p' | fzf)
        if [[ -n "$AWS_PROFILES" ]]
        then
                export AWS_PROFILE=$AWS_PROFILES
                echo "Selected profile: $AWS_PROFILES"
        else
                echo "No profile selected"
        fi
}
