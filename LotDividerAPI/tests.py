from rest_framework import test
from rest_framework import status
from django.contrib.auth import get_user_model
from LotDividerAPI import models as apiModels
from django.contrib.auth.hashers import make_password

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
                3,
            ],
        }
        self.client.login(email='test@test.com', password='test1234')
        response = self.client.post(url, data, format='json')
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
            "productType": 3 # postgres does not reset id's on flush
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
            "productType": 3
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
    