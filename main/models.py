from django.db import models

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['name']) < 4:
            errors["name"] = "El nombre del usuario debe tener más de 4 letra"
        if len(postData['email']) < 4:
            errors["email"] = "El correo debe tener más de 4 letras"
        if len(postData['password']) < 6:
            errors["password"] = "La contraseña debe tener más de 6 caracteres"
        if postData['password'] != postData['password_conf']:
            errors['password'] = "Ambas contraseñas deben ser iguales"
        return errors

class User(models.Model):
    avatar = models.URLField(default="https://png.pngtree.com/png-vector/20191110/ourlarge/pngtree-avatar-icon-profile-icon-member-login-vector-isolated-png-image_1978396.jpg")
    name = models.CharField(max_length=455)
    email = models.EmailField()
    password = models.CharField(max_length=455)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Message(models.Model):
    message = models.CharField(max_length=455)
    user = models.ForeignKey(User, related_name="messages", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=455)
    user = models.ForeignKey(User, related_name="comments", on_delete= models.CASCADE)
    message = models.ForeignKey(Message, related_name="comments", on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

