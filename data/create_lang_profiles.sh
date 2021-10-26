#!/bin/bash

for FILE in theNorthWindAndTheSun/*.txt; do
  NEW=${FILE##*\/}
  NAME=${NEW%.txt}
  cat $FILE | segments profile > "lang_profiles/${NAME}_profile.prf"
done;