from rest_framework import test
from rest_framework import status
from django.contrib.auth import get_user_model
from LotDividerAPI import models as apiModels
from django.contrib.auth.hashers import make_password
from LotDividerAPI import serializers, read_serializers
from rest_framework.renderers import JSONRenderer
from datetime import date
from decimal import Decimal

# Unit / Integration tests between API and db (CRUD functionality)
class RegisterTestCase(test.APITestCase):
    
    def setUp(self):
        self.url = ('http://localhost:8000/api/rest-auth/registration/')

    def test_registerUser(self):
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(get_user_model().objects.filter(name="Alex")),1)

    def test_registerUser_noEmail(self):
        data = {
            'name': 'Alex',
            'email': '',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_nameLessThan3(self):
        data = {
            'name': 'Al',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_passwordsDoNotMatch(self):
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'FAKEPASSWORD',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registerUser_hashPassword(self):
        data = {
            'name': 'Alex',
            'email': 'test@test.com',
            'alias': 'ac',
            'password': 'test1234',
            'passwordConfirm': 'test1234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test = get_user_model().objects.get(email=data['email'])
        self.assertNotEqual(test.password, data['password'])

class LoginTestCase(test.APITestCase):
    # intial setup with a test user
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        user = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        user.save()

    # base functionality case
    def test_loginUser(self):
        url = ('http://localhost:8000/api/rest-auth/login/')
        data = {
            'email': 'test@test.com',
            'password': 'test1234',
        }
        response = self.client.post(url, data, format='json')
        print(get_user_model().objects.all())
        self.assertEquals(len(get_user_model().objects.all()), 1)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
    def test_403Error(self):
        url = ('http://localhost:8000/api/welcome/')
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_200WithToken(self):
        response = self.client.login(email='test@test.com', password='test1234')
        self.assertEqual(response, True)
        response = self.client.get('http://localhost:8000/api/welcome/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, {'welcome': 'hello!'})
        print(response.data)

class ProjectTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )

        pwHash = make_password('test5678')
        get_user_model().objects.create(
            name =  'Chris',
            email = 'test2@test.com',
            alias = 'cc',
            password = pwHash,
        )
        
        project = apiModels.Project.objects.create(name= 'testProject')
        project.owners.add(get_user_model().objects.first())
        
    def test_setUpData(self):
        self.assertEqual(apiModels.Project.objects.first().owners.all()[0].name,'Alex')

    def test_createProject(self):
        url = ('http://localhost:8000/api/projects/')
        data = {
            'name': 'testProject2',
            'owners': [
                1,
            ],
        }
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.post(url, data, format='json')
        for person in get_user_model().objects.all():
            print(person.id)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listProjects(self):
        url = ('http://localhost:8000/api/projects/')
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

    def test_listProjectsDifferentUser(self):
        url = ('http://localhost:8000/api/projects/')
        self.client.login(email='test2@test.com', password='test5678')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

class ProductTypeTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        get_user_model().objects.create(
            name='test',
            alias='test',
            email='test@test.com',
            password=pwHash,
        )
        apiModels.ProductType.objects.create(
            name = 'stock',
            fractionalLotsAllowed = True
        )

    def test_addProductType(self):
        url = 'http://localhost:8000/api/products/'
        data = {
            'name': 'mutual fund',
            'fractionalLotsAllowed': 'false',
        }
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_getProductTypes(self):
        url = 'http://localhost:8000/api/products/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print(response.content)

    def test_getProductType1(self):
        url = 'http://localhost:8000/api/products/1/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.content)

    def test_putProductType1(self):
        url = 'http://localhost:8000/api/products/1/'
        data = {
            'name': 'equity',
            'fractionalLotsAllowed': 'true'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.content)

    def test_patchProductType1(self):
        url = 'http://localhost:8000/api/products/1/'
        data = {
            'fractionalLotsAllowed': 'false'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.content)
    
class SecurityTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(self):
        # set up test user
        pwHash = make_password('test1234')
        get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )

        apiModels.ProductType.objects.create(
            name="stock",
            fractionalLotsAllowed=False
        )

        apiModels.Security.objects.create(
            name="amc",
            ticker="AMC",
            cusip="cusip",
            productType=apiModels.ProductType.objects.get(
                name="stock"
            ),
        )

    def test_createSecurity(self):
        url = "http://localhost:8000/api/securities/"
        data = {
            "name": "microsoft",
            "ticker": "MSFT",
            "cusip": "test",
            "productType": 1 # postgres does not reset id's on flush
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(apiModels.Security.objects.get(ticker="MSFT").name,"microsoft")

    def test_createSecurityNoProductType(self):
        url = "http://localhost:8000/api/securities/"
        data = {
            "name": "microsoft",
            "ticker": "MSFT",
            "cusip": "test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listSecurities(self):
        url = "http://localhost:8000/api/securities/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.content)

    def test_getSecurity(self):
        url = "http://localhost:8000/api/securities/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticker'],'AMC')

    def test_putSecurity1(self):
        # PUT operation to first overwrite first entry in db
        url = "http://localhost:8000/api/securities/1/"
        data = {
            "name": "facebook",
            "ticker": "FB",
            "cusip": "test",
            "productType": 1
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # GET operation to check
        response = self.client.get(url)
        self.assertEqual(response.data['ticker'],'FB')

    def test_patchSecurity1(self):
        # PUT operation to first overwrite first entry in db
        url = "http://localhost:8000/api/securities/1/"
        data = {
            "cusip": "bookface",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # GET operation to check
        response = self.client.get(url)
        self.assertEqual(response.data['cusip'],'bookface')
    
class PortfolioTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        user = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        user.save()
    
    def test_createPortfolio(self):
        url = ('http://localhost:8000/api/portfolios/')
        data = {
            'name': 'testPortfolio',
        }
        # self.client.login(email='test@test.com', password='test1234')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listPortfolios(self):
        url = ('http://localhost:8000/api/portfolios/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class AccountTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        user = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        user.save()
    
        apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

    def test_createAccount(self):
        url = ('http://localhost:8000/api/accounts/')
        data = {
            'name': 'testAccount',
            'portfolio': 1,
        }
        print(apiModels.Portfolio.objects.all())
        print(apiModels.Portfolio.objects.get(id=1))
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listAccounts(self):
        url = ('http://localhost:8000/api/accounts/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        print(response.data)

class HoldingTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        user = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        user.save()
        
        apiModels.ProductType.objects.create(
            name='stock',
        )

        apiModels.ProductType.objects.create(
            name='mutual fund',
        )

        apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        apiModels.Holding.objects.create(
            account=apiModels.Account.objects.get(name='testAccount'),
            security=apiModels.Security.objects.first()
        )

    def test_createHolding(self):
        url = ('http://localhost:8000/api/holdings/')
        data = {
            'account': 1,
            'security': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(apiModels.Holding.objects.all()), 2)

    def test_listHoldings(self):
        url = ('http://localhost:8000/api/holdings/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(apiModels.Holding.objects.all()), 1)

    def test_patchHolding1(self):
        url = ('http://localhost:8000/api/holdings/1/')
        data = {
            'security': 2
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        security = apiModels.Account.objects.get(id=1).holdings.first().security.id
        self.assertEqual(security, 2)
    
    def test_putHolding1(self):
        url = ('http://localhost:8000/api/holdings/1/')
        data = {
            'account': 2,
            'security': 2
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        security = apiModels.Account.objects.get(id=2).holdings.first().security.id
        self.assertEqual(security, 2)

    def test_listHoldingDetails(self):
        url = ('http://localhost:8000/api/holdings/1/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deleteHolding(self):
        url = ('http://localhost:8000/api/holdings/1/')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(apiModels.Holding.objects.all()), 0)

class TaxLotTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        user = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        user.save()
        
        apiModels.ProductType.objects.create(
            name='stock',
        )

        apiModels.ProductType.objects.create(
            name='mutual fund',
        )

        apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        apiModels.Holding.objects.create(
            account=apiModels.Account.objects.get(name='testAccount'),
            security=apiModels.Security.objects.first()
        )

        apiModels.Holding.objects.create(
            account=apiModels.Account.objects.get(name='testAccount'),
            security=apiModels.Security.objects.get(id=2)
        )

        apiModels.TaxLot.objects.create(
            holding = apiModels.Holding.objects.first(),
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

    def test_createTaxLot(self):
        url = ('http://localhost:8000/api/tax-lots/')
        data = {
            'holding' : 1,
            'units' : 20,
            'totalFederalCost' : 20,
            'totalStateCost' : 20,
            'acquisitionDate' : date.today()
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    
    def test_listTaxLots(self):
        url = ('http://localhost:8000/api/tax-lots/')
        response = self.client.get(url, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_patchTaxLot1(self):
        url = ('http://localhost:8000/api/tax-lots/1/')
        data = {
            'units' : 15,
        }
        response = self.client.patch(url, data, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_putTaxLot1(self):
        url = ('http://localhost:8000/api/tax-lots/1/')
        data = {
            'holding' : 2,
            'units' : 30,
            'totalFederalCost' : 30,
            'totalStateCost' : 30,
            'acquisitionDate' : date.today()
        }
        response = self.client.put(url, data, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_deleteTaxLot1(self):
        url = ('http://localhost:8000/api/tax-lots/1/')
        response = self.client.delete(url, format = 'json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

class ProposalTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        cls.u1 = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        
        cls.pt1 = apiModels.ProductType.objects.create(
            name='stock',
        )

        cls.pt2 = apiModels.ProductType.objects.create(
            name='mutual fund',
            fractionalLotsAllowed = True
        )

        cls.s1 = apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        cls.s2 = apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        cls.p1 = apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        cls.a1 = apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.a2 = apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.h1 = apiModels.Holding.objects.create(
            account=cls.a1,
            security=cls.s1
        )

        cls.h2 = apiModels.Holding.objects.create(
            account=cls.a2,
            security=cls.s2
        )

        cls.tl1 = apiModels.TaxLot.objects.create(
            holding = cls.h1,
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

        cls.pj1 = apiModels.Project.objects.create(
            name='test project',
        )
        cls.pj1.owners.add(cls.u1)
        cls.pj1.save()

        cls.pp1 = apiModels.Proposal.objects.create(
            name = 'test proposal',
            project = cls.pj1
        )


        cls.dp1 = apiModels.DraftPortfolio.objects.create(
            name= 'testDraftPortfolio',
            proposal= cls.pp1,
        )
    
    def test_createProposal(self):
        url = ('http://localhost:8000/api/proposals/')
        data = {
            'name': 'test proposal',
            'project': self.pj1.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_autoCalculateProposal(self):
        url = ('http://localhost:8000/api/proposals/')
        data = {
            'projectID': 1,
            'proposalName': 'test proposal',
            'accountID': 1,
            'autoCalculate': 'true',
            'numberOfPortfolios': 2,
            'targetShares': {
                'AMC': 10,
            },
            'method': 'HIFO',
        }
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)

    def test_listProposals(self):
        url = ('http://localhost:8000/api/proposals/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print(response.data)

    def test_patchProposal1(self):
        url = ('http://localhost:8000/api/proposals/1/')
        data = {
            'name': 'another name!'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'another name!')
        print(apiModels.Proposal.objects.get(id=1))

    def test_putProposal1(self):
        url = ('http://localhost:8000/api/proposals/1/')
        data = {
            'name': 'put route test',
            'project': self.pj1.id,
        }
        response = self.client.put(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'put route test')

    def test_deleteProposal1(self):
        url = ('http://localhost:8000/api/proposals/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(apiModels.Proposal.objects.all()), 0)

class DraftPortfolioTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        cls.u1 = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        
        cls.pt1 = apiModels.ProductType.objects.create(
            name='stock',
        )

        cls.pt2 = apiModels.ProductType.objects.create(
            name='mutual fund',
            fractionalLotsAllowed = True
        )

        cls.s1 = apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        cls.s2 = apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        cls.p1 = apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        cls.a1 = apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.a2 = apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.h1 = apiModels.Holding.objects.create(
            account=cls.a1,
            security=cls.s1
        )

        cls.h2 = apiModels.Holding.objects.create(
            account=cls.a2,
            security=cls.s2
        )

        cls.tl1 = apiModels.TaxLot.objects.create(
            holding = cls.h1,
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

        cls.pj1 = apiModels.Project.objects.create(
            name='test project',
        )
        cls.pj1.owners.add(cls.u1)
        cls.pj1.save()

        cls.pp1 = apiModels.Proposal.objects.create(
            name = 'test proposal',
            project = cls.pj1
        )


        cls.dp1 = apiModels.DraftPortfolio.objects.create(
            name= 'testDraftPortfolio',
            proposal= cls.pp1,
        )
    
    def test_createDraftPortfolio(self):
        url = ('http://localhost:8000/api/draft-portfolios/')
        data = {
            'name': 'test draft Portfolio',
            'proposal': self.pp1.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listDraftPortfolios(self):
        url = ('http://localhost:8000/api/draft-portfolios/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_patchDraftPortfolio1(self):
        url = ('http://localhost:8000/api/draft-portfolios/1/')
        data = {
            'name': 'another name!'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'another name!')

    def test_putDraftPortfolio1(self):
        url = ('http://localhost:8000/api/draft-portfolios/1/')
        data = {
            'name': 'put route test',
            'proposal': self.pp1.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'put route test')

    def test_deleteDraftPortfolio1(self):
        url = ('http://localhost:8000/api/draft-portfolios/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(apiModels.DraftPortfolio.objects.all()), 0)

class DraftAccountTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        cls.u1 = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        
        cls.pt1 = apiModels.ProductType.objects.create(
            name='stock',
        )

        cls.pt2 = apiModels.ProductType.objects.create(
            name='mutual fund',
            fractionalLotsAllowed = True
        )

        cls.s1 = apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        cls.s2 = apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        cls.p1 = apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        cls.a1 = apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.a2 = apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.h1 = apiModels.Holding.objects.create(
            account=cls.a1,
            security=cls.s1
        )

        cls.h2 = apiModels.Holding.objects.create(
            account=cls.a2,
            security=cls.s2
        )

        cls.tl1 = apiModels.TaxLot.objects.create(
            holding = cls.h1,
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

        cls.pj1 = apiModels.Project.objects.create(
            name='test project',
        )
        cls.pj1.owners.add(cls.u1)
        cls.pj1.save()

        cls.pp1 = apiModels.Proposal.objects.create(
            name = 'test proposal',
            project = cls.pj1
        )


        cls.dp1 = apiModels.DraftPortfolio.objects.create(
            name= 'testDraftPortfolio',
            proposal= cls.pp1,
        )

        cls.da1 = apiModels.DraftAccount.objects.create(
            name = 'test draft account',
            draftPortfolio = cls.dp1,
        )
    
    def test_createDraftAccount(self):
        url = ('http://localhost:8000/api/draft-accounts/')
        data = {
            'name': 'test draft Portfolio',
            'draftPortfolio': self.dp1.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listDraftAccounts(self):
        url = ('http://localhost:8000/api/draft-accounts/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_patchDraftAccount1(self):
        url = ('http://localhost:8000/api/draft-accounts/1/')
        data = {
            'name': 'another name!'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'another name!')

    def test_putDraftAccount1(self):
        url = ('http://localhost:8000/api/draft-accounts/1/')
        data = {
            'name': 'put route test',
            'draftPortfolio': self.dp1.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'put route test')

    def test_deleteDraftAccount1(self):
        url = ('http://localhost:8000/api/draft-accounts/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(apiModels.DraftAccount.objects.all()), 0)

class DraftHoldingTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        cls.u1 = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        
        cls.pt1 = apiModels.ProductType.objects.create(
            name='stock',
        )

        cls.pt2 = apiModels.ProductType.objects.create(
            name='mutual fund',
            fractionalLotsAllowed = True
        )

        cls.s1 = apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        cls.s2 = apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        cls.p1 = apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        cls.a1 = apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.a2 = apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.h1 = apiModels.Holding.objects.create(
            account=cls.a1,
            security=cls.s1
        )

        cls.h2 = apiModels.Holding.objects.create(
            account=cls.a2,
            security=cls.s2
        )

        cls.tl1 = apiModels.TaxLot.objects.create(
            holding = cls.h1,
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

        cls.pj1 = apiModels.Project.objects.create(
            name='test project',
        )
        cls.pj1.owners.add(cls.u1)
        cls.pj1.save()

        cls.pp1 = apiModels.Proposal.objects.create(
            name = 'test proposal',
            project = cls.pj1
        )


        cls.dp1 = apiModels.DraftPortfolio.objects.create(
            name= 'testDraftPortfolio',
            proposal= cls.pp1,
        )
        
        cls.dp2 = apiModels.DraftPortfolio.objects.create(
            name= 'test draft portfolio 2',
            proposal= cls.pp1,
        )

        cls.da1 = apiModels.DraftAccount.objects.create(
            name = 'test draft account',
            draftPortfolio = cls.dp1,
        )

        cls.da2 = apiModels.DraftAccount.objects.create(
            name = 'test draft account 2',
            draftPortfolio = cls.dp1,
        )

        cls.dh1 = apiModels.DraftHolding.objects.create(
            security = cls.s1,
            draftAccount = cls.da1,
        )
    
    def test_createDraftHolding(self):
        url = ('http://localhost:8000/api/draft-holdings/')
        data = {
            'security': self.s1.id,
            'draftAccount': self.da1.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listDraftHoldings(self):
        url = ('http://localhost:8000/api/draft-holdings/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print(response.data)

    def test_patchDraftHolding1(self):
        url = ('http://localhost:8000/api/draft-holdings/1/')
        data = {
            'security': self.s2.id,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['security'], 2)

    def test_putDraftHolding1(self):
        url = ('http://localhost:8000/api/draft-holdings/1/')
        data = {
            'security': self.s2.id,
            'draftAccount': self.da2.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['draftAccount'], 2)
        self.assertEqual(response.data['security'], 2)

    def test_deleteDraftAccount1(self):
        url = ('http://localhost:8000/api/draft-holdings/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(apiModels.DraftHolding.objects.all()), 0)

class DraftTaxLotTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        cls.u1 = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        
        cls.pt1 = apiModels.ProductType.objects.create(
            name='stock',
        )

        cls.pt2 = apiModels.ProductType.objects.create(
            name='mutual fund',
            fractionalLotsAllowed = True
        )

        cls.s1 = apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        cls.s2 = apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        cls.p1 = apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        cls.a1 = apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.a2 = apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.h1 = apiModels.Holding.objects.create(
            account=cls.a1,
            security=cls.s1
        )

        cls.h2 = apiModels.Holding.objects.create(
            account=cls.a2,
            security=cls.s2
        )

        cls.tl1 = apiModels.TaxLot.objects.create(
            holding = cls.h1,
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

        cls.pj1 = apiModels.Project.objects.create(
            name='test project',
        )
        cls.pj1.owners.add(cls.u1)
        cls.pj1.save()

        cls.pp1 = apiModels.Proposal.objects.create(
            name = 'test proposal',
            project = cls.pj1
        )


        cls.dp1 = apiModels.DraftPortfolio.objects.create(
            name= 'testDraftPortfolio',
            proposal= cls.pp1,
        )
        
        cls.dp2 = apiModels.DraftPortfolio.objects.create(
            name= 'test draft portfolio 2',
            proposal= cls.pp1,
        )

        cls.da1 = apiModels.DraftAccount.objects.create(
            name = 'test draft account',
            draftPortfolio = cls.dp1,
        )

        cls.da2 = apiModels.DraftAccount.objects.create(
            name = 'test draft account 2',
            draftPortfolio = cls.dp1,
        )

        cls.dh1 = apiModels.DraftHolding.objects.create(
            security = cls.s1,
            draftAccount = cls.da1,
        )

        cls.dh2 = apiModels.DraftHolding.objects.create(
            security = cls.s2,
            draftAccount = cls.da1,
        )

        cls.dtl1 = apiModels.DraftTaxLot.objects.create(
            draftHolding = cls.dh1,
            units = 10,
            referencedLot = cls.tl1,
        )

    def test_createDraftTaxLot(self):
        url = ('http://localhost:8000/api/draft-taxlots/')
        data = {
            'draftHolding': self.dh1.id,
            'units': 20,
            'referencedLot': self.tl1.id,
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listDraftTaxLots(self):
        url = ('http://localhost:8000/api/draft-taxlots/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        print(response.content)

    def test_patchDraftTaxLot1(self):
        url = ('http://localhost:8000/api/draft-taxlots/1/')
        data = {
            'units': 30,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_putDraftTaxLot1(self):
        url = ('http://localhost:8000/api/draft-taxlots/1/')
        data = {
            'draftHolding': self.dh2.id,
            'units': 30,
            'referencedLot': self.tl1.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['referencedLot'], self.tl1.id)

    def test_deleteDraftTaxLot1(self):
        url = ('http://localhost:8000/api/draft-taxlots/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(apiModels.DraftTaxLot.objects.all()), 0)

class SerializerTestCase(test.APITestCase):
    @classmethod
    def setUpTestData(cls):
        pwHash = make_password('test1234')
        cls.u1 = get_user_model().objects.create(
            name =  'Alex',
            email = 'test@test.com',
            alias = 'ac',
            password = pwHash,
        )
        
        cls.pt1 = apiModels.ProductType.objects.create(
            name='stock',
        )

        cls.pt2 = apiModels.ProductType.objects.create(
            name='mutual fund',
            fractionalLotsAllowed = True
        )

        cls.s1 = apiModels.Security.objects.create(
            ticker='AMC',
            cusip='AMC',
            name='AMC',
            productType=apiModels.ProductType.objects.get(name='stock'),
        )

        cls.s2 = apiModels.Security.objects.create(
            ticker='VBINX',
            cusip='VBINX',
            name='VBINX',
            productType=apiModels.ProductType.objects.get(name='mutual fund'),
        )

        cls.p1 = apiModels.Portfolio.objects.create(
            name='testPortfolio',
        )

        cls.a1 = apiModels.Account.objects.create(
            name='testAccount',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.a2 = apiModels.Account.objects.create(
            name='testAccount2',
            portfolio=apiModels.Portfolio.objects.first(),
        )

        cls.h1 = apiModels.Holding.objects.create(
            account=cls.a1,
            security=cls.s1
        )

        cls.h2 = apiModels.Holding.objects.create(
            account=cls.a2,
            security=cls.s2
        )

        cls.tl1 = apiModels.TaxLot.objects.create(
            holding = cls.h1,
            units = 10,
            totalFederalCost = 10,
            totalStateCost = 10,
            acquisitionDate = date.today()
        )

        cls.pj1 = apiModels.Project.objects.create(
            name='test project',
        )
        cls.pj1.owners.add(cls.u1)
        cls.pj1.save()

        cls.pp1 = apiModels.Proposal.objects.create(
            name = 'test proposal',
            project = cls.pj1
        )


        cls.dp1 = apiModels.DraftPortfolio.objects.create(
            name= 'testDraftPortfolio',
            proposal= cls.pp1,
        )
        
        cls.dp2 = apiModels.DraftPortfolio.objects.create(
            name= 'test draft portfolio 2',
            proposal= cls.pp1,
        )

        cls.da1 = apiModels.DraftAccount.objects.create(
            name = 'test draft account',
            draftPortfolio = cls.dp1,
        )

        cls.da2 = apiModels.DraftAccount.objects.create(
            name = 'test draft account 2',
            draftPortfolio = cls.dp1,
        )

        cls.dh1 = apiModels.DraftHolding.objects.create(
            security = cls.s1,
            draftAccount = cls.da1,
        )

        cls.dh2 = apiModels.DraftHolding.objects.create(
            security = cls.s2,
            draftAccount = cls.da1,
        )

        cls.dtl1 = apiModels.DraftTaxLot.objects.create(
            draftHolding = cls.dh1,
            units = 10,
            referencedLot = cls.tl1,
        )

    def test_readNested(self):
        url = ('http://localhost:8000/api/proposals/')
        response = self.client.get(url, format='json', indent=4)
        response.render()
        print(response.content)
        print(type(response.data))
        print(type(response.content))
