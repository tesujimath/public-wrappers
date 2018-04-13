# include public wrappers on path, where they exist
for env in `ls -r /stash/miniconda3/envs 2>/dev/null`; do
    test -d /stash/miniconda3/envs/$env/public-wrappers && {
        PATH=/stash/miniconda3/envs/$env/public-wrappers:$PATH
    }
done
export PATH
