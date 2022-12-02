# reference: https://developers.google.com/youtube/v3/docs/subscriptions#resource
# reference: https://developers.google.com/youtube/v3/docs/subscriptions/insert
# reference: https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.errors-module.html

import os.path
import time
from auth import get_authenticated_service, deauthentication

import googleapiclient.errors

if __name__ == "__main__":
    # Read channel_id from "id_list.txt".
    if os.path.exists('id_list.txt'):
        with open('.\id_list.txt') as f:
            id_list = f.readlines()
        # Delete '\n'.
        id_list = [line.rstrip('\n') for line in id_list]
    else:
        print('[ERROR]: "id_list.txt" does not exist in the current directory.')
        exit()
    
    # Log in to Google with OAuth.
    youtube = get_authenticated_service()

    # Register the channel ID registered in "id_list.txt".
    # notes: About 200 registrations got stuck in quota.
    # Since "channelId" only accepts String, 
    # it was impossible to register multiple channels.
    
    for channel_id in id_list:
        try:
            request = youtube.subscriptions().insert(
                part="snippet",
                body=dict(
                    snippet=dict(
                        resourceId=dict(
                            channelId=channel_id
                            )
                        )
                    )
                )
            response = request.execute()

            print(f'[OK]: {response["snippet"]["title"]}({channel_id})')
            time.sleep(1)

        except googleapiclient.errors.HttpError as e:
            print(f'[ERROR]: {e.error_details[0]["message"]}')
        except Exception as e:
            print('[ERROR]: An unexpected error occurred.')
            deauthentication()

    deauthentication()