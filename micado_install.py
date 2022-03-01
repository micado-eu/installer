import click
import os
from python_on_whales import DockerClient
import requests
import subprocess
from dotenv import load_dotenv
from pathlib import Path
import time
import configparser



def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chown(folder, os.getuid(), os.getgid())
        print("Directory " , folder ,  " Created ")
    else:    
        print("Directory " , folder ,  " already exists") 

def create_env_file():
    file = Path('.env')
    file.touch(exist_ok=True)

def start_service(docker, service, service_name):
    docker.compose.up(
        services=[str(service)],
        detach=True,
        #compose_files['docker-compose-prod.yaml']
    )
    click.echo(f"Starting {service_name}")

def stop_service(docker, service):
    docker.compose.stop(
        services=[str(service)]
    )

def show_logs(docker, service):
    click.echo(docker.compose.logs(
        services=[str(service)]
    ))

def replace_in_git_ini_file(filename, group, key, value):
    with open(filename, 'r') as f:
        next(f)
        next(f)
        config = configparser.ConfigParser()
        config.optionxform = str
        config_string = f.read()
        config.read_string(config_string)
        config[str(group)][str(key)] = value
    with open(filename, 'w') as configfile:
      config.write(configfile)
    lines_to_add = "APP_NAME = Gitea: Git with a cup of tea\nRUN_MODE = dev\n\n"
    with open(filename, 'r+') as file:
      content = file.read()
      file.seek(0)
      file.write(lines_to_add + content)



#todo: add all the env variables necessary for deployment
@click.command()
@click.option("--micado_db_pwd", prompt="The password of the Micado database", help="The value of the password for the micado database", default="micado")
@click.option("--postgres_password", prompt="The password of the Postgres database", help="The value of the password for the micado database", default="micado")
@click.option("--kc_admin_pwd", prompt="The admin password of Keycloak ", help="The value of the password for the micado database", default="mypass1234")
@click.option("--pgadmin_deafult_password", prompt="The password of the pg_admin", help="The value of the password for the micado database", default="mypass1234")
@click.option("--weblate_admin_password", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="mypass1234")
@click.option("--keycloak_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="keycloak.micado.csi.it")
@click.option("--tz", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Europe/Rome")
@click.option("--micado_git_url", prompt="The admin password of Weblate", help="The value of the password for the micado database", default='http://git')
@click.option("--postgres_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micado")
@click.option("--postgres_db", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micado")
@click.option("--postgres_port", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="5432")
@click.option("--micado_db_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micadoapp")
@click.option("--micado_db_schema", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micadoapp")
@click.option("--keycloak_db_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="keycloak")
@click.option("--keycloak_db_pwd", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="keycloak")
@click.option("--keycloak_db_schema", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="keycloak")
@click.option("--keycloak_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="admin")
@click.option("--keycloak_password", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--gitea_db_schema", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--gitea_username", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="admin")
@click.option("--gitea_password", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--gitea_email", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="mail@csi.it")
@click.option("--migrants_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="migrants.micadoproject.eu")
@click.option("--pa_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="pa.micadoproject.eu")
@click.option("--ngo_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="ngo.micadoproject.eu")
@click.option("--db_admin_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="admin.micadoproject.eu")
@click.option("--analytic_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="monitoring.micadoproject.eu")
@click.option("--translation_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="translate.micadoproject.eu")
@click.option("--git_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="git.micadoproject.eu")
@click.option("--portainer_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="portainer.micadoproject.eu")
@click.option("--rocketchat_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="admin2.micadoproject.eu")
@click.option("--rasa_hostname", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="multichatbot")
@click.option("--pgadmin_default_email", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micado@csi.it")
@click.option("--mongo_replica_set_name", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="rs0")
@click.option("--weblate_debug", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="1")
@click.option("--weblate_loglevel", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="debug")
@click.option("--weblate_site_title", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="weblate.micadoproject.eu")
@click.option("--weblate_admin_name", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micadotransl")
@click.option("--weblate_admin_email", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="development@micadoproject.eu")
@click.option("--weblate_server_email", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="development@micadoproject.eu")
@click.option("--weblate_default_from_email", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="development@micadoproject.eu")
@click.option("--weblate_allowed_hosts", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="*")
@click.option("--weblate_registration_open", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="1")
def main( micado_db_pwd, postgres_password, kc_admin_pwd, pgadmin_deafult_password, weblate_admin_password, keycloak_hostname, tz, micado_git_url,
 postgres_user, postgres_db, postgres_port,micado_db_user, micado_db_schema, keycloak_db_user, keycloak_db_pwd ,keycloak_db_schema, keycloak_user, keycloak_password,
 gitea_db_schema, gitea_username, gitea_password,gitea_email, migrants_hostname, pa_hostname, ngo_hostname, db_admin_hostname, analytic_hostname, translation_hostname,
 git_hostname, portainer_hostname, rocketchat_hostname, rasa_hostname, weblate_debug, weblate_loglevel, weblate_site_title, weblate_admin_name, weblate_admin_email,
 weblate_server_email, weblate_default_from_email, weblate_allowed_hosts, weblate_registration_open ):
    """MICADO installer program"""

    #creating file and adding env variables
    create_env_file()
    f = open(".env", "a")
    f.write(f"MICADO_DB_PWD={micado_db_pwd}\n")
    f.write('POSTGRES_PASSWORD=' + postgres_password + '\n')
    f.write('KC_ADMIN_PWD=' + kc_admin_pwd + '\n')
    f.write('PGADMIN_DEFAULT_PASSWORD=' + pgadmin_deafult_password + '\n')
    f.write('WEBLATE_ADMIN_PASSWORD=' + weblate_admin_password + '\n')
    f.write('KEYCLOAK_HOSTNAME=' + keycloak_hostname + '\n')
    f.write('TZ=' + tz + '\n')
    f.write('MICADO_GIT_URL=' + micado_git_url + '\n')
    f.write('POSTGRES_USER=' + postgres_user + '\n')
    f.write('POSTGRES_DB=' + postgres_db + '\n')
    f.write('POSTGRES_PORT=' + postgres_port + '\n')
    f.write('MICADO_DB_USER=' + micado_db_user + '\n')
    f.write('MICADO_DB_SCHEMA=' + micado_db_schema + '\n')
    f.write('KEYCLOAK_DB_USER=' + keycloak_db_user + '\n')
    f.write('KEYCLOAK_DB_PWD=' + keycloak_db_pwd + '\n')
    f.write('KEYCLOAK_DB_SCHEMA=' + keycloak_db_schema + '\n')
    f.write('KEYCLOAK_USER=' + keycloak_user + '\n')
    f.write('KEYCLOAK_PASSWORD=' + keycloak_password + '\n')
    f.write('GITEA_DB_SCHEMA=' + gitea_db_schema + '\n')
    f.write('GITEA_USERNAME=' + gitea_username + '\n')
    f.write('GITEA_PASSWORD=' + gitea_password + '\n')
    f.write('GITEA_EMAIL=' + gitea_email + '\n')
    f.write('MIGRANTS_HOSTNAME=' + migrants_hostname + '\n')
    f.write('PA_HOSTNAME=' + pa_hostname + '\n')
    f.write('NGO_HOSTNAME=' + ngo_hostname + '\n')
    f.write('PGADMIN_DEFAULT_EMAIL=' + pgadmin_default_email + '\n')
    f.write('MONGO_REPLICA_SET_NAME=' + mongo_replica_set_name + '\n')
    f.write('DB_ADMIN_HOSTNAME=' + db_admin_hostname + '\n')
    f.write('ANALYTIC_HOSTNAME=' + analytic_hostname + '\n')
    f.write('TRANSLATION_HOSTNAME=' + translation_hostname + '\n')
    f.write('GIT_HOSTNAME=' + git_hostname + '\n')
    f.write('PORTAINER_HOSTNAME=' + portainer_hostname + '\n')
    f.write('ROCKETCHAT_HOSTNAME=' + rocketchat_hostname + '\n')
    f.write('RASA_HOSTNAME=' +multichatbot + '\n')
    f.write('WEBLATE_DEBUG=' + weblate_debug + '\n')
    f.write('WEBLATE_LOGLEVEL=' + weblate_loglevel + '\n')
    f.write('WEBLATE_SITE_TITLE=' + weblate_site_title + '\n')
    f.write('WEBLATE_ADMIN_NAME=' + weblate_admin_name + '\n')
    f.write('WEBLATE_ADMIN_EMAIL=' + weblate_admin_email + '\n')
    f.write('WEBLATE_SERVER_EMAIL=' + weblate_server_email + '\n')
    f.write('WEBLATE_DEFAULT_FROM_EMAIL=' + weblate_default_from_email + '\n')
    f.write('WEBLATE_ALLOWED_HOSTS=' + weblate_allowed_hosts + '\n')
    f.write)'WEBLATE_REGISTRATION_OPEN=' + weblate_registration_open + '\n')

    f.close

    #creating necessary folder
    click.echo("\nCreating folders\n")
    folder_list=["db_data", "weblate_data", "redis_data", "identity-server_data/deployment", "identity-server_data/tenants", "shared_images", 'git_data']
    [create_folder(i) for i in folder_list]

    #setting up docker client with env variables
    click.echo("\nSetting environment\n")
    docker = DockerClient(
        compose_env_file='./.env',
    )
    #setting env variables
    load_dotenv()

    #starting database
    click.echo("\nStarting PostgreSQL container deployment\n")
    start_service(docker, 'micado_db', 'micado database')

    #checking if db is up
    click.echo("\nWaiting for PostgreSQL to start\n")
    check_db = -1
    word = 'accepting'
    while(check_db == -1):
        bash_for_db = 'docker-compose exec micado_db pg_isready'
        process=subprocess.Popen(bash_for_db.split(" "), stdout=subprocess.PIPE)
        db_data = str(process.communicate()[0])
        if(word in db_data):
            check_db = 1
            click.echo("Db ready")
        else:
            check_db = -1
            click.echo("Db not ready")
    show_logs(docker, 'micado_db')
    click.echo("\nStarted PostgreSQL\n")


    #starting mongo and replica
    click.echo("\nStarting MongoDB container deployment\n")
    start_service(docker, 'mongo_db', 'mongo database')
    time.sleep(15)
    start_service(docker, 'mongo-init-replica', 'mongo replica')
    time.sleep(15)
    echo.click("\nStarted MongoDB\n")
    time.sleep(25)

    #starting balancer
    click.echo("\nStarting Balancer container deployment\n")
    start_service('balancer', 'balancer')
    time.sleep(15)

    #starting and setting up git and weblate
    click.echo("\nStarting WEBLATE containers deployment\n")
    start_service(docker, 'cache', 'git cache')
    time.sleep(15)
    start_service(docker,'git', 'git')
    time.sleep(15)
    stop_service(docker, 'git')
    click.echo("\nAdding SCHEMA to git_data/gitea/conf/app.ini\n")
    replace_in_git_ini_file('git_data/gitea/conf/app.ini','database', 'SCHEMA', gitea_db_schema)
    time.sleep(5)
    start_service(docker, 'git', 'git')
    time.sleep(15)
    gitea_migrate = 'docker-compose exec git gitea migrate'
    process=subprocess.Popen(gitea_migrate.split(" "), stdout=subprocess.PIPE)
    gitea_create_user='docker-compose exec git gitea admin create-user --username ' + gitea_username + ' --password ' + gitea_password + ' --email ' + gitea_email + ' --admin'
    process=subprocess.Popen(gitea_create_user.split(" "), stdout=subprocess.PIPE)
    stop_service(docker, 'git')
    time.sleep(5)
    click.echo("\nSetting INSTALL_LOCK=true to git_data/gitea/conf/app.ini\n")
    replace_in_git_ini_file('git_data/gitea/conf/app.ini','security', 'INSTALL_LOCK', 'true')
    start_service(docker, 'git', 'git')
    time.sleep(15)
    #todo: add create gitea repo
    #todo: add git hook on push

    #starting weblate
    start_service(docker, 'weblate', weblate)
    time.sleep(25)
    show_logs(docker, 'weblate')
    click.echo("\nStarted WEBLATE\n")

    if click.confirm('Weblate is running, now you need to configure GIT before installation can continue, press y after you configured it'):
        click.echo("Continuing installation")
    
    #starting backend
    click.echo("\nStarting backend container deployment\n")
    start_service(docker,'backend', 'backend')
    time.sleep(15)
    show_logs(docker, 'backend')
    click.echo("\nStarted backend\n")

    #starting countly
    click.echo("\nStarting Countly containers deployment\n")
    start_service(docker, 'countly_api', 'countly api')
    time.sleep(25)
    start_service(docker, 'countly_frontend', 'countly frontend')
    time.sleep(25)
    show_logs(docker, 'countly_frontend')
    click.echo("\nStarted Countly")

    #starting nginx
    click.echo("\nStarting NGINX containers deployment\n")
    start_service(docker,'frontend', 'nginx')
    time.sleep(15)
    show_logs(docker, 'nginx')
    click.echo("\nStarted NGINX")

    #starting keycloak
    click.echo("\nStarting Keycloak containers deployment\n")
    start_service(docker,'keycloak', 'keycloak')
    time.sleep(15)
    show_logs(docker, 'keycloak')
    click.echo("\nStarted Keycloak")

    #starting rasa chatbot
    click.echo("\nStarting Chatbot containers deployment\n")
    start_service(docker,'action_server', 'action server')
    time.sleep(15)
    start_service(docker,'duckling_server', 'duckling server')
    time.sleep(15)
    start_service(docker,'chatbot_en', 'chatbot')
    time.sleep(25)
    show_logs(docker, 'chatbot_en')
    click.echo("\nStarted Chatbot")

    #starting rocketchat
    click.echo("\nStarting Rocketchat containers deployment\n")
    start_service(docker,'rocketchat', 'rocketchat')
    time.sleep(15)
    show_logs(docker, 'rocketchat')
    click.echo("\nStarted Keycloak")

    #todo:configure rocketchat

    #starting the apps
    click.echo("\nStarting MICADO applications' containers deployment")
    start_service(docker, 'data_migrant', 'migrant application')
    start_service(docker, 'data_pa', 'pa application')
    start_service(docker, 'data_ngo', 'cso application')
    
    click.echo("\nIf you need to monitor your deployment you can use portainer included in the deployment with the following command:\n")
    click.echo("\n(set -a; source prod.env; set +a; docker-compose -f docker-compose-prod.yaml up -d portainer)\n")
    click.echo("\nIf you need to access the DB you can start the pgadmin service with the following command:\n")
    click.echo("\n(set -a; source prod.env; set +a; docker-compose -f docker-compose-prod.yaml up -d db_admin)\n")




if __name__ == '__main__':
    click.echo("\nCreating .env file. If you didn't set the variables with the flags, you will be asked to enter them. Just press enter to use the default written between square brackets")
    main()