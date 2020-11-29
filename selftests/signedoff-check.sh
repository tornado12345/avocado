#!/bin/sh -e

AUTHOR="$(git log --no-merges -1 --pretty='format:%aN <%aE>')"
git log --no-merges -1 --pretty=format:%B | grep "Signed-off-by: $AUTHOR"
if [ $? != 0 ]; then
    echo "The commit message does not contain author's signature (Signed-off-by: $AUTHOR)"
    exit 1
fi
