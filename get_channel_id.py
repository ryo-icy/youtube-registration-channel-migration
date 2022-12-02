# reference: https://developers.google.com/youtube/v3/docs/subscriptions#resource
# reference: https://developers.google.com/youtube/v3/docs/subscriptions/list

import math
from auth import get_authenticated_service, deauthentication

id_list: list = []
counter: int = 0
if __name__ == "__main__":
    # Log in to Google with OAuth.
    youtube = get_authenticated_service()

    # Get channel_id.
    request = youtube.subscriptions().list(
        part="snippet",
        mine=True,
        maxResults=50
        )
    response = request.execute()

    # Save channel_id to the list.
    for item in response['items']:
        id_list.append(item['snippet']['resourceId']['channelId'])

    counter = math.ceil((int(response['pageInfo']['totalResults'])/50) - 1)
    for d in range(0, counter):
        request = youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=response['nextPageToken']
            )
        response = request.execute()

        for item in response['items']:
            id_list.append(item['snippet']['resourceId']['channelId'])

    # Save the obtained channel_id in "id_list.txt".
    with open('id_list.txt','w') as f:
        f.writelines([d+"\n" for d in id_list])

    deauthentication()