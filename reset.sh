rm *.html
rm *.pyc

echo "Parsing Optionmetrics Data"
rm ~/data/optionmetrics/temp/*temp
python parse_optionmetrics.py

echo ""
echo "Cleaning Weight Data"
rm ~/data/impliedCorr/FTSE_weights_from_pdf.csv
yes "" | python GetFTSEWeights.py
rm ~/data/impliedCorr/STOXX_weights_from_pdf.csv
yes "" | python GetSTOXXWeights.py

echo ""
echo "Joining Optionmetrics and Weight Data"
rm ~/data/impliedCorr/STOXXCombinedData.csv
rm ~/data/impliedCorr/FTSECombinedData.csv
python add_weights.py

echo ""
echo "Computing correlation, graphing, and regenerating the website."
python graphs.py
python website.py

echo ""
echo "Finished."

