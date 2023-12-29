MOODSENSE
The problem with delivering a lesson as a university professor is that you never truly know the real or close to real insight emotions or feedback which can be derived from those emotions about how the student feels about a particular professor teaching style or delivered lessons. There is often stigma among college students to not participate in evaluating these teaching related problems accurately also the threat of one or two biased experiences driving towards the false results could be a problem too. Furthermore, to evaluate and know the feedback of students is an essential brick in the wall of education industry thus Moodsense helps with collecting real time data and draw insights from it.

Installation Steps(Windows): Perform the following steps in order to install the Project onto your System:

Step 1: Create Virtual Environment:

  python -m venv env
Step 2: Activate the Environment:

env\Scripts\Activate.bat
Step 3: Clone

git clone https://github.com/prakrutipathak/MOODSENSE.git
Step 4: Install all the Packages: After Activating the Virtual Environment. For installing all the packages used for the development of this project (Note: requirements.txt will be included in the project folder.).

 pip install -r requirements.txt
Step 5: Run the below command to makemigrations

python manage.py makemigrations
Step 6: Run the below command to migrate

python manage.py migrate
Step 7: Run the below to start the server

python manage.py runserver
Changes you should make in the settings.py file:

#Gmail SMTP
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your email id'
EMAIL_HOST_PASSWORD = 'Your app password'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
