FROM jupyter/scipy-notebook:6399d2faf16f

USER root
RUN apt-get update
RUN apt-get install -y curl

USER jovyan
ADD python-package-requirement.txt /home/jovyan/work/python-package-requirement.txt
ADD install-parser.sh /home/jovyan/work/install-parser.sh
ADD set_env.sh /home/jovyan/work/set_env.sh
ADD run.sh /home/jovyan/work/run.sh

RUN pip install --requirement python-package-requirement.txt
RUN jupyter nbextension enable --py widgetsnbextension --sys-prefix
RUN ./install-parser.sh

# Launchbot labels
LABEL name.launchbot.io="snorkel"
LABEL workdir.launchbot.io="/usr/workdir"
LABEL 8888.port.launchbot.io="Jupyter Notebook"

# Set the working directory
WORKDIR /usr/workdir

# Expose the notebook port
EXPOSE 8888

# Start the notebook server
CMD ["/home/jovyan/work/run.sh"]
