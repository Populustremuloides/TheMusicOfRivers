# TheMusicOfRivers

code file | input file | output file | figure produced (if any) | Notes
-------------- | ---- | -------- | ------ | -----
map_of_catchments.py | dayOfMeanFlowThroughTime.csv | | 1 |
map_of_catchments.py | alldata.csv | | 1 |
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
