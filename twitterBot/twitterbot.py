from requests_oauthlib import OAuth1Session
import os
import json
import sys


consumer_key ="kiFgKySL4aEzz5SNVaJSiYDpq"
consumer_secret ="xg4CjzjPh9DUiGP4XUEDyTtztNbbzfK6drW5GqyAHtVJKh6bIl"

request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "Girdiğiniz consumer_key yada consumer_secret hatalı."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Buradan yetki verin :  %s" % authorization_url)
verifier = input("Pin'i giriniz :  ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

while True:
    komut = input("İşlem seçiniz (Tweet atmak için 'tweetat', tweet silmek için 'tweetsil', Uyuglamadan çıkmak için'çık'): ")

    if komut == "tweetat":
        payload = {"text": "test"}  # Adjust the tweet text as needed

        # Set up OAuth1Session
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Send the POST request to Twitter's API to create a tweet
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )

        # Check if the tweet was posted successfully (201 status code indicates success for POST)
        if response.status_code != 201:
            raise Exception(
                "Bir hata oluştu: {} {}".format(response.status_code, response.text)
            )

        print("Tweet Oluşturuldu!")
        print("Yanıt kodu : {}".format(response.status_code))

        # Print the response as JSON (tweet data)
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))

    elif komut == "tweetsil":
        # Handle deleting a tweet
        tweet_id = input("Silinecek tweet id'sini yazınız: ")
        
        # Set up OAuth1Session
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

        # Send the DELETE request to Twitter's API to delete the tweet
        response = oauth.delete(
            f"https://api.twitter.com/2/tweets/{tweet_id}"
        )

        # Check if the tweet was deleted successfully (200 status code indicates success for DELETE)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        print("Tweet Silindi!")
        print("Response code: {}".format(response.status_code))

        # Print the response as JSON (confirmation of the delete action)
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))

    elif komut == "çık":
        print("Program Kapatılıyor...")
        break  # Exit the loop and terminate the program

    else:
        print("Geçersiz komut. Tekrar deneyiniz.")




   










        

