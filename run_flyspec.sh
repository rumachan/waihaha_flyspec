#!/bin/bash

#run_flyspec.sh
#basic flyspec pre-processing

basedir='/home/volcano/data/tongariro_flyspecs'

if [ $# == 1 ]
then
	d=$1
	date=`date -d $d +%Y_%m_%d`
else
	date=`date +%Y_%m_%d`
fi
#echo $date

for site in TOFP03 TOFP04
do

	#concatenate scanning flyspec files for a given day into a single file
	cat $basedir/$site/data/$date'_'????.txt > $basedir/$site/data/$site'_'$date'_'day.txt
	#delete concatenated file if empty	
	if [ ! -s $basedir/$site/data/$site'_'$date'_'day.txt ]
  	then
		\rm $basedir/$site/data/$site'_'$date'_'day.txt
	fi

	#split a day-length file into a file for each scan and plot that scan
	fs_splitplot.py $basedir/$site/data/$site'_'$date'_'day.txt $basedir/scratch

	#montage all scan plots and tidy up
	auto_montage.sh $site $basedir/scratch $date
	mv $basedir/scratch/$site'_'$date'_day.png' $basedir/$site/data
	rm -r $basedir/scratch
	\rm  $basedir/$site/data/$site'_'$date'_'day.txt
done
