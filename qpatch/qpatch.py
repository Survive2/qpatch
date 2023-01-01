import os
import click
import re
from subprocess import check_output
from sgtpyutils.xls_txt.list import list2sheet
from sgtpyutils.logger import logger

def log(log_information, value):
    logger.debug(log_information+value)

def warning(value):
    logger.warning(value)

def check_x86_64(program_name):
    sys_path = os.path.abspath(program_name)
    recv = os.popen('file ' + sys_path).read()
    if '64-bit' in recv:
        arch = 'x64'
        log("Target Arch is","amd64")
    elif '32-bit' in recv:
        arch = 'x86'
        log("Target Arch is","i386")
    else:
        logger.error("Sorry,This arch is not supported")
        exit()
    return arch

def check_libc():
    recv = os.popen('find ~ -name glibc-all-in-one').read()
    if not recv:
        warning("Detected that you don't have glibc-all-in-one,I'll download it now")
        os.system("git clone https://github.com/matrix1001/glibc-all-in-one.git")
        recv = os.popen('find ~ -name glibc-all-in-one').read()
    log("glibc-all-in-one  path is",recv.replace("\n",''))
    glibc_path = recv.replace("\n",'')
    return glibc_path

def list_libc():
    libc_path = os.path.abspath("glibc-all-in-one")
    libc_list = [f for f in os.listdir(libc_path + '/libs')]
    ret_list = libc_list
    libc_list= list2sheet(libc_list, max_show_count=20)
    description = ['\navaliable libc list:']
    description.append('\n'.join(libc_list))
    logger.debug('\n'.join(description))
    os.system("rm log.log")
    return ret_list


@click.command(name='qpatch', short_help="Use this to patch an elf quickly")
@click.argument('program_name', type=str)

def qpatch(program_name):
    program_path = os.path.abspath(program_name)
    arch = check_x86_64(program_name)
    libc_path = check_libc()
    libc_list = list_libc()
    num = input("\033[33m[NOTICE]Please choose one libc,just the number will be fine:\033[0m")
    num = int(num)
    target_libc = libc_list[num]
    target_version = target_libc[0:4]
    logger.debug("The Target libc is set to " + target_libc)
    logger.debug("The Target version is auto detected: " + target_version)
    command = "patchelf --set-interpreter " + libc_path + "/libs/" + target_libc + "/ld-" + target_version + ".so" + " " + program_path
    if(os.system(command)==0):
        logger.info("ld has been changed successfully!")
    else:
        logger.error("Failed to change the ld")
        exit()
    command = "patchelf --set-rpath " + libc_path + "/libs/" + target_libc + "/" + " " + program_path
    if(os.system(command)==0):
        logger.info("libc has been changed successfully!")
    else:
        logger.error("Failed to change the libc")
        exit()
    recv =  os.popen("ldd "+  program_name).read()
    if  target_libc in recv:
        logger.info("The Elf file is patched successfully!")
    else:
        logger.error("Something is wrong when trying to patch the elf")

qpatch()
