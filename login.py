import constants
import oauth2, urllib.parse as urlparse, json
from user import User
from database import Database
# request, authorize, access
##### step 1. create consumer
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)


##### step 2. create a request using client
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')

if response.status!=200:
    print("an error occurred")

#### step 3. translate the response
request_token = dict(urlparse.parse_qsl(content.decode('UTF-8')))

print("Go to the following site in your browser")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

oauth_verifier = input("What is the PIN? ")

token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth2.Client(consumer, token)

response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
# converts bytes to string
access_token = dict(urlparse.parse_qsl(content.decode('UTF-8')))

print(access_token)


# require user input
email = input('Enter email: ')
firstname = input('Enter firstname: ')
lastname = input('Enter lastname: ')
# create user object
user = User(email, firstname, lastname, access_token['oauth_token'], access_token['oauth_token_secret'],None)

Database.initialise(dbname="learning", user="postgres", password="P@ssw0rd", host="localhost");
User.save_to_db(user)




authorized_token = oauth2.Token(access_token['oauth_token'],
                                access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')

if response.status!=200:
    print("an error occurred")

tweets = json.loads(content.decode('utf-8'))


for tweet in tweets['statuses']:
    print(tweet['text']) # because it's a dictionary