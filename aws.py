from urllib.request import urlopen
import json
import boto3
import time

# The audio file should be uploaded in a Bucket, in the AWS, read 'Read Me' for more


def check_job_name(job_name):  # to check if the job with this name exits

    job_verification = True  # Assuming there's no job name, similar
    existed_jobs = transcribe.list_transcription_jobs()

    for job in existed_jobs['TranscriptionJobSummaries']:

        if job_name == job['TranscriptionJobName']:
            job_verification = False
            break

    if not job_verification:
        command = input(job_name + " has existed.\nDo you want to override the existed job (Y/N): ")

        if command.lower() == "y" or command.lower() == "yes":
            transcribe.delete_transcription_job(TranscriptionJobName=job_name)

        elif command.lower() == "n" or command.lower() == "no":
            job_name = input("Insert new job name? ")
            check_job_name(job_name)

        else:
            print("Input can only be (Y/N)")
            command = input(job_name + " has existed. \nDo you want to override the existed job (Y/N): ")

    return job_name


def amazon_transcribe(file, max_speakers=-1):
    if max_speakers > 10:
        raise ValueError("Maximum detected speakers is 10.")

    #job_uri = "s3://{}/{}"
    #job_uri.format(bucket, file)
    job_name = (file.split('.')[0]).replace(" ", "")

    # check if name is taken or not
    job_name = check_job_name(job_name)

    if max_speakers != -1:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat=file.split('.')[1],
            LanguageCode='en-US',  # English to Us works the best
            Settings={'ShowSpeakerLabels': True,
                      'MaxSpeakerLabels': max_speakers})

    else:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat=file.split('.')[1],
            LanguageCode='en-US',
            Settings={'ShowSpeakerLabels': True})

    while True:

        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)

        if job['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

        print('Audio File not transcribed yet...')
        time.sleep(15)

    if job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':

        print('Transcription Done.')

        response = urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        data = json.loads(response.read())
        text = data['results']['transcripts'][0]['transcript']

        with open('transcriptions/aws_transcription.txt', 'w') as f:  # writing the transcription on to a text file
            f.write(text)

    return job


def run(access_key, secret_key, file):

    global transcribe
    global bucket
    global job_uri

    transcribe = boto3.client('transcribe',
                              aws_access_key_id=access_key,  # insert your access key ID here,
                              aws_secret_access_key=secret_key,  # insert your secret
                              region_name="ap-south-1")  # region: Mumbai south"

    bucket = input('Enter bucket name: ')
    job_uri = f"s3://{bucket}/{file}"

    amazon_transcribe(file_name, 5)


if __name__ == '__main__':
    access_key = input('Enter your AWS access key ID: ')
    secret_key = input('Enter your AWS secret access key: ')
    file_name = input('Enter file name: ')

    run(access_key, secret_key, file_name)
