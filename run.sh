# Set & move to home directory
#source set_env.sh
#cd "$SNORKELHOME"

# Make sure the submodules are installed
git submodule update --init --recursive

# Make sure parser is installed
PARSER="parser/stanford-corenlp-3.6.0.jar"
if [ ! -f "$PARSER" ]; then
    read -p "CoreNLP [default] parser not found- install now?   " yn
    case $yn in
        [Yy]* ) echo "Installing parser..."; ./install-parser.sh;;
        [Nn]* ) ;;
    esac
fi

export SNORKELHOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Snorkel home directory: $SNORKELHOME"
export PYTHONPATH="$PYTHONPATH:$SNORKELHOME:$SNORKELHOME/treedlib"
export PATH="$PATH:$SNORKELHOME:$SNORKELHOME/treedlib"
echo "Environment variables set!"

# Launch jupyter notebook!
echo "Launching Jupyter Notebook..."
jupyter notebook --no-browser --port 8888 --ip=*
