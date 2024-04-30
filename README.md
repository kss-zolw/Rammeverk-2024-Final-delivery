# Webscraper - Kristoffer Snopestad Søderkvist
**GITHUB LINK TO SCRAPER:https://github.com/kss-zolw/Rammeverk-2024-Final-delivery**
### How to run:

This webscraper is tested with Python version 3.12.3
Some packages and code will probably work with older versions of python, but that has not been tested.

Steps to get the webscraper up and running:

* Unzip to a suitable location on your computer.
* Open a terminal in the unzipped folder
* create a python virtual environment
````
> python3 -m venv venv
````
* activate the virtual environment 
````
Visual Studio Code will activate it with a message popup.
# or run this:
> /venv/Scripts/activate.ps1
# or
> /venv/Scripts/activate.bat
# or
This is an explanation on how to do this in Visual Studio Code:
1. Go to Extensions or press Ctrl+Shift+X Search Python and look for one published by Microsoft
2. Open a .py file or create a new one.
3. Ctrl+Shift+P and type Python:Select Interpreter
4. This could be a global one or the venv (virtual enviroment) That is acivated above.

After this it will display (venv) PS C:....USERNAME\etc.... in the powershell window (Sometimes it does not display (venv) and I dont know why. So it is a bit random)
````
If you are on unix systems (PS: I havent tested this, just read about it so I am not 100% sure this works.)
````
> source venv/bin/activate
````
* install python dependencies to the virtual environment
````
(venv) > pip3 install -r requirements.txt
````
pip list to check if all packages is installed and what versions packages have.
Should also be able to pip install into the dist folder to use the .tar.gz file as a packages for other projects.
This will be like installing all other libaries and adding it to your new project
