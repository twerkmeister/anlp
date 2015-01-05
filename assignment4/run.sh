#!/bin/bash

cd `dirname $0`
if [ ! -d results ]; then
  mkdir results
fi
# create berkeley files
cd berkeley-parser
for i in `seq 1 3`
do
  if [ ! -f ../results/$i.berkeley ]; then
  java -Xmx 2G -jar BerkeleyParser.jar -gr eng_sm6.gr < ../a4_test_sets/$i.plain > ../results/$i.berkeley
  fi
done
cd ..
cd stanford-parser
for i in `seq 1 3`
do
  if [ ! -f ../results/$i.stanford ]; then
  java -mx6000m -cp "./*:" edu.stanford.nlp.parser.lexparser.LexicalizedParser \
 -sentences newline -tokenized -nthreads 3 -outputFormat "oneline" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ../a4_test_sets/$i.plain > ../results/$i.stanford
  sed -i 's/ROOT//g' ../results/$i.stanford
  fi
done

cd ..
cd a4_test_sets
if [ ! -f all.gold ]; then
  cat [123].gold > all.gold
fi
cd ../results
cat [123].stanford > all.stanford
cat [123].berkeley > all.berkeley

cd ..
for i in `seq 1 3` all
do
  for parser in "stanford" "berkeley"
  do
    for mode in "labeled" "unlabeled"
    do
      target="results/$i.$parser.eval.$mode"
      if [ ! -f $target ]; then
        ./evalb -p $mode.prm a4_test_sets/$i.gold results/$i.$parser | tail -n 40 > $target
      fi
    done
  done
done

#create randomized approximations
for i in `seq 1 3` all
do
  python2 createRandomizedApproximizations.py 1000 $i
  for mode in "labeled" "unlabeled"
  do
    folder="results/testcase$i"
    for round in $folder/round[AB]????
    do
      target="$round.eval.$mode"
      ./evalb -p $mode.prm a4_test_sets/$i.gold $round | tail -n 40 > $target
    done
  python2 evaluateRandomizedApproximization.py $i $mode 1000
  done
  rm -rf $folder
done




#java -mx6000m -cp "./*:" edu.stanford.nlp.parser.metrics.TaggingEval ../a4_test_sets/1.gold ../results/1.stanford

#java -mx6000m -cp "./*:" edu.stanford.nlp.parser.lexparser.FactoredParser \
# -sentences newline -tokenized -nthreads 3 -outputFormat "evalb" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ../a4_test_sets/$i.plain > ../results/$i.stanford