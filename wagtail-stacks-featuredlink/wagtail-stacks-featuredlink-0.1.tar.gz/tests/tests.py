from __future__ import unicode_literals
import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stacks_featuredlink.models import StacksFeaturedLinkList


class StacksFeaturedLinkTestCase(TestCase):
    """The test suite for stacks-page"""

    fixtures = ['stacksfeaturedlink.json']
    maxDiff = None

    def setUp(self):
        """Set up the test suite."""
        password = '12345'
        user = User.objects.create_user(
            username='test_user',
            email='user@test.com',
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        user_client = Client()
        user_login = user_client.login(
            username='test_user',
            password=password
        )
        self.assertTrue(user_login)
        self.user = user
        self.user_client = user_client
        self.featuredlinklist = StacksFeaturedLinkList.objects.get()

    def test_instance(self):
        """Test the test StacksFeaturedLink instance."""
        self.assertEqual(
            self.featuredlinklist.pk,
            1
        )
        self.assertEqual(
            self.featuredlinklist.__str__(),
            'Stacks Sites'
        )
        self.assertEqual(
            self.featuredlinklist.links.all()[0].__str__(),
            'Last Days in Vietnam'
        )
        self.assertEqual(
            self.featuredlinklist.stacksfeaturedlinklistlink_set.all()[
                0
            ].__str__(),
            'Stacks Sites 1. Last Days in Vietnam'
        )

    def test_serialization(self):
        """Test the StacksFeaturedLink textplusstuff serializer."""
        response = self.client.get(
            '/textplusstuff/stacks_featuredlink/'
            'stacksfeaturedlinklist/detail/1/'
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            json.loads(response.content)['context'],
            {
                "name": "Stacks Sites",
                "display_title": "Stacks Sites",
                "extra_context": {},
                "links": [
                    {
                        "name": "Last Days in Vietnam",
                        "overline": "",
                        "display_title": "Last Days in Vietnam",
                        "image": {
                            "full_size": (
                                "/media/stacks_featuredlink/"
                                "last-days-poster.jpg"
                            )
                        },
                        "url": (
                            "http://www.pbs.org/wgbh/americanexperience/"
                            "lastdays/"
                        ),
                        "optional_content": {
                            "as_plaintext": (
                                "During the Fall of Saigon in 1975, a handful "
                                "of individuals took matters into their own "
                                "hands in a desperate effort to evacuate as "
                                "many South Vietnamese as possible.\n"
                            ),
                            "as_html": (
                                "<p>During the Fall of Saigon in 1975, a "
                                "handful of individuals took matters into "
                                "their own hands in a desperate effort to "
                                "evacuate as many South Vietnamese as "
                                "possible.</p>\n"
                            ),
                            "raw_text": (
                                "During the Fall of Saigon in 1975, a handful "
                                "of individuals took matters into their own "
                                "hands in a desperate effort to evacuate as "
                                "many South Vietnamese as possible."
                            ),
                            "as_html_no_tokens": (
                                "<p>During the Fall of Saigon in 1975, a "
                                "handful of individuals took matters into "
                                "their own hands in a desperate effort to "
                                "evacuate as many South Vietnamese as "
                                "possible.</p>\n"
                            ),
                            "as_markdown": (
                                "During the Fall of Saigon in 1975, a handful "
                                "of individuals took matters into their own "
                                "hands in a desperate effort to evacuate as "
                                "many South Vietnamese as possible."
                            )
                        },
                        "extra_context": {}
                    },
                    {
                        "name": "Sacred Journeys",
                        "overline": "",
                        "display_title": "Sacred Journeys",
                        "url": (
                            "http://www.pbs.org/wgbh/sacredjourneys/"
                            "content/home/"
                        ),
                        "image": {
                            "full_size": (
                                "/media/stacks_featuredlink/sacred-journeys-"
                                "poster.jpg"
                            )
                        },
                        "optional_content": {
                            "as_plaintext": (
                                "Join best-selling author/adventurer Bruce "
                                "Feiler on an epic journey as he travels with "
                                "contemporary pilgrims on six historic "
                                "pilgrimages.\n"
                            ),
                            "as_html": (
                                "<p>Join best-selling author/adventurer Bruce "
                                "Feiler on an epic journey as he travels with "
                                "contemporary pilgrims on six historic "
                                "pilgrimages.</p>\n"
                            ),
                            "raw_text": (
                                "Join best-selling author/adventurer Bruce "
                                "Feiler on an epic journey as he travels with "
                                "contemporary pilgrims on six historic "
                                "pilgrimages."
                            ),
                            "as_html_no_tokens": (
                                "<p>Join best-selling author/adventurer Bruce "
                                "Feiler on an epic journey as he travels with "
                                "contemporary pilgrims on six historic "
                                "pilgrimages.</p>\n"
                            ),
                            "as_markdown": (
                                "Join best-selling author/adventurer Bruce "
                                "Feiler on an epic journey as he travels with "
                                "contemporary pilgrims on six historic "
                                "pilgrimages."
                            )
                        },
                        "extra_context": {}
                    },
                    {
                        "name": "The Downton Abbey Experience",
                        "overline": "",
                        "display_title": "The Downton Abbey Experience",
                        "url": (
                            "http://www.pbs.org/wgbh/masterpiece/downtonabbey/"
                            "downton-experience.html"
                        ),
                        "image": {
                            "full_size": (
                                "/media/stacks_featuredlink/downton-"
                                "experience-poster.jpg"
                            )
                        },
                        "optional_content": {
                            "as_plaintext": (
                                "Explore video, photos, what's trending on "
                                "social, and more from Downton Abbey Season "
                                "5. The new season of Downton Abbey airs "
                                "Sundays, Jan. 4th - Mar. 1st, 2015 at 9pm ET "
                                "on MASTERPIECE on PBS. #DowntonPBS\n"
                            ),
                            "as_html": (
                                "<p>Explore video, photos, what's trending on "
                                "social, and more from Downton Abbey Season "
                                "5. The new season of Downton Abbey airs "
                                "Sundays, Jan. 4th - Mar. 1st, 2015 at 9pm ET "
                                "on MASTERPIECE on PBS. #DowntonPBS</p>\n"
                            ),
                            "raw_text": (
                                "Explore video, photos, what's trending on "
                                "social, and more from Downton Abbey Season "
                                "5. The new season of Downton Abbey airs "
                                "Sundays, Jan. 4th - Mar. 1st, 2015 at 9pm ET "
                                "on MASTERPIECE on PBS. \\#DowntonPBS"
                            ),
                            "as_html_no_tokens": (
                                "<p>Explore video, photos, what's trending on "
                                "social, and more from Downton Abbey Season "
                                "5. The new season of Downton Abbey airs "
                                "Sundays, Jan. 4th - Mar. 1st, 2015 at 9pm ET "
                                "on MASTERPIECE on PBS. #DowntonPBS</p>\n"
                            ),
                            "as_markdown": (
                                "Explore video, photos, what's trending on "
                                "social, and more from Downton Abbey Season "
                                "5. The new season of Downton Abbey airs "
                                "Sundays, Jan. 4th - Mar. 1st, 2015 at 9pm ET "
                                "on MASTERPIECE on PBS. \\#DowntonPBS"
                            )
                        },
                        "extra_context": {}
                    }
                ]
            }
        )
