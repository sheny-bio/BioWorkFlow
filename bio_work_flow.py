#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : shenny
# @Time     : 2022/11/8 15:09
# @File     : bio_work_flow.py
# @Project  : BioWorkFlow

import os
import subprocess

import click


path = os.path.dirname(os.path.abspath(__file__))
d_conda = f"{path}/conda_env"
d_pipe = f"{path}/workflow/snakefile"
d_conf = f"{path}/config/"


@click.command()
@click.option("--work_dir")
@click.option("--pipeline")
@click.option("--conf", multiple=True)
@click.option("--dry_run", is_flag=True)
def cli(work_dir, pipeline, conf, dry_run):
    cmd = f"snakemake --directory {work_dir} " \
          f"--snakefile {d_pipe}/{pipeline}.pipeline " \
          f"--configfile {d_conf}/base.yaml " \
          f"--jobname {{params.rulename}}.{{jobid}} " \
          f"--use-conda --conda-prefix {d_conda} " \
          f"-k -j 1199 " \
          f"--cluster 'bsub -q normal -n {{threads}} -J aio2020.{{wildcards.sample}}.{{rule}} -R \"span[hosts=1]\" " \
          f"-o Results/{{wildcards.sample}}/01Log/{{params.rulename}}.{{wildcards.sample}}.out " \
          f"-e Results/{{wildcards.sample}}/01Log/{{params.rulename}}.{{wildcards.sample}}.err '"

    if conf:
        for i in conf:
            cmd += f" --configfile {i} "
    if dry_run:
        cmd = cmd + " --dry-run "
    print(cmd)
    subprocess.check_output(cmd, shell=True)


if __name__ == '__main__':
    cli()

