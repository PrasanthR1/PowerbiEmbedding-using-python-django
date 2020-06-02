# THIS DOCUMENT EXPLAINS HOW TO EMBED REPORTS USING POWERBI REST API

- First thing you need to Register your application on https://app.powerbi.com/embedsetup/appownsdata 
- Need js sdk -> powebi.js file to render your report,you can get it from here https://github.com/microsoft/PowerBIJavaScript/tree/master/dist add it to your project.
- To access rest_api and your workspace, you need to get access_token and exchange it for authorization code.

## To get access_token use post url and payload for the url :-

`payload = {
           'grant_type': 'password',
           'scope': 'openid',
           'resource': r`https://analysis.windows.net/powerbi/api`,
           'client_id': '{client id from auzre reg app}',
           'username': '{your powerbi acc}',
           'password': '{powerbi acc password}
           }`
           
          
#### POST URL : 'https://login.microsoftonline.com/common/oauth2/token',data=payload

result -> you will get access_token

## After getting access_token use it as with Bearer to get Authorization

headers = { 'Authorization' : 'Bearer ' + access_token }

#### GET URL : 'https://api.powerbi.com/v1.0/myorg/groups',headers=headers

result -> you will get workspaces Note : 'value' is the name of the workspace

##### choose the workspace which you want use (Note:put all the reports in one workspace to embed multiple reports from one ws) If you didn't provide any workspace name it will take 1st workspace as default After selecting the workspace -> get group id from that particular workspace.

## To get all reports in a particular ws: headers -> same as above

#### GET URL : https://api.powerbi.com/v1.0/myorg/groups/' + group_id + '/reports',headers=headers

result -> you will get all the reports Note : 'Value' is name of the report

## Now get embedUrl and reportId from reports

`post_data = post_data =
""" 
{ "accessLevel": "View" }
"""`

headers.update({'Content-type': 'application/json'})

#### POST URL : ('https://api.powerbi.com/v1.0/myorg/groups/' + group_id +
'/reports/' + reportId + '/GenerateToken',data = post_data, headers=headers)

result -> you will get embed_token

## Fianlly you have :- json_data = { 'embedToken' : {}, 'embedUrl' : {}, 'reportId' : {} }

send it as context to html and use it in javascript code I'm rendering multiple reports,that's why i have [{report1},{report2}],so i used report index to render particular report

           `<script type="text/javascript">
                   var models = window['powerbi-client'].models;

                           var json_data = {{json_data | safe }}
                           var embedConfiguration = {
                               id: json_data[0].reportId,
                       ``        type: 'report',
                               embedUrl: 'https://app.powerbi.com/reportEmbed',
                               tokenType: models.TokenType.Embed,
                               accessToken: json_data[0].embedToken,
                               settings: {
                                   navContentPaneEnabled: false
                               }
                           };

                           var element = document.getElementById('reportContainer');
                           var report = powerbi.embed(element, embedConfiguration); 
      </script>`
> Tips : If you want to embed multiple report and show when button is clicked,this example is so helpful for you.

<button type="button" onclick="getreport(0)" class="btn btn-primary">report1</button>

where getreport 0-> is the 1st report likewise you can access all your reports.

           `<script type="text/javascript">

                   var models = window['powerbi-client'].models;

                           var json_data = {{json_data | safe }}
                           var embedConfiguration = {
                               id: json_data[key].reportId,
                       ``        type: 'report',
                               embedUrl: 'https://app.powerbi.com/reportEmbed',
                               tokenType: models.TokenType.Embed,
                               accessToken: json_data[0].embedToken,
                               settings: {
                                   navContentPaneEnabled: false
                               }
                           };

                           var element = document.getElementById('reportContainer');
                           var report = powerbi.embed(element, embedConfiguration); 
      </script>`

## HAPPY CODING :)
