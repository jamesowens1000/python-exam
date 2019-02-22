from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData, pageType, userEmail):
        errors = {}

        if pageType == 'registration':  #Registration Checks
            pattern = re.compile("^[A-Za-z]+$")
            
            if len(postData['reg-fname']) < 1:
                errors['reg-fname'] = "First Name is a required field"
            elif len(postData['reg-fname']) < 2:
                errors['reg-fname'] = "First Name must be at least 2 characters"
            elif not pattern.match(postData['reg-fname']):
                errors['reg-fname'] = "First Name must only contain letters"
            
            if len(postData['reg-lname']) < 1:
                errors['reg-lname'] = "Last Name is a required field"
            elif len(postData['reg-lname']) < 2:
                errors['reg-lname'] = "Last Name must be at least 2 characters"
            elif not pattern.match(postData['reg-lname']):
                errors['reg-lname'] = "Last Name must only contain letters"
            
            pattern = re.compile("^[^\s@]+@[^\s@]+\.[^\s@]+$")

            if len(postData['reg-email']) < 1:
                errors['reg-email'] = "Email is a required field"
            elif not pattern.match(postData['reg-email']):
                errors['reg-email'] = "Please enter a valid email address! \n Example: joe.smith@email.com"
            
            checkEmail = User.objects.filter(email=postData['reg-email'])
            if checkEmail:
                errors['reg-email'] = "A user with this email is already registered. Please enter a different email."
            
            if len(postData['reg-pword']) < 1:
                errors['reg-pword'] = "Password is a required field"
            elif len(postData['reg-pword']) < 8:
                errors['reg-pword'] = "Password must be at least 8 characters"
            elif postData['reg-pword'] != postData['reg-confpw']:
                errors['reg-pword'] = "Passwords DO NOT match!"

        elif pageType == 'login': #Login Checks
            pattern = re.compile("^[^\s@]+@[^\s@]+\.[^\s@]+$")

            if len(postData['log-email']) < 1:
                errors['log-email'] = "Email is a required field"
            if len(postData['log-pword']) < 1:
                errors['log-pword'] = "Password is a required field"
            else:
                checkUser = User.objects.filter(email=postData['log-email'], password=postData['log-pword'])
                if (len(checkUser) < 1):
                    #If there is no match, we return to the reg/login page with an error message, as stated below
                    errors['log-invalid'] = "The email and password combination entered do not match a record in our database"
            
        elif pageType == 'update': #Update Page Checks
            pattern = re.compile("^[A-Za-z]+$")
            
            if len(postData['fname']) < 1:
                errors['fname'] = "First Name is a required field"
            elif len(postData['fname']) < 2:
                errors['fname'] = "First Name must be at least 2 characters"
            elif not pattern.match(postData['fname']):
                errors['fname'] = "First Name must only contain letters"
            
            if len(postData['lname']) < 1:
                errors['lname'] = "Last Name is a required field"
            elif len(postData['lname']) < 2:
                errors['lname'] = "Last Name must be at least 2 characters"
            elif not pattern.match(postData['lname']):
                errors['lname'] = "Last Name must only contain letters"
            
            pattern = re.compile("^[^\s@]+@[^\s@]+\.[^\s@]+$")

            if len(postData['email']) < 1:
                errors['email'] = "Email is a required field"
            elif not pattern.match(postData['email']):
                errors['email'] = "Please enter a valid email address! \n Example: joe.smith@email.com"
            else:
                if (postData['email'] != userEmail):
                    checkEmail = User.objects.filter(email=postData['email'])
                    if checkEmail:
                        errors['email'] = "A user with this email is already registered. Please enter a different email."

        return errors

class QuoteManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if (len(postData['post-author']) < 3):
            errors['post-author'] = "Author must be at least 3 characters"
        
        if (len(postData['post-quote']) < 10):
            errors['post-quote'] = "Quote must be at least 10 characters"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    user = models.ForeignKey(User, related_name="quotes")
    author = models.CharField(max_length=255)
    quote = models.TextField()
    like = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()