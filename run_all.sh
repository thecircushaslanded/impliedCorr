rm *.html
rm *.pyc

echo "Parsing Optionmetrics Data"
python parse_optionmetrics.py

echo ""
echo "Cleaning Weight Data"
yes "" | python GetFTSEWeights.py
yes "" | python GetSTOXXWeights.py

echo ""
echo "Joining Optionmetrics and Weight Data"
python add_weights.py

echo ""
echo "Computing correlation, graphing, and regenerating the website."
python graphs.py
python website.py

echo ""
echo "Finished."

