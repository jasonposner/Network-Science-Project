# Music Collaboration Network

## Setting Up Spotipy
Run:

util.prompt_for_user_token(username,
                         scope,
                         client_id='your-spotify-client-id',
                         client_secret='your-spotify-client-secret',
                         redirect_uri='your-app-redirect-url')

And fill in each value as follows:

username - the spotify username used to log on
scope - the "scope" of power the application ges. Ex: user-library-read
client_id - given by spotify web dev portal
client_secret - given by spotify web dev portal
redirect_uri - can be localhost

May need to set up environment variables by running the following in bash:

export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
