#Part 1: Data exploration
# 1.1
cat data/Land_and_Ocean_summary.txt | tail +49 | wc -l
 
#Part 4: CO2 emission
# 4.1
cat data/annual-co-emissions-by-region.csv | grep [,][A-Z][A-Z][A-Z][,] | sort -r -n -t',' -k3,3 -k4 | head >> top10_CO2.csv 
