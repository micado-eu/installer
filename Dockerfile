FROM python:3.9.10

WORKDIR /usr/src/app

#RUN apt-get update
#RUN apt-get install -y apt-utils portaudio19-dev python3-pyaudio alsa-base alsa-utils
#RUN apt-get install -y libportaudio-dev python-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#COPY main.py ./

#CMD [ "python", "./main.py" ]
