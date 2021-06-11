from rest_framework import test
from rest_framework import status
from django.contrib.auth import get_user_model
from LotDividerAPI import models as apiModels
from django.contrib.auth.hashers import make_password
from LotDividerAPI import serializers, read_serializers
from rest_framework.renderers import JSONRenderer
from datetime import date
from decimal import Decimal

class AutoProposalSerializerTestCase(test.APITestCase):
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
            project = cls.pj1,
            accountUsed = cls.a1
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

    # def test_instance(self):
    #     data = {
    #         'projectID': 1,
    #         'proposalName': 'test proposal',
    #         'accountID': 1,
    #         'autoCalculate': 'true',
    #         'numberOfPortfolios': 2,
    #         'targetShares': {
    #             'AMC': 10,
    #         },
    #         'method': 'HIFO',
    #     }
    #     proposal = serializers.AutoProposalSerializer(data)
    #     self.assertEqual(proposal.data['projectID'], 1)
    #     self.assertEqual(proposal.data['method'], 'HIFO')

    # def test_split(self):
    #     data = {
    #         'projectID': 1,
    #         'proposalName': 'test proposal',
    #         'accountID': 1,
    #         'autoCalculate': 'true',
    #         'numberOfPortfolios': 2,
    #         'targetShares': {
    #             'AMC': 10,
    #         },
    #         'method': 'HIFO',
    #     }
    #     proposal = serializers.AutoProposalSerializer(data=data)
    #     response = proposal.is_valid()
    #     print(response)
    #     newProposal = proposal.save()
    #     testSerializer = read_serializers.ProposalSerializer(newProposal)
    #     print(JSONRenderer().render(testSerializer.data))