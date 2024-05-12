import fileops
import checks
import git
# from python_on_whales import DockerClient
import requests
import subprocess
from dotenv import load_dotenv
from pathlib import Path
import time
import configparser
from hashlib import sha256
from typing_extensions import Annotated
from password_validator import PasswordValidator
import typer
from rich import print
import prepare

app = typer.Typer()

app = typer.Typer()
app.add_typer(prepare.app, name="prepare")
#app.add_typer(items.app, name="items")




 
def pwd_callback(value: str):
    print("Validating password")
    schema = PasswordValidator()
    schema.min(6).max(10).has().uppercase().has().lowercase().has().digits().has().no().spaces()
    validation = schema.validate(value)
    print(f"Validation was : {validation}")
    if not validation:
        raise typer.BadParameter("Only Camila is allowed")
    return value



 #   folder_list=["db_data", "weblate_data", "redis_data", "identity-server_data/deployment", "identity-server_data/tenants", "shared_images"]
 #   [fileops.create_folder(i) for i in folder_list]

    #create_folder("db_data")
    #create_folder("weblate_data")
    #create_folder("redis_data")
    #create_folder("identity-server_data/deployment")
    #create_folder("identity-server_data/tenants")
    #create_folder("shared_images")
    #create_folder("git_data")



@app.command()
def deploy(count, name):
    """MICADO installer program"""
    print("Deploying MICADO application")
    for _ in range(count):
        click.echo(f"Hello, {name}!")

    folder_list=["db_data", "weblate_data", "redis_data", "identity-server_data/deployment", "identity-server_data/tenants", "shared_images", "translations_dir"]
    [create_folder(i) for i in folder_list]

@app.command()
def configure(
    db_password: Annotated[
        str, typer.Option(
            prompt="Insert the password for the database",
            help="This is the root password for the MICADO database",
            hide_input=True,
        ),
    ],
    micado_password: Annotated[
        str, typer.Option(
            prompt="Insert the password for the MICADO application",
            help="This is the password for the MICADO application",
            hide_input=True,
            callback=pwd_callback,
        ),
    ],
):
    print("Configuring MICADO application")
    print(f"You choose for the DB password: {db_password}")
    print(f"You choose for the MICADO password: {micado_password}")

    if not checks.check_prepared():
        print("MICADO is not prepared, you must execute the [bold green]prepare[/bold green] command first")
        return


if __name__ == '__main__':
    app()


""" 

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
@click.option("--weblate_email_host", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="smtp.micadoproject.eu")
@click.option("--weblate_email_host_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="development@micadoproject.eu")
@click.option("--weblate_email_host_ssl", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="false")
@click.option("--gitea_db_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="gitea")
@click.option("--micado_translations_dir", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="/tmp/translations")
@click.option("--micado_translations_dir", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="/tmp/translations")
@click.option("--micado_env", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="prod")
@click.option("--rocketchat_admin", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="admin")
@click.option("--rocketchat_admin_mail", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="test@test.it")
@click.option("--algorithm", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="aes-192-cbc")
@click.option("--salt", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="salt")
@click.option("--key_length", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="24")
@click.option("--buffer_0", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="16")
@click.option("--buffer_1", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="0")
@click.option("--countly_admin", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micadoadm")
@click.option("--micado_weblate_project", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micado")
@click.option("--rasa_schema", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="rasa")
@click.option("--rasa_db_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="rasa")
@click.option("--bot_name", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="rasa_bot")
@click.option("--title_limit", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="30")
@click.option("--weblate_postgres_password", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--weblate_email_host_password", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--gitea_db_pwd", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--rocketchat_admin_pwd", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="Pa55w0rd")
@click.option("--rocketchat_user", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="rasa_bot")
@click.option("--rocketchat_password", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="micadobot")
@click.option("--respond_to_livechat", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="true")
@click.option("--weblate_registration_open", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="true")
@click.option("--rasa_bot", prompt="The admin password of Weblate", help="The value of the password for the micado database", default="rasa_bot")

def main( micado_db_pwd, postgres_password, kc_admin_pwd, pgadmin_deaf    "
rocketchat_admin_mail,algorithm,salt,key_length,buffer_0,buffer_1,
 countly_admin, micado_weblate_project,rasa_bot, rasa_db_user, rasa_schema, bot_name, title_limit, weblate_postgres_password, weblate_email_host_password,
 gitea_db_pwd, rocketchat_admin_pwd, rocketchat_user, rocketchat_password, respond_to_livechat,pgadmin_default_email , mongo_replica_set_name):

    #creating file and adding env variables
    create_file('./.env')
    with open('./.env', 'a') as f:
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
        f.write('RASA_HOSTNAME=' +rasa_hostname + '\n')
        f.write('WEBLATE_DEBUG=' + weblate_debug + '\n')
        f.write('WEBLATE_LOGLEVEL=' + weblate_loglevel + '\n')
        f.write('WEBLATE_SITE_TITLE=' + weblate_site_title + '\n')
        f.write('WEBLATE_ADMIN_NAME=' + weblate_admin_name + '\n')
        f.write('WEBLATE_ADMIN_EMAIL=' + weblate_admin_email + '\n')
        f.write('WEBLATE_SERVER_EMAIL=' + weblate_server_email + '\n')
        f.write('WEBLATE_DEFAULT_FROM_EMAIL=' + weblate_default_from_email + '\n')
        f.write('WEBLATE_ALLOWED_HOSTS=' + weblate_allowed_hosts + '\n')
        f.write('WEBLATE_REGISTRATION_OPEN=' + weblate_registration_open + '\n')
        f.write('WEBLATE_EMAIL_HOST=' + weblate_email_host + '\n')
        f.write('WEBLATE_EMAIL_HOST_USER=' + weblate_email_host_user + '\n')
        f.write('WEBLATE_EMAIL_HOST_SSL=' + weblate_email_host_ssl + '\n')
        f.write('GITEA_DB_USER=' + gitea_db_user + '\n')
        f.write('MICADO_TRANSLATIONS_DIR=' + micado_translations_dir + '\n')
        f.write('MICADO_ENV=' + micado_env + '\n')
        f.write('ROCKETCHAT_ADMIN=' + rocketchat_admin + '\n')
        f.write('ROCKETCHAT_ADMIN_MAIL=' + rocketchat_admin_mail + '\n')
        f.write('ALGORITHM=' + algorithm + '\n')
        f.write('SALT=' + salt + '\n')
        f.write('KEY_LENGTH=' + key_length + '\n')
        f.write('BUFFER_0=' + buffer_0 + '\n')
        f.write('BUFFER_1=' + buffer_1 + '\n')
        f.write('COUNTLY_ADMIN=' + countly_admin + '\n')
        f.write('MICADO_WEBLATE_PROJECT=' + micado_weblate_project + '\n')
        f.write('RASA_SCHEMA=' + rasa_schema + '\n')
        f.write('RASA_DB_USER=' + rasa_db_user + '\n')
        f.write('BOT_NAME=' + bot_name + '\n')
        f.write('TITLE_LIMIT=' + title_limit + '\n')
        f.write('WEBLATE_POSTGRES_PASSWORD=' + weblate_postgres_password + '\n')
        f.write('WEBLATE_EMAIL_HOST_PASSWORD=' + weblate_email_host_password + '\n')
        f.write('GITEA_DB_PWD=' + gitea_db_pwd + '\n')
        f.write('ROCKETCHAT_ADMIN_PWD=' + rocketchat_admin_pwd + '\n')
        f.write('ROCKETCHAT_USER=' + rocketchat_user + '\n')
        f.write('ROCKETCHAT_PASSWORD=' + rocketchat_password + '\n')
        f.write('RESPOND_TO_LIVECHAT=' + respond_to_livechat + '\n')
    click.echo("\nWriting env file\n")
    time.sleep(5)
    click.echo("\nThese are the contents of the .env file\n")
    a_file = open(".env")
    file_contents = a_file.read()
    click.echo(file_contents)

    #creating necessary folders
    click.echo("\nCreating folders\n")
    folder_list=["db_data", "weblate_data", "redis_data", "identity-server_data/deployment", "identity-server_data/tenants", "shared_images", 'git_data']
    [create_folder(i) for i in folder_list]
    create_file('traefik/traefik-acme/acme.json')

    #setting up docker client with env variables
    click.echo("\nSetting environment\n")
    docker = DockerClient(
        #compose_env_file='prod.env',
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
    #needs testing
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
    #should be done with python_on_whales when docker-compose exec is implemented
    gitea_migrate = 'docker-compose -f docker-compose-prod.yaml exec git gitea migrate'
    process=subprocess.Popen(gitea_migrate.split(" "), stdout=subprocess.PIPE)
    #should be done with python_on_whales when docker-compose exec is implemented
    gitea_create_user='docker-compose -f docker-compose-prod.yaml exec git gitea admin create-user --username ' + gitea_username + ' --password ' + gitea_password + ' --email ' + gitea_email + ' --admin'
    process=subprocess.Popen(gitea_create_user.split(" "), stdout=subprocess.PIPE)
    stop_service(docker, 'git')
    time.sleep(5)
    click.echo("\nSetting INSTALL_LOCK=true to git_data/gitea/conf/app.ini\n")
    replace_in_git_ini_file('git_data/gitea/conf/app.ini','security', 'INSTALL_LOCK', 'true')
    start_service(docker, 'git', 'git')
    time.sleep(15)
    #should be done with python_on_whales when docker-compose exec is implemented
    create_repo = 'docker-compose -f docker-compose-prod.yaml exec git curl -X POST "http://' + gitea_username+ ':' +gitea_password+'@git:3000/api/v1/user/repos" -H "Content-Type: application/json" -d "{\"name\": \"'+ gitea_repo + '\", \"auto_init\": true }"'
    process=subprocess.Popen(create_repo.split(" "), stdout=subprocess.PIPE)
    #should be done with python_on_whales when docker-compose exec is implemented
    create_hook = 'docker-compose -f docker-compose-prod.yaml exec git curl -X POST "http://' + gitea_username+ ':' +gitea_password+'@git:3000/api/v1/repos/$GITEA_USERNAME/$GITEA_REPO/hooks" -H "Content-Type: application/json" -d "{"active": true,"branch_filter": "*","config": {"content_type": "json","url": "http://weblate:8080/hooks/gitea/","http_method": "post"},"events": ["push"],"type": "gitea"}"'
    process=subprocess.Popen(create_hook.split(" "), stdout=subprocess.PIPE)

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
    time.sleep(5)
    click.echo("\nCreating realms\n")
    keycloak_token =requests.post('https://'+ keycloak_hostname + '/auth/realms/master/protocol/openid-connect/token', data={'username': keycloak_user, "password": keycloak_password, "grant_type": "password", "client_id":"admin-cli"}, headers = {"Content-Type": "application/x-www-form-urlencoded"})
    access_token = keycloak_token.json()['access_token']
    click.echo("\nCreating migrant realm\n")
    data_migrant = open('./migrant-realm-export.json', 'rb')
    create_realm_migrant = requests.post('https://'+ keycloak_hostname + '/auth/admin/realms', data = data_migrant, headers={"Authorization": "Bearer "+ access_token, 'Content-Type': 'application/json'})
    click.echo("\nCreating pa realm\n")
    data_pa = open('./pa-realm-export.json', 'rb')
    create_realm_pa = requests.post('https://'+ keycloak_hostname + '/auth/admin/realms', data = data_pa, headers={"Authorization": "Bearer "+ access_token, 'Content-Type': 'application/json'})
    click.echo("\nCreating cso realm\n")
    data_ngo = open('./ngo-realm-export.json', 'rb')
    create_realm_ngo = requests.post('https://'+ keycloak_hostname + '/auth/admin/realms', data = data_ngo, headers={"Authorization": "Bearer "+ access_token, 'Content-Type': 'application/json'})
    time.sleep(5)
    click.echo("\nFinished keycloak setup\n")

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
    click.echo("\nStarted Rocketchat")

    #needs testing
    click.echo("\nSetting up Rocketchat")
    bot_name=rasa_bot
    rktauth = requests.post('https://'+ rocketchat_hostname + '/api/v1/login', data = {'username': rocketchat_admin, 'password': rocketchat_admin_pwd}, headers = {"Content-Type": "application/json"})
    click.echo(rktauth.content)
    rkauth_json=rktauth.json()
    rktuid=rkauth_json['data']['userId']
    click.echo(rktuid)
    rkttk=rkauth_json['data']['authToken']
    click.echo(rkttk)
    click.echo("Creating user")
    rkdos = requests.post('https://'+ rocketchat_hostname + '/api/v1/login', data = {'name': bot_name,'email': 'luca.gioppo@csi.it','password': rasa_bot_password,'username': bot_name,'requirePasswordChange': 'false','sendWelcomeEmail': 'false', 'roles': '[bot]'}, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid})
    click.echo(rkdos.content)
    rktres=requests.post('https://'+ rocketchat_hostname + '/api/v1/livechat/users/agent', data={'username': bot_name}, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid})
    click.echo(rktres.content)
    rktres_json=rktres.json()
    agent_user_id=rktres_json['user']['_id']
    click.echo(agent_user_id)

    sha256password=sha256(rocketchat_admin_pwd.encode('utf-8')).hexdigest()
    click.echo(sha256password)
    ##CONFIGURE LIVECHAT and SETTINGS
    rktres=requests.post('https://'+ rocketchat_hostname + '/api/v1/settings/Livechat_enabled', data={'value': 'true'}, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid, 'x-2fa-method':'password','x-2fa-code': sha256password})
    click.echo(rktres.content)
    rktres=requests.post('https://'+ rocketchat_hostname + '/api/v1/settings/Livechat_registration_form', data={'value': 'false'}, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid, 'x-2fa-method':'password','x-2fa-code': sha256password})
    click.echo(rktres.content)
    rktres=requests.post('https://'+ rocketchat_hostname + '/api/v1/settings/Livechat_title', data={'value': 'Micado bot'}, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid, 'x-2fa-method':'password','x-2fa-code': sha256password})
    click.echo(rktres.content)
    ##CREATE DEPARTMENT
    rktres=requests.post('https://'+ rocketchat_hostname + '/api/v1/livechat/department', data={'department':{'enabled': 'true','showOnRegistration': 'true','showOnOfflineForm':'false','email': 'email@email.com','name': 'micado','description': 'default department'},'agents': [{'agentId': agent_user_id,'username': bot_name,'count': 0,'order': 0}]}, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid})
    click.echo(rktres.content)
    ##CREATE WEBHOOK
    rktres=requests.post('https://'+ rocketchat_hostname + '/api/v1/integrations.create', data={ 'type': 'webhook-outgoing', 'name': 'Rasa', 'event': 'sendMessage', 'enabled': 'true', 'username': bot_name, 'urls': ['http://chatbot:5005/webhooks/rocketchat/webhook'], 'scriptEnabled': 'true', 'channel':'all_direct_messages' }, headers = {"Content-Type": "application/json", 'X-Auth-Token': rkttk, 'X-User-Id': rktuid})
    click.echo(rktres.content)
    click.echo("\nFinished Rocketchat setup")


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
""" 
