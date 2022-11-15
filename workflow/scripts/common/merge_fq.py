#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : shenny
# @Time     : 2022/11/14 16:37
# @File     : merge_fq.py
# @Project  : BioWorkFlow


"""合并同一个样本的所有fq文件"""

from multiprocessing import Pool
import logging
from glob import glob
import os
import subprocess

import click
import coloredlogs


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)


class MergeFq(object):

    def __init__(self, raw_data_list: list, sample_id, output="", threads=5,
                 suffix_1="R1_*.fastq.gz", suffix_2="R2_*.fastq.gz"):

        self.raw_data_list = raw_data_list
        self.sample_id = sample_id
        self.output = self._outdir(output)
        self.threads = threads
        self.suffix_1 = suffix_1
        self.suffix_2 = suffix_2

        self.pool = Pool(processes=threads)

    def merge(self):
        """合并R1 R2 fastq文件"""

        cmd_list = []
        r1_list = sorted([f for d in self.raw_data_list for f in glob(f"{d}/{self.sample_id}*{self.suffix_1}")])
        r2_list = sorted([f for d in self.raw_data_list for f in glob(f"{d}/{self.sample_id}*{self.suffix_2}")])

        if r1_list and r2_list:

            cmd_1, cmd_2 = "cat ", "cat "
            for r1, r2 in zip(r1_list, r2_list):
                if self.rreplace(r1, "R1", "R2") != r2:
                    raise ValueError(f"R1,R2 file not equal: <{r1}> <{r2}>")
                cmd_1 += f" {r1} "
                cmd_2 += f" {r2} "

            cmd_1 += f" > {self.output}/{self.sample_id}_R1.fastq.gz"
            cmd_2 += f" > {self.output}/{self.sample_id}_R2.fastq.gz"
            cmd_list.append(cmd_1)
            cmd_list.append(cmd_2)

            self.pool.map(self.run_command, cmd_list)
            self.pool.close()
            self.pool.join()

        else:
            logger.warning(f"find no fq files in <{self.raw_data_list}>.")

    @staticmethod
    def _outdir(p):
        if not os.path.exists(p):
            try:
                os.makedirs(p)
            except:
                pass
        return p

    @staticmethod
    def rreplace(string, old, new, times=1):
        """从右往左进行字符串替换"""

        return string[::-1].replace(old[::-1], new[::-1], times)[::-1]

    @staticmethod
    def run_command(cmd):
        logger.info(f"run cmd: {cmd}")
        subprocess.check_output(cmd, shell=True)
        logger.info(f"done")

    def __del__(self):
        self.pool.close()
        self.pool.join()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option("-r", "--raw_data", "raw_data_list",
              multiple=True, required=True,
              help="原始下机目录"
              )
@click.option("-s", "--sample_id", "sample_id",
              required=True,
              help="样本ID"
              )
@click.option("-o", "--output",
              required=True,
              help="结果目录"
              )
@click.option("-t", "--threads",
              default=5, type=click.INT,
              help="最大线程数"
              )
@click.option("--x1", "--suffix_1", "suffix_1",
              default="R1_*.fastq.gz", help="R1文件的后缀(包含R1往后的字符串格式，支持正则匹配)"
              )
@click.option("--x2", "--suffix_2", "suffix_2",
              default="R2_*.fastq.gz", help="R2文件的后缀(包含R1往后的字符串格式，支持正则匹配)"
              )
def cli(**kwargs):
    MergeFq(**kwargs).merge()


if __name__ == '__main__':
    cli()
