from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from molo.core.models import LanguagePage, Main
from molo.yourwords.models import (
    YourWordsCompetition, YourWordsCompetitionEntry)
from wagtail.wagtailcore.models import Site, Page


class TestYourWordsViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')

        # Create page content type
        page_content_type, created = ContentType.objects.get_or_create(
            model='page',
            app_label='wagtailcore'
        )

        # Create root page
        Page.objects.create(
            title="Root",
            slug='root',
            content_type=page_content_type,
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )

        main_content_type, created = ContentType.objects.get_or_create(
            model='main', app_label='core')

        # Create a new homepage
        main = Main.objects.create(
            title="Main",
            slug='main',
            content_type=main_content_type,
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/home/',
        )
        main.save_revision().publish()

        self.english = LanguagePage(
            title='English',
            code='en',
            slug='english')
        main.add_child(instance=self.english)
        self.english.save_revision().publish()

        # Create a site with the new homepage set as the root
        Site.objects.all().delete()
        Site.objects.create(
            hostname='localhost', root_page=main, is_default_site=True)

    def test_yourwords_competition_page(self):
        client = Client()
        client.login(username='tester', password='tester')

        comp = YourWordsCompetition(
            title='Test Competition',
            description='This is the description',
            slug='test-competition')
        self.english.add_child(instance=comp)
        comp.save_revision().publish()

        comp = YourWordsCompetition.objects.get(slug='test-competition')

        response = client.get('/english/test-competition/')
        self.assertContains(response, 'Test Competition')
        self.assertContains(response, 'This is the description')

    def test_yourwords_validation_for_fields(self):
        client = Client()
        client.login(username='tester', password='tester')

        comp = YourWordsCompetition(
            title='Test Competition',
            description='This is the description',
            slug='test-competition')
        self.english.add_child(instance=comp)
        comp.save_revision().publish()

        comp = YourWordsCompetition.objects.get(slug='test-competition')

        client.get(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]))

        response = client.post(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]), {})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'This field is required')

        response = client.post(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]),
            {'story_name': 'this is a story'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'This field is required')

        response = client.post(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]),
            {'story_name': 'This is a story', 'story_text': 'The text'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'This field is required')

        response = client.post(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]), {
                'story_name': 'This is a story',
                'story_text': 'The text',
                'terms_or_conditions_approved': 'true'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(YourWordsCompetitionEntry.objects.all().count(), 1)

        response = client.post(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]), {
                'story_name': 'This is a story',
                'story_text': 'The text',
                'terms_or_conditions_approved': 'true',
                'hide_real_name': 'true'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(YourWordsCompetitionEntry.objects.all().count(), 2)

    def test_yourwords_thank_you_page(self):
        client = Client()
        client.login(username='tester', password='tester')

        comp = YourWordsCompetition(
            title='Test Competition',
            description='This is the description',
            slug='test-competition')
        self.english.add_child(instance=comp)
        comp.save_revision().publish()

        response = client.post(
            reverse('molo.yourwords:competition_entry', args=[comp.slug]), {
                'story_name': 'This is a story',
                'story_text': 'The text',
                'terms_or_conditions_approved': 'true'})

        self.assertEqual(
            response['Location'],
            'http://testserver/yourwords/thankyou/test-competition/')
