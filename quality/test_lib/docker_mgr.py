import os
from os.path import join, exists, dirname, abspath, realpath, basename
import time
import tarfile
import docker
from docker.errors import NotFound, ImageNotFound, APIError

CLIENT = docker.from_env()


def spin_up(image):
    container = False
    if ensure_image(image):
        container = ensure_container(image)
    return container


def ensure_image(image_name):
    app_dir = abspath(join(dirname(realpath(__file__)), '..', 'images', image_name))
    try:
        img = CLIENT.images.get(image_name)
        print '%s image exists' % img
    except ImageNotFound as e:
        print e
        # build image
        img = CLIENT.images.build(path=app_dir, tag=image_name, rm=True)
        print 'Image built %s' % img
    except APIError as e:
        print e
        return False

    return True


def ensure_container(image):
    id_file = 'container_id_%s' % image
    try:
        id = temp_get_val(id_file)
        print 'retrieve container %s' % id
        if id:
            container = CLIENT.containers.get(id)
            print 'container %s status %s ' % (container.id, container.status)
            if container.status != 'running':
                container = run_container(image)
        else:
            container = run_container(image)
    except NotFound as e:
        print e
        container = run_container(image)
    except APIError as e:
        print e
        return False

    if container:
        temp_save_val(id_file, container.id)

    return container


def run_container(image):
    print 'spin up container %s...' % image
    container = None
    try:
        container = CLIENT.containers.run(image, detach=True)
        print 'container %s is up and running' % container
        time.sleep(5)
    except Exception as e:
        print e

    return container


def temp_save_val(file, val):
    with open(join(_get_tmpdir(), file), 'w') as f:
        f.write(val)


def temp_get_val(file):
    path = join(_get_tmpdir(), file)
    if exists(path):
        with open(join(_get_tmpdir(), file), 'r') as f:
            val = f.read()
        return val
    else:
        return None


def _get_tmpdir():
    tmpdir = join(dirname(__file__), '..', '.tmp')
    if not exists(tmpdir):
        os.makedirs(tmpdir)
    return tmpdir


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=basename(source_dir))
