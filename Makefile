#!/bin/bash
LINE_NUM=120

all: configure

configure: 
	@g++ -o Calc calc.cc `root-config --libs --cflags` ;\
	cd data ; \
	for dir in `ls` ; do \
		echo $${dir}' generating' ;\
		cp ../subq.con $${dir} ;\
		cp ../Calc $${dir} ;\
	done ; \


compile:
	@g++ -o Calc calc.cc `root-config --libs --cflags` 

submit:
	@cd data;\
	for dir in `ls` ; do \
		cd $${dir} ;\
		condor_submit subq.con; \
		cd .. ;\
	done 

check:
	@cd data ; \
	for dir in `ls` ; do \
		if [ -e "$${dir}/tmpl.pid" ];then \
			exitcode=`cat $${dir}/tmpl.pid` ; \
			echo "$${dir}'s exitcode is $${exitcode}." ; \
			if [ $${exitcode} -ne 0 ]; then \
				echo "job failed" ; \
			else \
				echo "job succeeded" ; \
			fi; \
		else \
			echo "$${dir} not finished" ; \
		fi ; \
	done

clean:
	for dir in `ls data`;do \
		rm data/$${dir}/job.err ; \
		rm data/$${dir}/job.out ; \
		rm data/$${dir}/job.log ; \
		rm data/$${dir}/AuAu54.root ; \
	done

clearRoot:
	for dir in `ls data`;do \
		rm data/$${dir}/AuAu54.root ; \
	done
	
merge:
	@cdir=`pwd` ; \
	mkdir _merge ; \
	cd data/TASK1 ; \
	rootfiles=(`find * -name '*.root'`) ; \
	cd $${cdir}/data ; \
	for file in $${rootfiles[@]}; do \
		roots=() ; \
		for dir in `ls`; do \
			if [ -d $${dir} ];then \
				roots=($${roots[@]} $${dir}/$${file}) ; \
			fi ; \
		done ; \
		echo hadd ../_merge/$${file} $${roots[@]} ; \
		hadd ../_merge/$${file} $${roots[@]} ; \
	done

chec:
	@for dir in `ls data` ;do\
		ls -hl data/$${dir}/rawmoments.root ;\
	done

mer:
	hadd rawmoments_merged.root `find data -name '*.root'`

clearEmpty:
	find data -name "*" -type f -size 0c | xargs -n 1 rm -f

submitEmpty:
	for dir in `ls data` ;do\
		if [ ! -f data/$${dir}/AuAu54.root ];then \
			condor_submit data/$${dir}/subq.con ;\
		fi ; \
	done
mm:
	@for dir in `ls data`;do\
		cat data/$${dir}/job.out >> job.out ;\
	done

me:
	@mkdir merge ;\
	cd merge ;\
	hadd 1.root ../data/task1/rawmoments.root ../data/task11/rawmoments.root ../data/task21/rawmoments.root ;\
	hadd 2.root ../data/task2/rawmoments.root ../data/task12/rawmoments.root ../data/task22/rawmoments.root ;\
	hadd 3.root ../data/task3/rawmoments.root ../data/task13/rawmoments.root ../data/task23/rawmoments.root ;\
	hadd 4.root ../data/task4/rawmoments.root ../data/task14/rawmoments.root ../data/task24/rawmoments.root ;\
	hadd 5.root ../data/task5/rawmoments.root ../data/task15/rawmoments.root ../data/task25/rawmoments.root ;\
	hadd 6.root ../data/task6/rawmoments.root ../data/task16/rawmoments.root ../data/task26/rawmoments.root ;\
	hadd 7.root ../data/task7/rawmoments.root ../data/task17/rawmoments.root ../data/task27/rawmoments.root ;\
	hadd 8.root ../data/task8/rawmoments.root ../data/task18/rawmoments.root ../data/task28/rawmoments.root ;\
	hadd 9.root ../data/task9/rawmoments.root ../data/task19/rawmoments.root ../data/task29/rawmoments.root ;\
	hadd 10.root ../data/task10/rawmoments.root ../data/task20/rawmoments.root ../data/task30/rawmoments.root ;\
	hadd 12.root 1.root 2.root ;\
	hadd 34.root 3.root 4.root ;\
	hadd 56.root 5.root 6.root ;\
	hadd 78.root 7.root 8.root ;\
	hadd 90.root 9.root 10.root ;\
	hadd 14.root 12.root 34.root ;\
	hadd 58.root 56.root 78.root ;\
	hadd rawmoments.root 14.root 58.root 90.root 
