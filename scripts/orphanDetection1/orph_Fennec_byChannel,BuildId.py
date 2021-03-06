import json
import jydoop
import healthreportutils_v3
import random


'''
in following commands, UPDATE DATES

----to run against HDFS sample of ALL v3 records (extract created by anurag in HDFS at /user/aphadke/temp_fennec_raw_dump)


---HDFS dump of all Fennec records to HDFS summary
make ARGS="scripts/orph_Fennec_byChannel,BuildId.py ./outData/orph_Fennec_byChannel,BuildId_2013-10-28 /user/aphadke/temp_fennec_raw_dump/part*" hadoop


SAVE OUTPUT TO HDFS, then need to PROCESS WITH e.g:
make ARGS="scripts/orph_Fennec_byChannel,BuildId_process.py ./outData/orph_Fennec_byChannel,BuildId_extraInfo_2013-10-25.csv /user/bcolloran/outData/orph_Fennec_byBuildId_extraInfo_2013-10-25/part*" hadoop


'''

######## to OUTPUT TO HDFS from RAW HBASE
# make ARGS="scripts/orph_Fennec_byBuildId.py /user/bcolloran/outData/orph_Fennec_byBuildId_extraInfo_2013-10-25" hadoop
def skip_local_output():
    return True



def setupjob(job, args):
    """
    Set up a job to run on one or more HDFS locations

    Jobs expect one or more arguments, the HDFS path(s) to the data.
    """
    import org.apache.hadoop.mapreduce.lib.input.FileInputFormat as FileInputFormat
    import org.apache.hadoop.mapreduce.lib.input.SequenceFileAsTextInputFormat as MyInputFormat

    if len(args) < 1:
        raise Exception("Usage: <hdfs-location1> [ <location2> ] [ <location3> ] [ ... ]")

    job.setInputFormatClass(MyInputFormat)
    FileInputFormat.setInputPaths(job, ",".join(args));
    job.getConfiguration().set("org.mozilla.jydoop.mappertype", "TEXT")
    # set the job to run in the RESEARCH queue
    job.getConfiguration().set("mapred.job.queue.name","research")


# setupjob = healthreportutils_v3.setupjob



@healthreportutils_v3.FHRMapper()
def map(key, payload, context):

    if payload.version!=3:
        return


    channel = payload._o.get('environments', {}).get('current', {}).get('geckoAppInfo',{}).get('updateChannel','no_channel')

    if channel not in ['nightly','aurora','beta','release']:
        channel = "minor_channel"




    try:
        firstDay = payload.days[0]
    except IndexError:
        context.write((channel,"no_firstDay"),1)
        return


    try:
        firstDayFirstEnvir = payload._o.get('data', {}).get('days', {}).get(firstDay,{}).keys()[0]
    except IndexError:
        context.write((channel,"no_firstDayFirstEnvir"),1)
        return


    try:
        firstDayFirstEnvirAppSession = payload._o.get('data', {}).get('days', {}).get(firstDay,{}).get(firstDayFirstEnvir,{})["org.mozilla.appSessions"]
    except KeyError:
        context.write((channel,"no_firstDayFirstEnvirAppSession"),1)
        return


    try:
        buildId = payload._o['environments']['current']['geckoAppInfo']['appBuildID']
    except KeyError:
        context.write((channel,"no_buildId"),1)
        return




    if firstDayFirstEnvirAppSession=={}:
        context.write((channel,"empty_firstDayFirstEnvirAppSession"),1)
        return
    else:
        firstDayDataStr = str(payload._o.get('data', {}).get('days', {}).get(firstDay,{}))
        context.write( (channel,hash((firstDay,firstDayDataStr))), buildId)
        return









def reduce(key,vIter,context):

    channel = key[0]

    if key[1] in ["no_firstDay","no_firstDayFirstEnvir","no_firstDayFirstEnvirAppSession","empty_firstDayFirstEnvirAppSession"]: # if we get an error codes, count them up
        context.write((channel,key[1]),sum(vIter))
        return


    else: #if we don't get an error code, if there is more than one thisPingDate associated with the fingerprint, emit all thisPingDates for the fingerprint.
        buildIdList = list(vIter)
        if len(buildIdList)>1:
            context.write((channel,key[1]),buildIdList)
            return
        else:
            context.write((channel,"recordWithUniquePrint"),1)
            return





