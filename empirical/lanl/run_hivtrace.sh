#!/bin/bash

NAME="LANL"

INPUT="raw_reference.fas"

FILTER_RESULTS="./$NAME.results.json" 
FILTER_LOG="./$NAME.results.log"
NOFILTER_RESULTS="./$NAME.nofilter.results.json" 
NOFILTER_LOG="./$NAME.nofilter.results.log"
CYCLE_RESULTS="./$NAME.cycle.results.json"
CYCLE_REPORT="./$NAME.cycle_report.json" 
CYCLE_LOG="./$NAME.cycle.results.log"

# Edge Filtering
time hivtrace --do-not-store-intermediate -i $INPUT -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o $FILTER_RESULTS --log $FILTER_LOG

# No Filtering
time hivtrace --do-not-store-intermediate -i $INPUT -a resolve -r HXB2_prrt -t .015 -m 500 -g .05 -o $NOFILTER_RESULTS --log $NOFILTER_LOG

# Cycle Filtering
time hivtrace --do-not-store-intermediate -i $INPUT -a resolve -f remove -r HXB2_prrt -t .015 -m 500 -g .05 -o $CYCLE_RESULTS --filter-cycles --cycle-report-fn $CYCLE_REPORT --log $CYCLE_LOG
