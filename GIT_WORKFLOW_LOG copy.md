# Git Workflow Log
My biggest mistake was having my files inside `static/` and `templates/` folders. This made my CSS not work, and the background stayed white. I fixed it by using the `mv` command to move everything to the main folder and updating my HTML link.
I used `git status` the most. It was the only way to make sure my files were "green" and ready before I committed them.
I found `git log --oneline` the most useful because it allowed me to track my progress and see exactly how many commits I had left to reach 10.
The most challenging part was remembering to `git add` before every `git commit`. At first, I kept trying to commit directly, and Git would tell me "nothing added to commit." I had to learn the "Add then Commit" rhythm.