#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : shenny
# @Time     : 2022/12/13 15:18
# @File     : run_shell.py
# @Project  : BioWorkFlow


"""提交shell命令，并保存运行日志"""

import logging
import os
import subprocess
import time

import click


def run_shell(cmd, jobname, sample, d_log=None):
    """ 提交shell命令，并保存运行日志

    :param cmd: 待提交的任务
    :param jobname:  任务名
    :param sample:  样本名
    :param d_log:  输出结果文件
    :return:
    """

    # 生成并记录命令
    f_log = f"{d_log}/{sample}--{jobname}.log"
    f_script = f"{d_log}/{sample}--{jobname}.sh"

    mylogger = logging.getLogger("BioWorkDlow")
    mylogger.setLevel(level=logging.DEBUG)
    fh = logging.FileHandler(f"{d_log}/{sample}.log")
    formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fh.setFormatter(formatter)
    mylogger.addHandler(fh)

    run_cmd = f"({cmd}) > {f_log} 2>&1"
    with open(f_script, 'w') as f:
        f.write(cmd)

    # 运行命令，记录日志
    start = time.time()
    mylogger.info("{}\t{}\t{}\t{}".format(sample, jobname, "start", -1))

    try:
        subprocess.check_call(run_cmd, shell=True)
    except Exception as error:
        mylogger.error(f"{sample}\t{jobname}\tfailed\t{time.time() - start}")
        raise RuntimeError(error)
    else:
        mylogger.info(f"{sample}\t{jobname}\tfinished\t{time.time() - start}")


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option("-c", "--cmd", required=True, help="command.")
@click.option("-j", "--jobname", required=True, help="job name.")
@click.option("-n", "--sample", required=True, help="sample name.")
@click.option("-d", "--d_log", required=True, help="path of log file.")
def cli(**kwargs):
    run_shell(**kwargs)


if __name__ == '__main__':
    cli()