from django.contrib.auth.models import User
from django.db import models

STANDARD = (
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
    ('V', 'V'),
    ('VI', 'VI'),
    ('VII', 'VII'),
    ('VIII', 'VIII'),
    ('IX', 'IX'),
    ('X', 'X'),
    ('XI', 'XI'),
    ('XII', 'XII'),
)


class StudentData(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    prn = models.CharField(max_length=16, unique=True)
    full_name = models.CharField(max_length=80)
    mother_name = models.CharField(max_length=20)
    roll_number = models.IntegerField(null=True, blank=True)
    standard = models.CharField(max_length=20, choices=STANDARD, null=True, blank=True)
    profile = models.ImageField(upload_to='profile/', default='avatar.png')
