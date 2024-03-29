# Slack-Hive
A prototype productivity app for Slack

Rationale: A large amount of knowledge within the organization is considered 'tribal': unwritten rules and information known by few individuals that is constantly being accumulated. These pieces of information are usually memorized or written down on paper so although they have the potential to bring value to another, little or none of it is shared. Platforms like Confluence or Sharepoint as a central repository of data work well when utilized but can be impractical or cumbersome for recording small tidbits of data which would either not warrant a full page or deemed not worth the time to be recorded. (Plus people are lazy!) These tidbits can be written down by their collector which provides a reliable reference for the future, but requires time-consuming manual lookup. A digital file can utilize much faster lookup times but files are not often shared and still require regular updating.

A better solution would be to use an existing rapidly accessible platform, like Slack, to store tidbits and retrieve data about a particular issue. The information can be held centrally as to be cross-functional and shared by all, with searches favoring one's team or role. For data storage, the ELK stack can be used (Elasticsearch, Kibana, Logstash) as search and indexing operations are already baked-in. A python flask server handles the processing between the two.

* Front End: Slack
* Back End: Python Flask Server 
* Data: ELK 

Packages are handled by pipenv (you should be using it if you aren't!)
* pipenv install
* pipenv shell

Design Pattern Used:
* Facade
* Command
* Singleton (as best as it can be in Python)

### Screenshots
<p align="center">
 <img src="https://user-images.githubusercontent.com/8539492/37557057-3ad23dea-29d5-11e8-9a31-28dd64d1bf0b.PNG" width="200"/>
 <img src="https://user-images.githubusercontent.com/8539492/37557058-3ae2ac8e-29d5-11e8-8dbb-509c2eda2893.PNG" width="200"/>
 <img src="https://user-images.githubusercontent.com/8539492/37557059-3af1d268-29d5-11e8-9bd0-82f1b60d3958.PNG" width="200"/>
 <img src="https://user-images.githubusercontent.com/8539492/37557060-3b01731c-29d5-11e8-8be3-718963e12265.PNG" width="200"/>
 <img src="https://user-images.githubusercontent.com/8539492/37557061-3b1182f2-29d5-11e8-9fdd-2e76e2d2f8c9.PNG" width="200"/>
</p>

### Setup - Windows
Instructions and scripts for backend setup are provided in the "install.txt" file within the tools/windows folder for the backend and data layer.  

Setting up a Slack app in browser requires admin permissions on a slack space. To connect to the backend server, you'll need to:
* Create a Slack app by signing into the Slack workspace in browser, then grab the App Credentials when created to fill the export_secrets Powershell script in the setup folder of this repo. 
* Start the server so that the URLs provided to the application can be automatically tested. 
* Enabled Interactive Components on the Slack app control panel in browser, with the reguest URL given to the ngrok  (or hosted) endpoint under the following url to handle interactive messages:

>https://ENDPOINTHERE/slack/message_actions

* Event Subscriptions should also be enabled with the following URL to enable subscriptions to workspace events:

>https://ENDPOINTHERE/slack/events

* Finally, a Bot User is required to be created to handle interactions with the user. Any user name is allowed. 
* Install the app into the Slack space using the Install App heading of the web control panel and you're good to go.
