# TheMusicOfRivers


## Data Availability

The raw data files used in this analysis are currently published on Research Gate [here](https://doi.org/10.13140/RG.2.2.31696.84487) and [here](https://doi.org/10.13140/RG.2.2.24985.95842). The methods used for generating these data can be found in [this preprint](https://doi.org/10.1002/essoar.10507854.1).

## Dependencies

The Python code was executed using version 3.7.1. To run the code, you will need the following packages installed in your environment:

- pandas 1.2.3
- scipy 1.6.2
- numpy 1.19.2
- matplotlib 3.3.4
- seaborn 0.11.1
- sklearn 0.24.1

In addition, the code uses the following native libraries:
- math
- os

R code was executing using version 3.6.1. R libraries used include the following:
- WaveletComp 1.1

code file | input file | output file | figure produced (if any) | Notes
-------------- | ---- | -------- | ------ | -----
map_of_catchments.py | dayOfMeanFlowThroughTime.csv | | 2 |
map_of_catchments.py | alldata.csv | | 2 |
correlateSpectralWithSelf.py | universallyAligned_powers.csv | | 4 |
visFreqPlace.R | long_matrix_temp_order_seas_prec.csv | | 6 |
meanFrequencyDecomp.py | alldata.csv | long_matrix_temp_order_seas_prec.csv | 
meanFrequencyDecomp.py | FullDatabase.csv | long_matrix_temp_order_seas_prec.csv | 
meanFrequencyDecomp.py | universallyAligned_powersTranpose.csv | long_matrix_temp_order_seas_prec.csv | 
analyzeCorrelations.py | universallyAligned_powersTranpose.csv | | 9, S2, S3, S8, S15 | 
analyzeCorrelations.py | FullDatabase.csv | | 9, S2, S3, S8, S15 |
analyzeCorrelations.py | frequency_to_flow_metrics_r_all_jan2021_universally_aligned.csv | | 9, S2, S3, S8, S15 |
plotHuman.py | ml_importances_with_categories.csv | | 10 |
ml_visualize_predict_flow_metrics.py | ml_predict_flow_metrics_feature_importances_wide.csv | | S4, S5 |
humanPlotPrepPVals.py | ml_r_squared.csv |  | S16 | 
ml_predict_flow_metrics.py | universallyAligned_powers.csv, alldata.csv | ml_predict_flow_metrics_feature_importances_wide.csv | |
humanPlotPrep.py | ml_feature_importances_short.csv | | |
machineLearning.py | universallyAligned_powers.csv, alldata_hemisphereCorrected.csv | ml_feature_importances_short.csv, ml_r_squared.csv | |
dayOfMeanFlowThroughTime.py | alldata.csv | dayOfMeanFlowThroughTime.csv |  |
spectralThroughTime.py | alldata.csv | spectralPowersThroughTime.csv |  |
splitIntoNonGlobalWaterYears.py | alldata.csv | localWaterYear |  |
plotSpectralNumberThroughTime.py | day_of_mean_flow_vs_size.csv | spectralNumber_acrossTime.csv |  |
combineThroughTime.py | dayOfMeanFlowThroughTime.csv | throughTimeCombined.csv |  |
testDifferenceInDayOfMeanFlow.py | FullDatabase.csv | day_of_mean_flow_vs_size.csv |  |
testDifferencesInMean.py | FullDatabase.csv | specific_discharge_vs_size.csv |  | Convert discharge to specific disharge data
convertToSpecificDischarge.py | localWaterYear | localWaterYear |  | converts to specific discharge
dayOfMeanFlowThroughTime.py | localWaterYear | dayOfMeanFlowThroughTime.csv |  |
example_spectral_properties_hydrographs.py | localWaterYear |  |  |
specificDischargeThroughTime.py | localWaterYear | specificDischargeThroughTime.csv |  |
splitIntoNonGlobalWaterYears.py | localWaterYear | universallyAlignedGlobalFlow_DailyQ2_column.csv |  |
WaveletAnalysisLocalWaterYear.R | localWaterYear | localWaterYearSpectralDecomposition |  |
compressTemporalPatternsPreprocess.py | localWaterYearSpectralDecomposition | ml_all_years_data_separate.csv |  | create dataset for dimensionality compression
example_spectral_properties_hydrographs.py | localWaterYearSpectralDecomposition |  |  |
spectralThroughTime.py | localWaterYearSpectralDecomposition | spectralPowersThroughTime.csv |  |
testDifferenceInDayOfMeanFlow.py | localWaterYearSpectralDecomposition | day_of_mean_flow_vs_size.csv |  |
testDifferencesInMean.py | localWaterYearSpectralDecomposition | specific_discharge_vs_size.csv |  |
compressTemporalPaternsSlope.py | ml_all_years_data_separate.csv | ml_slope_encodings1.csv |  |
combineThroughTime.py | ml_slope_encodings1.csv | throughTimeCombined.csv |  |
example_spectral_properties_hydrographs.py | ml_slope_encodings1.csv |  |  |
plotSpectralNumberThroughTime.py | ml_slope_encodings1.csv | spectralNumber_acrossTime.csv |  |
plotSpectralNumberThroughTime.py | specific_discharge_vs_size.csv | spectralNumber_acrossTime.csv |  |
combineThroughTime.py | specificDischargeThroughTime.csv | throughTimeCombined.csv |  |
dimensionalityCompression.py | universallyAligned_powers.csv | ml_encodings1.csv |  |
WaveletAnalysisGlobal.R | universallyAlignedGlobalFlow_DailyQ2_column.csv | universallyAligned_powers.csv |  |
WaveletAnalysisGlobal.R | universallyAlignedGlobalFlow_DailyQ2_column.csv | universallyAligned_powersTranspose.csv |  |
