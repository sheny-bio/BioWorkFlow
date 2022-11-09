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


@click.command()
@click.option("--work_dir")
@click.option("--pipeline")
@click.option("--conf_sample", require=True)
@click.option("--conf_env")
@click.option("--dry_run", is_flag=True)
def click(work_dir, pipeline, conf_sample, conf_env, dry_run):
    cmd = f"snakemake --directory {work_dir} " \
          f"--snakefile {d_pipe}/{pipeline}.snk " \
          f"--configfile {conf_sample} " \
          f"--configfile {conf_env} " \
          f"--jobname {{params.rulename}}.{{jobid}} " \
          f"--use-conda --conda-prefix {d_conda} " \
          f"-k -j 1199 " \
          f"--cluster 'bsub -q normal -n {{threads}} -J aio2020.{{wildcards.sample}}.{{rule}} -R \"span[hosts=1]\" " \
          f"-o Results/{{wildcards.sample}}/01Log/{{params.rulename}}.{{wildcards.sample}}.out " \
          f"-e Results/{{wildcards.sample}}/01Log/{{params.rulename}}.{{wildcards.sample}}.err '"
    if dry_run:
        cmd = cmd + " --dry_run "
    subprocess.check_output(cmd, shell=True)

