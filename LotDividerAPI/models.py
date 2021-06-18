from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
import yfinance as yf
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
    ticker = models.CharField(max_length=50, unique=True)
    cusip = models.CharField(max_length=50, unique=True)
    name = models.TextField()
    number = models.CharField(max_length=50, default=uuid.uuid4)
    productType = models.ForeignKey(ProductType, related_name="relatedSecurities", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"Security Ticker {self.ticker}, Security Name: {self.name}, Security Product Type: {self.productType.name}")

    @property
    def latestClosingPrice(self):
        closingDate = date.today().strftime("%Y-%m-%d")
        closingPrice = yf.download([self.ticker], closingDate)['Adj Close'][0]
        return closingPrice

class Portfolio(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # accounts
    # holdings
    # taxLots

    def __str__(self):
        return (f"Portfolio Name: {self.name}, Portfolio Number: {self.number}, ID: {self.id}")

class Account(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    portfolio = models.ForeignKey(Portfolio, related_name="accounts", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # holdings = holdings
    
    def __str__(self):
        return (f"Account Name {self.name}, Account Number: {self.number}")

class Holding(models.Model):
    security = models.ForeignKey(Security, related_name="relatedHoldings", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name="holdings", on_delete=models.CASCADE)
    number = models.CharField(max_length=50, default=uuid.uuid4)
    
    #taxLots = tax lots associated with the holding

    def __str__(self):
        return (f"Holding: {self.security.name}, Account Name: {self.account.name}, ID: {self.id}")

class TaxLot(models.Model):
    number = models.CharField(max_length=50, default=uuid.uuid4)
    holding = models.ForeignKey(Holding, related_name="taxLots", on_delete=models.CASCADE)
    units = models.DecimalField(max_digits=20, decimal_places=4)
    totalFederalCost = models.DecimalField(max_digits=20, decimal_places=2)
    totalStateCost = models.DecimalField(max_digits=20, decimal_places=2)
    acquisitionDate = models.DateTimeField(auto_now_add=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # portfolio = models.ForeignKey(Portfolio, related_name="lots", on_delete=models.CASCADE)
    # productType = models.ForeignKey(ProductType, related_name="lotsAssociated", on_delete=models.CASCADE)

    def __str__(self):
        return (f"Lot Number: {self.number}, Ticker: {self.holding.security.ticker}, Units: {self.units}, Cost: {self.totalFederalCost}")

class Proposal(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    number = models.CharField(max_length=50, default=uuid.uuid4)
    accountUsed = models.ForeignKey(Account, related_name="relatedProposals", on_delete=models.CASCADE)
    holdingsUsed = models.ManyToManyField(Holding, related_name="relatedProposals")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name="proposals", on_delete=models.CASCADE)
    
    # accounts
    # draft portfolios

    def __str__(self):
        return (f"Proposal Name: {self.name}, Proposal Number: {self.number}")

class DraftPortfolio(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    number = models.CharField(max_length=50, default=uuid.uuid4)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    proposal = models.ForeignKey(Proposal, related_name="draftPortfolios", on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, related_name="draftPortfolios", on_delete=models.CASCADE)
    # accounts

    def __str__(self):
        return (f"Draft Portfolio Name: {self.name}, Draft Portfolio Number: {self.number}")

class DraftAccount(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    number = models.CharField(max_length=50, default=uuid.uuid4)
    draftPortfolio = models.ForeignKey(DraftPortfolio, related_name="draftAccounts", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    # draftHoldings = holdings
    
    def __str__(self):
        return (f"Draft Account Name: {self.name}, Draft Account Number: {self.number}")

class DraftHolding(models.Model):
    security = models.ForeignKey(Security, related_name="relatedDraftHoldings", on_delete=models.CASCADE)
    draftAccount = models.ForeignKey(DraftAccount, related_name="draftHoldings", on_delete=models.CASCADE)
    
    #taxLots = tax lots associated with the holding

    def __str__(self):
        return (f"Draft Holding: {self.security.name}, Draft Account Name: {self.draftAccount.name}")

class DraftTaxLot(models.Model):
    number = models.CharField(max_length=50, default=uuid.uuid4)
    draftHolding = models.ForeignKey(DraftHolding, related_name="draftTaxLots", on_delete=models.CASCADE)
    units = models.DecimalField(max_digits=20, decimal_places=4)
    referencedLot = models.ForeignKey(TaxLot, related_name="draftTaxLotsRelated", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # portfolio = models.ForeignKey(Portfolio, related_name="lots", on_delete=models.CASCADE)
    # productType = models.ForeignKey(ProductType, related_name="lotsAssociated", on_delete=models.CASCADE)

    def __str__(self):
        return (f"Draft Lot Number: {self.number}, Ticker: {self.draftHolding.security.ticker}, Units: {self.units}")

