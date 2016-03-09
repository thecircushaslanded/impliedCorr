rm *.html
rm *.pyc

echo "Downloading yesterday's data."
/opt/anaconda/bin/python ~/python_modules/optionmetrics/obtain.py

echo "Parsing Optionmetrics data."
/opt/anaconda/bin/python ~/Projects/impliedCorr/parse_optionmetrics.py

# echo ""
# echo "Cleaning weight data."
# yes "" | python GetFTSEWeights.py
# yes "" | python GetSTOXXWeights.py


echo ""
echo "Joining Optionmetrics and weight data."
/opt/anaconda/bin/python ~/Projects/impliedCorr/add_weights.py

echo ""
# echo "Computing correlation, graphing, and regenerating the website."
echo "Computing correlation and updating graphs."
/opt/anaconda/bin/python ~/Projects/impliedCorr/graphs.py

# /opt/anaconda/bin/python website.py


echo ""
echo "Finished."

