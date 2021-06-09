# Panel App Heroku Template
### Template Repo to deploy python panel app on heroku

[![hackmd-github-sync-badge](https://hackmd.io/0CmslwnjTCK8S1hATlUnNQ/badge)](https://hackmd.io/ApPMBo0_QSG5AM0Rs_qThg)
---

To run locally:

First activate your virtual environment and install the requirements. Then:

`panel serve augmentedbondingcurve/app.py --auto --show`

To get started working with Heroku [signup](https://signup.heroku.com/) for a free account and [download and install the CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up). Once you are set up follow the instructions to log into the CLI.

1. Clone this repository

2. Add a Jupyter notebook or Python script which declares a Panel app along with dependent files to the repository.

 
3. Try running the panel app locally using this repo's environmemt before deploying. As Heroku allows only few pushes to the app. Update requirements.txt if necessary.
 
4. Create a heroku app using the CLI. This would generate URL for app and github:
```
heroku create app-name
```

5. Modify the `Procfile` according to your app: 
    - `model/app.py` with servable panel app 
    - `app-name.herokuapp.com` which you generated in the above step

6. Set github remote to push to heroku. Use git URL from step 3

```
git remote add heroku https://git.heroku.com/app-name.git 
```

5. Git Commit and Push the app to heroku and wait until it is deployed:

```
git add .
git commit -m "init"
git push heroku master
```

6. Visit the app at app-name.herokuapp.com

Modify the Procfile which declares which command Heroku should run to serve the app. In this sample app the following command serves the app.py example and the websocket origin should match the name of the app on Heroku app-name.herokuapp.com which you will declare in the next step:

`web: panel serve --address="0.0.0.0" --port=$PORT model/app.py --allow-websocket-origin=app-name.herokuapp.com`

### To distribute as package
	
1. Install setuptools and twine  
```
pip install setuptools twine
```

2. Check if any metadata are missing

```
python setup.py check
```

3. Create a source distribution

```
python setup.py sdist
```

4. Upload it to PyPI. You will need an registered account at  https://pypi.python.org  
```
twine upload dist/*
```

### Credits:
> https://panel.holoviz.org/user_guide/Server_Deployment.html

> https://github.com/holoviz-demos/minimal-heroku-demo/blob/master/README.md

> https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/
