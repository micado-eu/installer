# MICADO installer

##Image preparation
In case of the need to use new python libraries is necessary to create a new development library
```
docker build -t micadoproject/installer .
```

#Development
This is the command to execute to run the installer in development
```
docker run -v $PWD:/usr/src/app -it --rm micadoproject/installer python micado_install.py
```
