import sys
import textwrap
import time
import os
import re
import random
import parabam
import pdb

from shutil import copy
from numpy import genfromtxt,mean,sqrt,\
                  rot90,tril,log,zeros,std
from numpy import round as np_round
from itertools import izip
from collections import namedtuple
from sklearn.mixture import GMM

import simulator

######################################################################
##
##      Create a length estimate given a set of TELBAMS 
##
##      Author: jhrf
##
######################################################################

class ReadLogic(object):

    def __init__(self,phred_offset=33,error_profile=None):
        self._SimpleRead = namedtuple("SimpleRead","seq qual complete five_prime adjust pattern frames")
        self._phred_offset = phred_offset

        self._compliments = {"A":"T","T":"A",
                             "C":"G","G":"C",
                             "N":"N"}

        self._error_profile = error_profile
        if error_profile is None:
            self._complete_decision = self.__complete_decision__
        else:
            self._complete_decision = self.__complete_decision_error__

        self._templates = self.__get_compare_templates__(["TTAGGG","CCCTAA"])

        self._solution_tree =\
            {'CCCTAA': {'A': {'AAA': ('', 1), 'TAC': ('A', 0)},
                        'ACA': {'TACAC': ('', 1)},
                        'AGA': {'TAGAC': ('', 1)},
                        'AGC': {'AAGCC': ('', 1)},
                        'ATA': {'TATAC': ('', 1)},
                        'ATC': {'AATCC': ('', 1)},
                        'CA': {'CCAA': ('T', 1)},
                        'CAC': {'ACACC': ('', 1), 'CCACT': ('', 1)},
                        'CAT': {'CCATA': ('', 1)},
                        'CC': {'ACCT': ('C', 0), 'CCCC': ('', 1)},
                        'CGC': {'ACGCC': ('', 1), 'CCGCT': ('', 1)},
                        'CGT': {'CCGTA': ('', 1)},
                        'CTC': {'ACTCC': ('', 1), 'CCTCT': ('', 1)},
                        'TCA': {'CTCAA': ('', 1)},
                        'TGA': {'CTGAA': ('', 1)},
                        'TT': {'CTTA': ('', 1)}},
             'TTAGGG': {'AA': {'TAAG': ('', 1)},
                        'ACG': {'TACGG': ('', 1)},
                        'ATG': {'TATGG': ('', 1)},
                        'GAG': {'AGAGG': ('', 1), 'GGAGT': ('', 1)},
                        'GAT': {'GGATT': ('', 1)},
                        'GCG': {'AGCGG': ('', 1), 'GGCGT': ('', 1)},
                        'GCT': {'GGCTT': ('', 1)},
                        'GG': {'AGGT': ('G', 0), 'GGGG': ('', 1)},
                        'GTG': {'AGTGG': ('', 1), 'GGTGT': ('', 1)},
                        'T': {'GTA': ('T', 0), 'TTT': ('', 1)},
                        'TAT': {'GTATA': ('', 1)},
                        'TCA': {'TTCAG': ('', 1)},
                        'TCT': {'GTCTA': ('', 1)},
                        'TG': {'TTGG': ('A', 1)},
                        'TGA': {'TTGAG': ('', 1)},
                        'TGT': {'GTGTA': ('', 1)}}}
    
    def __complete_decision__(self,seq,qual,mismatch_loci):
        return len(mismatch_loci) == 0

    def __complete_decision_error__(self,seq,qual,mismatch_loci):
        if len(mismatch_loci) == 0:
            return True
        else:
            average_quality = self.__get_average_qual__(mismatch_loci, qual)
            return self._error_profile[len(mismatch_loci),average_quality]
        return False

    def __get_average_qual__(self,loci,qual):
        qual_ints = []
        for i in loci:
            qual_ints.append(ord(qual[i])-self._phred_offset)
        return int(mean(qual_ints))

    def __get_pattern__(self,seq):
        cta,tag = "CCCTAA","TTAGGG"
        pattern = ""
        if cta in seq or tag in seq:   
            if seq.count(cta) > seq.count(tag):
                pattern = cta
            else:
                pattern = tag
        return pattern

    def __get_compare_templates__(self,patterns):
        templates = {}
        for pattern in patterns:
            templates[pattern] = {}
            for i in xrange(len(pattern)):
                templates[pattern][i] = (pattern[ len(pattern)- i:] )\
                                        + (pattern*17)[:100]
        return templates

    def get_read_type(self,read1,read2):
        simple_reads = self.get_simple_reads( (read1,read2,) )
        is_complete = map(lambda read: read.complete, simple_reads)

        if all(is_complete):
            #Reads both completely mapped to reference are true telomere
            return "F1"
        elif any(is_complete):
            #One read not complete, test if it's on the telomere boundary
            return self.__check_orientation__(simple_reads)
        else:
            return "F3"

    def __check_orientation__(self,simple_reads):
        #This function is only called when at least 
        #one read was completely telomeric 
        
        if (simple_reads[0].five_prime and simple_reads[0].complete) or\
           (not simple_reads[0].five_prime and not simple_reads[0].complete):
            #This read may be on the boundary, or could be the opposite
            #side of an interestitial read.
            return "F2"
        else:
            #Wrong end is complete! This is a TTAGGG read (originally), 
            #We know that this read originated from an ITS region or
            #malformed proximal telomere
            return "F4"

    def get_simple_reads(self,reads):
        simple_reads = []
        for read in reads:
            seq,qual = self.__flip_and_compliment__(read)
            pattern = self.__get_pattern__(seq)

            if pattern:
                adjust,seq,qual,frames = self.__frameshift_adjustment__(seq,qual,pattern)
                complete = self.__is_complete__(seq,qual,pattern,frames) #complete
            else:
                frames = []
                adjust = False
                complete = False
                
            simple_read = self._SimpleRead(
                seq,
                qual,
                complete,
                (pattern == "CCCTAA"),#five_prime
                adjust,
                pattern,
                frames)

            simple_reads.append(simple_read)
        return simple_reads

    def __flip_and_compliment__(self,read):
        if read.is_reverse:
            compliments = self._compliments
            seq_compliment = map(lambda base: compliments[base],read.seq)
            seq_compliment = "".join(seq_compliment)
            return(seq_compliment[::-1],read.qual[::-1])
        else:
            return (read.seq,read.qual)

    def __is_complete__(self,seq,qual,pattern,frames):

        mismatch_loci = self.__get_mismatch_loci__(seq,pattern,frames)
        return self._complete_decision(seq,qual,mismatch_loci)

    def __get_mismatch_loci__(self,seq,pattern,frames):
        best_offset = float("inf")
        best_mismatch = []
        best_mismatch_count = len(seq)+1

        offsets = set(zip(*frames)[0])
        for offset in offsets:
            mismatch = []
            mismatch_count = 0

            reference = self._templates[pattern][offset]
            for i,(s,r) in enumerate(izip(seq,reference)):
                if not s==r:
                    mismatch.append(i)
                    mismatch_count += 1

                if mismatch_count > best_mismatch_count:
                    break

            if mismatch_count < best_mismatch_count:
                best_offset = offset
                best_mismatch = mismatch
                best_mismatch_count = mismatch_count

        return best_mismatch

    def __frameshift_adjustment__(self,seq,qual,pattern):
        frames = self.__get_frames__(seq,pattern)
        interactions = self.__get_interactions__(frames)

        poor_quality_interactions = self.__poor_quality_interaction__(interactions,qual)
        if len(poor_quality_interactions) > 0:
            seq_list = list(seq)
            qual_list = list(qual)
            offset = 0
            adjust = False
            for inter_type,start,end in poor_quality_interactions:
                affected = seq[start:end+1]
                scope = seq[start-1:end+2]
                try: 
                    command,location = self._solution_tree[pattern][affected][scope]
                    adjust = True
                except KeyError:
                    command,location = None,None

                if not location is None:
                    if command:
                        seq_list.insert(start+location+offset, command)
                        qual_list.insert(start+location+offset, "H")

                        offset += 1
                    else:
                        del seq_list[start+location+offset]
                        del qual_list[start+location+offset]
                        offset -= 1

            return adjust,"".join(seq_list),"".join(qual_list),frames
        return False,seq,qual,frames

    def __poor_quality_interaction__(self,interactions,qual):
        poor_qual_inter = []
        for inter_type,start,end in interactions:
            for q in qual[start:(end+1)]:
                if (ord(q)-self._phred_offset) < 11:
                    is_poor_qual = True
                    poor_qual_inter.append( (inter_type,start,end) )
                    break
        return poor_qual_inter

    def __get_frames__(self,seq,pattern):
        frames = []
        mismatch_loci = []
        end_span = self.__end_span__
        if pattern:
            for offset in xrange(len(pattern)):
                regex_output = (re.findall("."*len(pattern)+"?",seq[offset:]))
                if pattern in regex_output:
                    spans = []
                    start = 0
                    carry_on = False
                    prev_segment = seq[:offset]
                    for seg_id,segment in enumerate(regex_output):
                        position = (seg_id*len(pattern))+offset
                        if segment == pattern:
                            if not carry_on:
                                start = position
                                for pat,seg in zip(pattern[::-1],prev_segment[::-1]):
                                    if pat == seg:
                                        start -= 1
                                    else:
                                        break
                                carry_on = True
                        else:
                            if carry_on:
                                spans.append((start,end_span(pattern, segment, position)))
                                carry_on = False
                        prev_segment = segment
                    if carry_on:
                        spans.append( (start,end_span(pattern, seq[position:], position)) ) 
                    frames.append( (offset,spans,) )
        return frames

    def __end_span__(self,pattern,segment,block_start):
        for pat,seg in zip(pattern*17,segment):
            if pat == seg:
                block_start += 1
            else:
                break
        return (block_start-1) #minus because loci are zero based

    def __get_interactions__(self,frames):
        interactions = []
        test_interaction = self.__test_interaction__
        for offset,spans in frames:
            for span in spans:
                for target_offset,target_spans in frames:
                    if target_offset >= offset:
                        continue
                    for t_span in target_spans:
                        interaction = test_interaction(span, t_span)
                        if interaction:
                            interactions.append(interaction)
        return interactions

    def __test_interaction__(self,span1,span2):
        if span1[0] >= span2[0]: #copy and paste code
            higher,lower = span1,span2
        else:
            lower,higher = span1,span2

        dif = higher[0] - lower[1]
        if dif > 0 and dif < 3: #gap
            return ("gap",lower[1],higher[0])
        elif dif < 0:#overlap
            return ("overlap",higher[0],lower[1])
        else:#no_interaction
            return None

class VitalStatsFinder(object):

    def __init__(self,temp_dir,total_procs,task_size):
        self._temp_dir = temp_dir
        self._total_procs = total_procs
        self._task_size = task_size

    def __csv_to_dict__(self,stats_path):
        insert_dat = genfromtxt(stats_path,delimiter=",",
                                names=True,dtype=("S256",float,float,
                                                         float,float,
                                                         float,float))
        N = int(insert_dat['N'])
        if N == 0:
            insert_mean = -1
            insert_sd = -1
        else:
            ins_sum = int(insert_dat['sum'])
            power_2 = int(insert_dat['power_2'])

            insert_mean = ins_sum /N
            insert_sd = sqrt(N * power_2 - ins_sum**2) / N
            
        return {"insert_mean":insert_mean, 
                "insert_sd": insert_sd,
                "read_len":int(insert_dat['read_len']),
                "min_qual":int(insert_dat['min_qual']),
                "max_qual":int(insert_dat['max_qual'])}

    def get_vital_stats(self,sample_path):

        vital_stats_csv = self.__run_vital_engine__(sample_path)
        result_dictionary = self.__csv_to_dict__(vital_stats_csv)

        read_counts_path,random_path,phred_offset = self.__run_read_count_engine__(sample_path,
                                                                    result_dictionary)
        
        error_profile = self.__path_to_profile__(read_counts_path)
        
        result_dictionary["read_counts_path"] = read_counts_path
        result_dictionary["error_profile"] = error_profile
        result_dictionary["phred_offset"] = phred_offset
        
        return result_dictionary

    def __path_to_profile__(self,read_counts_path,std_thresh = .5):
        read_counts = genfromtxt(read_counts_path,delimiter=",")
        read_counts[0,0] = 0

        mask = rot90(tril(zeros( read_counts.shape[::-1] )+1,k=-5),k=3)
        mask[0:2,:] = 1
        mask[25:,0:5] = 0

        log_read_counts = log(read_counts+1)

        mixture_model = GMM(n_components=2)
        mixture_model.fit(log_read_counts.reshape(len(log_read_counts.flatten()),1))

        means = np_round(mixture_model.means_,5).flatten().tolist()
        covars = np_round(mixture_model.covars_,5).flatten().tolist()

        if means[0] > means[1]:
            signal_index = 0
        else:
            signal_index = 1

        #print means,covars,signal_index

        thresh = means[signal_index] + (sqrt(covars[signal_index])*std_thresh)

        error_profile = log_read_counts > thresh
        error_profile[0:2,:] = 1

        return error_profile * mask

    def read_line(self,path):
        with open(path,"r") as file_obj:
            for line in file_obj:
                line.split(",")
                print line

    def __run_vital_engine__(self,sample_path):
        def engine(read,constants,master):
            stats = {}

            if read.is_read1:
                if read.mapq > 40 and read.is_proper_pair:
                    insert_size = abs(read.template_length)
                    stats["sum"] = {"result":insert_size}
                    stats["power_2"] = {"result":insert_size**2}
                    stats["N"] = {"result":1}
            
            stats["read_len"] = {"result": len(read.seq)}
            byte_vals = map(ord,read.qual)
            min_qual = min(byte_vals)
            max_qual = max(byte_vals)

            stats["min_qual"] = {"result":min_qual}
            stats["max_qual"] = {"result":max_qual}

            return stats

        structures = {}

        structures["sum"] = {"data":0,"store_method":"cumu"}
        structures["power_2"] = {"data":0,"store_method":"cumu"}
        structures["N"] = {"data":0,"store_method":"cumu"}
        structures["read_len"] = {"data":0,"store_method":"max"}

        structures["min_qual"] = {"data":999,"store_method":"min"}
        structures["max_qual"] = {"data":0,"store_method":"max"}

        stat_interface = parabam.command.stat.Interface(self._temp_dir)
        out_paths = stat_interface.run(
            input_bams= [sample_path],
            total_procs = self._total_procs,
            task_size = 10000,
            user_constants = {},
            user_engine = engine,
            user_struc_blueprint = structures,
            keep_in_temp=True)

        return out_paths["global"][0]

    def __run_read_count_engine__(self,sample_path,vital_stats):

        read_len = vital_stats["read_len"]
        phred_offset = vital_stats["min_qual"]
        max_phred = vital_stats["max_qual"] - phred_offset
        matrix_size = max_phred+1

        structures = {"read_counts":{"data":zeros((read_len,matrix_size)),
                                        "store_method":"cumu"},
                      "random_counts":{"data":zeros((read_len,matrix_size)),
                                        "store_method":"cumu"}}

        readlogic = ReadLogic(phred_offset=phred_offset)

        def engine(read,master,constant):
            read_counts = zeros((read_len,matrix_size))
            random_counts = zeros((read_len,matrix_size))
            simple_read = readlogic.get_simple_reads([read])[0]

            if simple_read.pattern:

                mismatch_loci = readlogic.__get_mismatch_loci__(\
                                    simple_read.seq,simple_read.pattern,simple_read.frames)

                if len(mismatch_loci) > 0:
                    average_qual = readlogic.__get_average_qual__\
                                        (mismatch_loci,simple_read.qual)
                    random_qual = map(lambda q: ord(q)-phred_offset,\
                                    random.sample(simple_read.qual,len(mismatch_loci)))

                    random_counts[len(mismatch_loci),mean(random_qual)] = 1
                    read_counts[len(mismatch_loci),average_qual] = 1
                elif len(mismatch_loci) == 0:
                    read_counts[len(mismatch_loci),0] = 1

            return {"read_counts":{"result":read_counts},
                    "random_counts":{"result":random_counts}}

        stat_interface = parabam.command.stat.Interface(self._temp_dir)
        out_paths = stat_interface.run(
            input_bams= [sample_path],
            total_procs = self._total_procs,
            task_size = 10000,
            user_constants = {},
            user_engine = engine,
            user_struc_blueprint = structures,
            keep_in_temp=True)

        return out_paths[sample_path][0],out_paths[sample_path][1],phred_offset

class Interface(parabam.core.Interface):
    def __init__(self,temp_dir):
        super(Interface,self).__init__(temp_dir)
        self._compliments = {"A":"T","T":"A","C":"G","G":"C","N":"N"}

    def run_cmd(self,parser):
        cmd_args = parser.parse_args()
        self.run(input_paths = cmd_args.input,
            total_procs = cmd_args.p,
            task_size = cmd_args.s,
            reader_n = cmd_args.f,
            verbose = cmd_args.v,
            save_alignment = cmd_args.a,
            inserts_path=cmd_args.insert,
            output = cmd_args.out,
            announce=True)

    def run(self,input_paths,total_procs,task_size,verbose,output,reader_n,inserts_path=None,
        save_alignment=False,alig_params=None,announce=False,keep_in_temp=False):
        
        if not verbose:
            announce = False
        self.verbose = verbose
        program_name = "telomerecat telbam2length"
        self.__introduce__(program_name,announce)

        names = map(lambda b: self.__get_basename__(b),input_paths)
        names = map(lambda nm: nm.replace("_telbam",""),names)

        output_csv_path = self.__create_output_file__(output)
        vital_stats_finder = VitalStatsFinder(self._temp_dir, 
                                        total_procs,
                                        task_size)
        
        insert_length_generator = self.__get_insert_generator__(inserts_path)

        for sample_path,sample_name, in izip(input_paths,names):
            sample_intro = "\tEstimating telomere length of sample: %s\n" % (sample_name)
            underline = "\t" + ("-" * (len(sample_intro)-2)) + "\n"

            self.__output__(sample_intro,1)
            self.__output__(underline,2)
            self.__output__("\t\t- Estimation start time: %s\n" % (self.__get_date_time__(),),2)

            self.__output__("\t\t- Finding read error rates and insert size\n",2)
            vital_stats = vital_stats_finder.get_vital_stats(sample_path)
            self.__check_vital_stats_insert_size__(inserts_path,insert_length_generator,vital_stats)

            read_type_counts = self.__get_read_types__(sample_path,
                                  vital_stats,total_procs,task_size,reader_n,
                                  save_alignment,keep_in_temp)

            simulation_results = self.__run_simulation__(vital_stats,read_type_counts,total_procs)

            read_type_counts.update(simulation_results)

            self.__write_to_csv__(read_type_counts,output_csv_path,sample_name)

            self.__output__("\t\t- Estimation end time: %s\n\n" \
                                                            % (self.__get_date_time__(),),1)

        self.__goodbye__(program_name,announce)
        if keep_in_temp:
            return output_csv_path
        else:
            self.__copy_out_of_temp__([output_csv_path])
            return os.path.join(".",os.path.split(output_csv_path)[1])

    def __get_insert_generator__(self,inserts_path):
        if inserts_path:
            with open(inserts_path,"r") as inserts_file:
                for line in inserts_file:
                    yield map(float,line.split(","))

    def __check_vital_stats_insert_size__(self,inserts_path,insert_length_generator,vital_stats):
        if inserts_path:
            insert_mean,insert_sd = insert_length_generator.next()
            vital_stats["insert_mean"] = insert_mean
            vital_stats["insert_sd"] = insert_sd
            self.__output__("\t\t\t+ Using user defined insert size: %d,%d\n" % (insert_mean,insert_sd),2)
        elif vital_stats["insert_mean"] == -1:
            default_mean,default_sd = 350,25
            vital_stats["insert_mean"] = 350
            vital_stats["insert_sd"] = 25
            self.__output__("\t\t\t+ Failed to estimate insert size. Using default: %d,%d\n" % \
                                                                        (default_mean,default_sd),2)

    def __get_read_types__(self,sample_path,vital_stats,total_procs,task_size,
                                          reader_n,save_alignment,keep_in_temp):
        self.__output__("\t\t- Categorising reads into telomeric read types\n",2)
        read_type_counts = self.__run_read_type_engine__(sample_path,
                                        vital_stats,task_size,
                                        total_procs,
                                        reader_n)

        self.__output__("\t\t\t+ F1:%d | F2a:%d | F2b+F4:%d\n" % (read_type_counts["F1"],
                                                            read_type_counts["F2a"],
                                                            read_type_counts["F2b_F4"],),2)
        return read_type_counts

    def __keep_files_decision__(self,file_paths,save_alignment,keep_in_temp):
        if save_alignment:
            if not keep_in_temp:
                self.__copy_out_of_temp__(file_paths)
        
        if not keep_in_temp:
            map(os.remove,file_paths)

    def __create_output_file__(self,output):
        if output:
            unqiue_file_ID = output
        else:
            unqiue_file_ID = "telomerecat_length_%d.csv" % (time.time(),)

        output_csv_path = os.path.join(self._temp_dir,unqiue_file_ID)
        with open(output_csv_path,"w") as total:
            header = "Sample,F1,F2a,F2b_F4,Uncertainty,Insert_mean,Insert_sd,Length\n"
            total.write(header)
        return output_csv_path

    def __output__(self,outstr,level=-1):
        if self.verbose and (self.verbose >= level or level == -1):
            sys.stdout.write(outstr)
            sys.stdout.flush()

    def __write_to_csv__(self,read_type_counts,output_csv_path,name):
        with open(output_csv_path,"a") as counts:
            counts.write("%s,%d,%d,%d,%.3f,%.3f,%.3f,%d\n" %\
                (name,
                read_type_counts["F1"],
                read_type_counts["F2a"],
                read_type_counts["F2b_F4"],
                read_type_counts["uncertainty"],
                read_type_counts["insert_mean"],
                read_type_counts["insert_sd"],
                read_type_counts["length"]))

    def __run_simulation__(self,vital_stats,read_type_counts,total_procs):
        self.__output__("\t\t- Using read counts to estimate length\n",2)
        total_F2 = read_type_counts["F2a"]
        total_f1 = read_type_counts["F1"]
        read_length = vital_stats["read_len"]
        insert_mean = vital_stats["insert_mean"]
        insert_sd =   vital_stats["insert_sd"]

        len_mean,len_std = simulator.run_simulator_par(insert_mean,insert_sd,
                                        total_f1,total_F2,
                                         total_procs,read_length,N=16)
        self.__output__("\t\t\t+ Length: %d\n" % (len_mean,),2)

        return {"insert_mean":insert_mean,
                "insert_sd":insert_sd,
                "length":len_mean,
                "uncertainty":len_std}
        
    def __run_read_type_engine__(self,sample_path,vital_stats,
                                        task_size,total_procs,reader_n):

        readlogic = ReadLogic(
                phred_offset=vital_stats["phred_offset"],
                error_profile=vital_stats["error_profile"])

        def engine(reads,constants,parent):
            read_type = readlogic.get_read_type(*reads)
            return {read_type:{"result":1}}

        structures = {"F1":{"data":0,"store_method":"cumu"},
                      "F2":{"data":0,"store_method":"cumu"},
                      "F4":{"data":0,"store_method":"cumu"},
                      "F3":{"data":0,"store_method":"cumu"},
                      }

        interface = parabam.command.stat.Interface(self._temp_dir)
        output_files = interface.run(input_bams=[sample_path],
                            total_procs = total_procs,
                            reader_n = reader_n,
                            task_size = 1000,
                            user_constants = {},
                            user_engine = engine,
                            user_struc_blueprint = structures,
                            keep_in_temp = True,
                            pair_process = True)

        return self.__parabam_results_to_dict__(output_files["global"][0])

    def __parabam_results_to_dict__(self,csv_path):
        results_array = genfromtxt(csv_path,
                                    delimiter=",",
                                    names=True,
                                    dtype=("S256",float,float,float,float))

        called_F2 = results_array["F2"].tolist()

        total_F4 = results_array["F4"].tolist()
        total_F1 = results_array["F1"].tolist()

        total_F2a = called_F2 - total_F4 #Find the F2a by removing the
                                          #probablistic amount of F2bs
                                          #For each F4 we assume an F2b thus

        total_F2b_F4 = total_F4 * 2 #Reflect the removal of F2b from F2a
                                     #by inflating the F4 count

        return {"F1":int(total_F1),"F2b_F4":int(total_F2b_F4),
                "F2a":int(total_F2a),
                "F2a_F2b":int(called_F2)}

    def __copy_out_of_temp__(self,file_paths,copy_path="."):
        map(lambda fil: copy(fil,copy_path),file_paths)

    def get_parser(self):
        parser = self.default_parser()
        parser.description = textwrap.dedent(
        '''\
        telomerecat telbam2length
        ----------------------------------------------------------------------

            The telbam2length command allows the user to genereate a telomere
            length estimate from a previously generated TELBAM file.

            Example useage:

            telomerecat telbam2length /path/to/some_telbam.bam

            This will generate a .csv file with an telomere length estimate
            for the `some_telbam.bam` file.

        ----------------------------------------------------------------------
        ''')

        parser.add_argument('input',metavar='TELBAM(S)', nargs='+',
            help="The telbam(s) that we wish to analyse")
        parser.add_argument('--out',metavar='CSV',type=str,nargs='?',default=None,
            help='Specify output path for length estimation CSV.\n'+\
                'Automatically generated if left blank [Default: None]')
        parser.add_argument('--insert',metavar='CSV',nargs='?',type=str,default=None,
            help="A file specifying the insert length mean and std for\n"+\
                 "each input sample. If not present telomerecat will\n"+\
                 "automatically estimate insert length of sample [Default: None]")
        parser.add_argument('-a',action="store_true",default=False
            ,help="Retain fastq and telref files created by analysis")
        parser.add_argument('-v',choices=[0,1,2],default=0,type=int,
            help="Verbosity. The amount of information output by the program:\n"\
            "\t0: Silent [Default]\n"\
            "\t1: Output\n"\
            "\t2: Detailed Output")

        return parser

if __name__ == "__main__":
    print "Do not run this script directly. Type `telomerecat` for help."
