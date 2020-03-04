#!/bin/bash

echo "Hello"
repos="$(find `pwd` -mindepth 1 -maxdepth 1 -type d)"
for r in $repos;
do
  echo $r
  /Users/isabellaferreira/Dropbox/PhD/Winter2020/ECSE611_SoftwareAnalytics/replication/pmd-bin-6.21.0/bin/run.sh cpd --minimum-tokens 150 --files $r --language pp --format xml >> $r/cpd.xml
done
