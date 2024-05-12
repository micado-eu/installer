# MICADO installer

## Image preparation
In case of the need to use new python libraries is necessary to create a new development library
```
docker build -t micadoproject/installer .
```

## Development
This is the command to execute to run the installer in development
```
docker run -v $PWD:/usr/src/app -it --rm  --user <user> micadoproject/installer python micado_install.py
```

```
docker run -v $PWD:/usr/src/app -v /var/run/docker.sock:/var/run/docker.sock -it --rm  python:3.9.10 /bin/bash
cd /usr/src/app
pip3 install -r requirements.txt
python micado_install.py prepare prepare
```
```
git push origin refs/heads/2024:refs/heads/2024
```