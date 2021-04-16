# Before running the scripts, make sure to install all the requirements in requirements.txt.

This is a Speech-to-text command line application, which transcribes audio from a audio file. Built with the help of AWS API and Assembly AI API. This application contains exactly two Python scripts which are essentialy
two ways to transcribe and process the audio file.

Method 1: (Using AWS and Boto3 API)
	Firstly, for this way to work to need to sign up for aws console and create a bucket, upload files that needs to be transcribed. YOU NEED HAVE YOUR OWN "AWS Acess Key" and "AWS Secret Key".
	Command line simply asks you to enter your keys, bucket name, audio file's name and creates a job. If the name of the job exist, it ask to either override it or create a new one. Later it transcribe the audio and 
	store the transcription in a local directory called 'transcriptions' on your machine.

	For more suggestions on how this application could improve check: suggestions.txt

Method 2: (Assembly AI API)

	Assembly AI, is a free Speech to Text API that transcribes and process audio files. You type the full location of your file and it uploads the audio file to a secure place, starts to do the transcription and get the transcription
	as a text file on your local machine.

	
Requirements:
-->  Before running the scripts, make sure to install all the requirements in requirements.txt.
-->  YOU NEED TO HAVE YOUR OWN "AWS Acess Key" and "AWS Secret Key" if using the aws.py

	
	