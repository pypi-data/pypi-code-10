from __future__ import unicode_literals

from datetime import date

from django.test import TestCase

from .models import Poll, PollSlug, UserSlug, User, Post, DayPost, WordPost, PostSlug


class SluggableTests(TestCase):
    def test_slug_without_populate_from(self):
        with self.assertNumQueries(4):
            user = User.objects.create(username='thoas')

        self.assertEqual(UserSlug.objects.count(), 1)

        user.username = 'oleiade'
        user.save()

        self.assertEqual(UserSlug.objects.count(), 2)

        current = UserSlug.objects.get_current(user)

        self.assertEqual(current.slug, 'oleiade')

        user.username = 'thoas'
        user.save()

        current = UserSlug.objects.get_current(user)

        self.assertEqual(current.slug, 'thoas')

        self.assertEqual(UserSlug.objects.filter(redirect=True).count(), 1)

        user = User.objects.create(username='thoas')

        self.assertEqual(user.username, 'thoas-2')

        old = User.objects.get(username='thoas')
        old.delete()

        user.username = 'thoas'
        user.save()

        self.assertEqual(user.username, 'thoas')

    def test_changed(self):
        poll = Poll.objects.create(question='Quick test')

        self.assertFalse(poll.slug_changed)

        poll = Poll.objects.get(slug='quick-test')

        self.assertFalse(poll.slug_changed)

        poll = Poll(question='Quick test')

        self.assertTrue(poll.slug_changed)

        poll.save()

        self.assertEqual(poll.slug, 'quick-test-2')

    def test_simple_add(self):
        poll = Poll.objects.create(question='Quick test')

        self.assertEqual(poll.slug, u'quick-test')

        self.assertEqual(PollSlug.objects.count(), 1)

        slug = PollSlug.objects.get(slug='quick-test')

        self.assertEqual(slug.slug, 'quick-test')

        self.assertFalse(slug.redirect)

        self.assertEqual(slug.content_object, poll)

    def test_redirect(self):
        poll = Poll.objects.create(question='Quick test')
        poll.question = 'Another test'
        poll.save()

        self.assertEqual(poll.slug, u'quick-test')

        poll.slug = 'quick-test-2'
        poll.save()

        self.assertEqual(PollSlug.objects.count(), 2)

        slug = PollSlug.objects.get(slug='quick-test-2')

        self.assertFalse(slug.redirect)

        old = PollSlug.objects.get(slug='quick-test')

        self.assertTrue(old.redirect)

        current = PollSlug.objects.get_current(poll)

        self.assertEqual(old.current, slug)

        self.assertFalse(current is None)

        self.assertFalse(current.redirect)

    def test_redirect_restore_previous_slug(self):
        poll = Poll.objects.create(question='Quick test')
        poll.question = 'Another test'
        poll.save()

        poll.slug = 'quick-test-2'
        poll.save()

        self.assertEqual(PollSlug.objects.count(), 2)

        poll.slug = 'quick-test'
        poll.save()

        self.assertEqual(PollSlug.objects.count(), 2)

        slug = PollSlug.objects.get(slug='quick-test')
        self.assertFalse(slug.redirect)

        self.assertEqual(PollSlug.objects.filter(redirect=False).count(), 1)

        current = PollSlug.objects.get_current(poll)

        self.assertEqual(current.slug, 'quick-test')

    def test_is_slug_available(self):
        poll = Poll.objects.create(question='Quick test')

        self.assertFalse(PollSlug.objects.is_slug_available('quick-test'))

        self.assertTrue(PollSlug.objects.is_slug_available('quick-test', obj=poll))

    def test_delete(self):
        poll = Poll.objects.create(question='Quick test')

        self.assertEqual(PollSlug.objects.count(), 1)

        poll.delete()

        self.assertEquals(PollSlug.objects.count(), 0)

    def _unique_with(self, cls, typ, thing1, thing2):
        post1 = cls.objects.create(**{ typ:thing1, 'slug':'a-slug' })
        post2 = cls.objects.create(**{ typ:thing1, 'slug':'a-slug' })
        post3 = cls.objects.create(**{ typ:thing1, 'slug':'a-different-slug' })
        post4 = cls.objects.create(**{ typ:thing2, 'slug':'a-slug' })

        self.assertEquals(PostSlug.objects.count(), 4)

        self.assertEquals(post1.slug, 'a-slug')
        self.assertEquals(post2.slug, 'a-slug-2')
        self.assertEquals(post3.slug, 'a-different-slug')
        self.assertEquals(post4.slug, 'a-slug')

        post2.slug = 'a-different-slug'
        post2.save()
        post4.slug = 'a-different-slug'
        post4.save()

        self.assertEquals(PostSlug.objects.count(), 6)
        self.assertEquals(post2.slug, 'a-different-slug-2')
        self.assertEquals(post4.slug, 'a-different-slug')

    def test_unique_with(self):
        user1 = User.objects.create(username='matthew')
        user2 = User.objects.create(username='peter')

        self._unique_with(Post, 'user', user1, user2)

    def test_unique_with_date(self):
        self._unique_with(DayPost, 'date', date(2014, 1, 1), date(2014, 2, 1))

    def test_unique_with_blank_word(self):
        user = User.objects.create(username='matthew')

        post1 = WordPost.objects.create(user=user, word='word', slug='a-slug')
        post2 = WordPost.objects.create(user=user, word='word', slug='a-slug')
        post3 = WordPost.objects.create(user=user, word='', slug='a-slug')
        post4 = WordPost.objects.create(user=user, word='', slug='a-slug')

        self.assertEquals(PostSlug.objects.count(), 4)

        self.assertEquals(post1.slug, 'a-slug')
        self.assertEquals(post2.slug, 'a-slug-2')
        self.assertEquals(post3.slug, 'a-slug')
        self.assertEquals(post4.slug, 'a-slug-2')
