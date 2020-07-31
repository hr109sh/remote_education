## Getting Started

By following the tutorial, you'll set up a development environment, deploy an app locally on IBM Cloud, and integrate a database service in your app.

[Project website](https://github.com/hr109sh/remote_education)

### Before you begin

You'll need the following:

* [IBM Cloud Account](https://cloud.ibm.com/registration)
* [IBM Cloud CLI](https://cloud.ibm.com/docs/cli/reference/ibmcloud?topic=cloud-cli-install-ibmcloud-cli)
* [Python](https://www.python.org/downloads)
* [Git](https://git-scm.com/downloads)

### Step 1: Clone the sample app

First, clone the repo and change to the directory where the app is located.

```bash
git clone https://github.com/hr109sh/remote_education
```

```bash
cd remote_education
```

Peruse the files in the remote_education directory to familiarize yourself with the contents.

### Step 2: Run the app locally

Install the dependencies listed in the [requirements.txt](https://github.com/hr109sh/remote_education/blob/master/requirements.txt) file to be able to run the app locally.

You can optionally use a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.

```bash
pip install -r requirements.txt
```

Alternatively with Python3 you can issue

```bash
python3 -m pip install -r requirements.txt
```

Run the app.

```bash
python manage.py runserver
```

View your app at: http://localhost:8000

### Step 3: Prepare the app for deployment

To deploy to IBM Cloud, it can be helpful to set up a manifest.yml file. The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. We've provided a sample manifest.yml file in the get-started-python directory.

Open the manifest.yml file, and change the name from remote-e to your app name, app_name. Change the http_proxy and https_proxy to your host url.

```bash
  applications:
 - name: remote-e
   command: pip install --upgrade pip
   command: pip install django==2.0.5
   command: ibmcloud cf set-env remote-e http_proxy "http://remote-e.eu-gb.mybluemix.net:8080"
   command: ibmcloud cf set-env remote-e https_proxy "https://remote-e.eu-gb.mybluemix.net:8081"
   command: ibmcloud cf map-route remote-e remote-e.eu-gb.mybluemix.net --port 8080
   command: python3 manage.py runserver
   random-route: true
   memory: 256M
env:
  DISABLE_COLLECTSTATIC: 1
```

### Step 4: Deploy the app

You can use the IBM Cloud CLI to deploy apps.
Log in to your IBM Cloud account, and select an API endpoint.

```bash
ibmcloud login
```

If you have a federated user ID, instead use the following command to log in with your single sign-on ID. See Logging in with a federated ID for more information.

```bash
ibmcloud login --sso
```

Target a Cloud Foundry org and space:

```bash
ibmcloud target --cf
```

From within the remote_education directory push your app to IBM Cloud

```bash
ibmcloud cf push remote-e -b https://github.com/cloudfoundry/python-buildpack.git -c "python3 manage.py runserver 0.0.0.0:8080" -u none
```

This can take a minute. If there is an error in the deployment process you can use the command ibmcloud cf logs <Your-App-Name> --recent to troubleshoot.

When deployment completes you should see a message indicating that your app is running. View your app at the URL listed in the output of the push command. You can also issue the following command to view your apps status and see the URL.

```bash
ibmcloud cf apps
```

You can also go to the IBM Cloud [resource list](https://cloud.ibm.com/resources) to view your app.

### Step 5: Add a database

Next, we'll add an IBM Db2 on Cloud database to this application and set up the application so that it can run locally and on IBM Cloud.

1. In your browser, log in to IBM Cloud and go to the Dashboard. Select Create resource.
2. Search for IBM Db2, and select the service.
3. Select a DB on Flex plan or above. (Lite Plan is unsupported for migration). Provide a Service Name.  You can leave the default settings for the other fields. Click Create to create the service.
4. In the navigation, go to Service Credentials, then click New Credentials and click Add.


### Step 6: Migrate the database

Django has a built in database which needs to be migrated to IBM Db2 on Cloud database.

1. Find your app in the IBM Cloud [resource list](https://cloud.ibm.com/resources). On the Service Details page for your app, click Connections in the sidebar. Click the IBM Db2 on Cloud menu icon (…) and select View credentials.

2. Copy and paste the db, username, password, host and port from the credentials to the same fields replacing NAME, USER, PASSWORD, HOST and PORT.

3. Follow the steps to perform the migration - [Getting started with IBM DB Django adapter](https://github.com/ibmdb/python-ibmdb-django/blob/master/README.md)

4. Run your application locally.

```bash
python manage.py runserver
```

View your app at: http://localhost:8000. Any names you enter into the app will now get added to the database.

Your local app and the IBM Cloud app are sharing the database. View your IBM Cloud app at the URL listed in the output of the push command from above. Names you add from either app should appear in both when you refresh the browsers.
