import calls

def BuildDataSourceString(sourceName, typeName,
                          threshold = calls.RRD_THRESHOLD,
                          sampleMin = calls.RRD_UNKNOWN,
                          sampleMax = calls.RRD_UNKNOWN):

    return 'DS:{0}:{1}:{2}:{3}:{4}'.format(sourceName, 
        typeName, threshold, sampleMin, sampleMax)

