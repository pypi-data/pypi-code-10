from molo.core.models import LanguagePage, Main, ArticlePage
from molo.yourwords.models import (
    YourWordsCompetitionEntry, YourWordsCompetition)
from django.test import TestCase, RequestFactory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.test.client import Client
from wagtail.wagtailcore.models import Site, Page


class TestAdminActions(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
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

    def test_convert_to_article(self):
        comp = YourWordsCompetition(
            title='Test Competition',
            description='This is the description')
        self.english.add_child(instance=comp)
        comp.save_revision().publish()

        entry = YourWordsCompetitionEntry.objects.create(
            competition=comp,
            user=self.user,
            story_name='test',
            story_text='test body',
            terms_or_conditions_approved=True,
            hide_real_name=True
        )
        client = Client()
        client.login(username='tester', password='tester')
        response = client.get(
            '/django-admin/yourwords/yourwordscompetitionentry/%d/convert/' %
            entry.id)
        article = ArticlePage.objects.get(title='test')
        entry = YourWordsCompetitionEntry.objects.get(pk=entry.pk)
        self.assertEquals(entry.story_name, article.title)
        self.assertEquals(entry.article_page, article)
        self.assertEquals(article.body.stream_data, [{
            "type": "paragraph", "value": "Written by: Anonymous",
            "type": "paragraph", "value": entry.story_text,
        }])

        self.assertEquals(ArticlePage.objects.all().count(), 1)
        self.assertEquals(
            response['Location'],
            'http://testserver/admin/pages/5/move/')

        # second time it should redirect to the edit page
        response = client.get(
            '/django-admin/yourwords/yourwordscompetitionentry/%d/convert/' %
            entry.id)
        self.assertEquals(
            response['Location'],
            'http://testserver/admin/pages/5/edit/')
        self.assertEquals(ArticlePage.objects.all().count(), 1)
