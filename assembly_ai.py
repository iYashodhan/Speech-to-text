import os
import requests
import json
import time


API_URL = "https://api.assemblyai.com/v2/"  # Assembly AI API, url
CDN_URL = "https://cdn.assemblyai.com/"


def upload_file_to_api(file):

    """Checks for a valid file and then uploads it to AssemblyAI
    so it can be saved to a secure URL that only that service can access.
    When the upload is complete we can then initiate the transcription
    API call. Returns the API JSON if successful, or None if file does not exist.
    """
    if not os.path.exists(file):
        return None

    def read_file(file, chunk_size=5242880):

        with open(file, 'rb') as check_file:
            while True:
                data = check_file.read(chunk_size)

                if not data:
                    break

                yield data

    headers = {'authorization': os.getenv("ASSEMBLYAI_KEY")}
    response = requests.post("".join([API_URL, "upload"]), headers=headers,
                             data=read_file(file))

    return response.json()


def initiate_transcription(file_id):
    """Sends a request to the API to transcribe a specific
    file that was previously uploaded to the API. This will
    not immediately return the transcription because it takes
    a moment for the service to analyze and perform the
    transcription, so there is a different function to retrieve
    the results.
    """
    endpoint = "".join([API_URL, "transcript"])

    w_json = {"audio_url": "".join([CDN_URL, "upload/{}".format(file_id)])}

    headers = {
        "authorization": os.getenv("ASSEMBLYAI_KEY"),
        "content-type": "application/json"
    }

    response = requests.post(endpoint, json=w_json, headers=headers)

    return response.json()


def get_transcription(transcription_id):  # Requests the transcription from the API and returns the JSON response.

    endpoint = "".join([API_URL, "transcript/{}".format(transcription_id)])

    headers = {"authorization": os.getenv('ASSEMBLYAI_KEY')}
    response = requests.get(endpoint, headers=headers)

    return response.json()


if __name__ == "__main__":

    file_location = input('Enter file name (full path on your machine): ')

    response_json = upload_file_to_api(file_location)
    time.sleep(15)  # To make the server take some time before we send another request

    file_id = ''
    if not response_json:
        print("file does not exist, try again")
        exit()

    else:
        print("File uploaded to URL: {}".format(response_json['upload_url']))

        upload_url = str(response_json['upload_url'])
        file_id = upload_url.replace("https://cdn.assemblyai.com/upload/", "") # Retrieving the ID from the Url

        print("The file id: {}".format(upload_url))

    j_data = json.load(initiate_transcription(file_id))

    transcription_id = j_data["id"]
    print("The transcription ID is: {}".format(transcription_id))

    response_json = get_transcription(transcription_id)

    result = ''
    if response_json['status'] == "completed":

        for word in response_json['words']:
            result += word['text']

    else:
        print("current status of transcription request: {}".format(
            response_json['status']))

    print('Process completed.')

    with open('transcriptions/aai_transcription.txt', 'w') as file:
        file.write(result)
