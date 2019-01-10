"""

Author: Muhammad Zohaib Anwar
License: GPL v3.0\n\n


Description:
Trinity is the state-of-the-art transcriptomic assembler. Trinity can be used in independently however for a relatively straight-forward use we have wrapped it in this script which assembles transcriptomic short reads from NGS (MiSeq, HiSeq or NextSeq) reads to longer contigs. Short reads can be single or paired end as described in examples below.

Dependencies:
1. Trinity https://github.com/trinityrnaseq/trinityrnaseq

Example:
python assemble_reads.py -i $Fastq_dir -o $Output_dir -c 16 -m 100G -l paired -s RF
Given an input directory $Fastq_dir {$[*]R1.fastq.gz, $[*]R2.fastq.gz}, paired-end RF orientation reads are assembled into contigs using Trinity in parallel with 16 cpus and 100G of memory.

python assemble_reads.py -i $Fastq_dir -o $Output_dir -c 16 -m 100G -l single -s F
Given an input directory $Fastq_dir {$[*].fastq.gz}, sinle F orientation reads are assembled into contigs using Trinity in parallel with 16 cpus and 100G of memory.

"""

import subprocess
import sys
import argparse
import os
import os.path as path

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-i", "--inputdir", help= "Fastq file directory")
parser.add_argument("-o", "--outputdir", help= "Output directory")
parser.add_argument("-c", "--cpus", help= "Number of Threads to be used", type=int, default=1)
parser.add_argument("-m", "--memory", help='Max-memory to be used in Gb e.g 20G', default = '20G')
parser.add_argument("-l", "--libtype", help='Single or Paired-end library')
parser.add_argument("-s", "--strandlibtype", help='Strand-specific RNA-Seq read orientation if paired: RF or FR, if single: F or R.')

args = parser.parse_args()
if not args.inputdir: print "No input reads directory provided"
if not args.outputdir: print "No output directory provided"
if not args.libtype: print "Please specify single or paired-end library"
if not args.strandlibtype: print "Please specify Strand-orientation"
if not (args.inputdir or args.outputdir or args.libtype or args.strandlibtype): sys.exit(1)


CoMWdir = os.path.realpath(__file__)
dbdir =  path.abspath(path.join(__file__ ,"../../databases"))
utildir = path.abspath(path.join(__file__ ,"../../utils"))
cpus = args.cpus
inputdir = args.inputdir
outputdir = args.outputdir
memory = args.memory
orientation = args.strandlibtype
lib = args.libtype

	
if __name__ == "__main__":

	if lib == 'paired':
		R1 = []
		R2 = []
		for i in os.listdir(inputdir):
			if 'R1' in i:	
				R1.append(i)
			else:
				R2.append(i)
		left = ""
		right = ""
		for item in sorted(R1):
			left = left + item + ","
		left = left.strip(",")		
		for item in sorted(R2):
			right = left + item + ","
		right = right.strip(",")
		command = ["Trinity", "--seqType fq" , "--max_memory " + str(memory), "--left " + left, "--right " + right, "--SS_lib_type " + str(orientation), "--CPU " + str(cpus), "--output " + str(outputdir)]
		print command
		#subprocess.check_output(command)
	else:
		files = []
		for i in os.listdir(inputdir):
			if 'R1' or 'R2' in i:	
				files.append(i)
		single = ""
		for item in files:
			single = single + item + ","
		single = single.strip(",")		
		command = ["Trinity", "--seqType fq" , "--max_memory " + str(memory), "--single " + single, "--SS_lib_type " + str(orientation), "--CPU " + str(cpus), "--output " + str(outputdir)]
		print command
		#subprocess.check_output(command)
