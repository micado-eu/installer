import click
import os
#from python_on_whales import DockerClient
import requests



def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chown(folder, os.getuid(), os.getgid())
        print("Directory " , folder ,  " Created ")
    else:    
        print("Directory " , folder ,  " already exists") 



@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def main(count, name):
    """MICADO installer program"""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

    folder_list=["db_data", "weblate_data", "redis_data", "identity-server_data/deployment", "identity-server_data/tenants", "shared_images"]
    [create_folder(i) for i in folder_list]




if __name__ == '__main__':
    main()