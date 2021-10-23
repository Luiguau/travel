from django.db import models
import re
import bcrypt
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errores = {}
        if len(User.objects.filter(username=postData['username'])) > 0:
            errores['username'] = "User already registered"
        else:
            if len(postData['name']) < 3:
                errores['name'] = "Name should be at least 3 characters"
            if len(postData['username']) < 3:
                errores['username'] = "Username should be at least 3 characters"
            EMAIL = re.compile(
                r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL.match(postData['email']):
                errores['email'] = "Invalid email"
            if len(postData['password']) < 8:
                errores['password'] = "Password should be at least 8 characters"

            val_pass = self.comparar_password(postData['password'],postData['password2'])
            if len(val_pass) > 0:
                errores['confpass'] = val_pass

        return errores

    def encriptar(self, password):
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password.decode('utf-8')

    def validar_login(self, password, usuario ):
        errores = {}
        if len(usuario) > 0:
            pw_hash = usuario[0].password

            if bcrypt.checkpw(password.encode(), pw_hash.encode()) is False:
                errores['login'] = "Password is incorrect"
        else:
            errores['login'] = "User does not exist"
        return errores
    
    def comparar_password(self,password, password2):
        if password != password2:
            return "Password does not match"
        else:
            return ""


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()