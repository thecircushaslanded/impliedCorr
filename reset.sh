echo "Cleaning Optionmetrics Data"
rm ~/data/optionmetrics/Selection*
python clean_optionmetrics.py

echo ""
echo "Cleaning Weight Data"
rm ~/data/impliedCorr/weights_from_pdf.csv
yes "" | python GetMostRecentWeights.py

echo ""
echo "Joining Optionmetrics and Weight Data"
rm ~/data/impliedCorr/CombinedData.csv
rm ~/data/impliedCorr/Index.csv
python JoinDatasets.py

echo ""
echo "Computing Correlation and graphing"
rm ~/data/impliedCorr/ImpliedCorr.csv
rm *.html
python ComputeCorr.py

echo ""
echo "Finished."

