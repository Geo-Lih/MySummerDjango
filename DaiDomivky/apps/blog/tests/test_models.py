from DaiDomivky.apps.blog.models import Post
from DaiDomivky.apps.user.models import CustomUser

from django.test import TestCase
from django.urls import reverse


class PostTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email='Test@gmail.com', password='test12345678')
        self.post = Post.objects.create(title='test', author=self.user, slug='test',
                                        content='Lorem ipsum dolor sit amet.')

    def test_get_absolute_url_method(self):
        expected_url = reverse('blog:detail', args=(self.post.slug,))
        self.assertEquals(self.post.get_absolute_url(), expected_url)

    def test_str_method(self):
        expected_string = 'test by Test@gmail.com'
        self.assertEquals(self.post.__str__(), expected_string)

    def test_field_values(self):
        self.assertEqual(self.post.title, 'test')
        self.assertEqual(self.post.slug, 'test')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.content, 'Lorem ipsum dolor sit amet.')
        self.assertEqual(self.post.status, 0)

    def test_unique_constraints(self):
        with self.assertRaises(Exception):
            # Creating a post with the same title and slug should raise an exception
            Post.objects.create(
                title='test',
                slug='test',
                author=self.user,
                content='Lorem ipsum dolor sit amet.',
                status=1
            )

    def test_ordering(self):
        # Create multiple posts with different created_on values
        post1 = Post.objects.create(
            title='Post 1',
            slug='post-1',
            author=self.user,
            content='Lorem ipsum dolor sit amet.',
            status=1
        )
        post2 = Post.objects.create(
            title='Post 2',
            slug='post-2',
            author=self.user,
            content='Lorem ipsum dolor sit amet.',
            status=1
        )
        post3 = Post.objects.create(
            title='Post 3',
            slug='post-3',
            author=self.user,
            content='Lorem ipsum dolor sit amet.',
            status=1
        )

        # Query the database and assert the ordering
        posts = Post.objects.all()
        self.assertEquals(posts[0], post3)
        self.assertEquals(posts[1], post2)
        self.assertEquals(posts[2], post1)
