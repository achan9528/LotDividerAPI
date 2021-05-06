from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, default=uuid.uuid4,
                unique=True)
    password = models.CharField(max_length=255)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    # objects = UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name', 'alias']
    # projects 

    def __str__(self):
        return f"Name: {self.name}"

class Project(models.Model):
    owners = models.ManyToManyField(User, related_name="projects")
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # draftPortfolios

    def __str__(self):
        return (f"Project Name: {self.name}, Project Number: {self.number}")

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    fractionalLotsAllowed = models.BooleanField(default=False)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # lotsAssociated = lots associated with this type of produc type

    def __str__(self):
        return (f"Product Type Name: {self.name}, Fractional Lots Allowed: {self.fractionalLotsAllowed}, ID: {self.id}")

class Security(models.Model):
    ticker = models.CharField(max_length=50)
    cusip = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    productType = models.ForeignKey(ProductType, related_name="relatedSecurities", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Security Ticker {self.ticker}, Security Name: {self.name}, Security Product Type: {self.productType.name}")

# class Portfolio(models.Model):
#     name = models.CharField(max_length=50)
#     number = models.CharField(max_length=50, default=uuid.uuid4)
#     uploadedBy = models.ForeignKey(User, related_name="relatedPortfolios", on_delete=models.CASCADE)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     updatedAt = models.DateTimeField(auto_now=True)

#     # accounts
#     # holdings
#     # taxLots

#     def __str__(self):
#         return (f"Portfolio Name: {self.name}, Portfolio Number: {self.number}")