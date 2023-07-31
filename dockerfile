FROM python:latest

LABEL Maintainer="talanakombat_carolaine_borre"
COPY *.py ./
# Actualizacion de los 'sources' a la ultima version
RUN apt-get update
# Instalar los paquetes del sistema necesarios para python
RUN apt-get install -qy python3 \
                        python-dev-is-python3 \
                        python3-pip \
                        python3-setuptools \
                        build-essential

WORKDIR ${WEB_DIR}
COPY . ${WEB_DIR} 
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD [ "python", "./talanakombat.py"]