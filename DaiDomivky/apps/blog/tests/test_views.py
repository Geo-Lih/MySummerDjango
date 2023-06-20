from DaiDomivky.DaiDomivky.constants import StatusType
from DaiDomivky.apps.blog.models import Post
from DaiDomivky.apps.blog.views import PostCreateView, PostDetailView, PostListView, PostUpdateView
from DaiDomivky.apps.user.models import CustomUser

from django.test import Client, TestCase


class BaseTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = CustomUser.objects.create(email='Test@gmail.com', password='test12345678')

    def create_published_post(self, **kwargs):
        post_data = {
            'title': 'Published Post',
            'slug': 'published-post',
            'status': StatusType.PUBLISHED,
            'author': self.user,
            'content': 'Loren Ipsum',
        }
        post_data.update(kwargs)
        return Post.objects.create(**post_data)

    def create_draft_post(self, **kwargs):
        post_data = {
            'title': 'Draft Post',
            'slug': 'draft-post',
            'status': StatusType.DRAFT,
            'author': self.user,
            'content': 'Loren Ipsum',
        }
        post_data.update(kwargs)
        return Post.objects.create(**post_data)


class TestPostListView(BaseTestCase):
    def test_view_template(self):
        response = self.c.get('/blog/')
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_view_attrs(self):
        view = PostListView()
        self.assertEquals(view.model, Post)
        self.assertEquals(view.template_name, 'blog/index.html')
        self.assertEquals(view.context_object_name, 'list')

    def test_auth_user_queryset(self):
        self.c.force_login(self.user)
        published_post = self.create_published_post()
        draft_post = self.create_draft_post()
        response = self.c.get('/blog/')
        self.assertIn(published_post, response.context['list'])
        self.assertIn(draft_post, response.context['list'])

    def test_unauth_user_queryset(self):
        published_post = self.create_published_post()
        draft_post = self.create_draft_post()
        response = self.c.get('/blog/')
        self.assertIn(published_post, response.context['list'])
        self.assertNotIn(draft_post, response.context['list'])

    def test_auth_user_only_draft(self):
        self.c.force_login(self.user)
        draft_post = self.create_draft_post()
        response = self.c.get('/blog/')
        self.assertIn(draft_post, response.context['list'])
        self.assertFalse(any(post.status == StatusType.PUBLISHED for post in response.context['list']))

    def test_auth_user_only_published(self):
        self.c.force_login(self.user)
        published_post = self.create_published_post()
        response = self.c.get('/blog/')
        self.assertIn(published_post, response.context['list'])
        self.assertFalse(any(post.status == StatusType.DRAFT for post in response.context['list']))


class TestPostDetailView(BaseTestCase):
    def test_view_template(self):
        post = self.create_published_post()
        response = self.c.get(f'/blog/{post.slug}')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_view_attrs(self):
        view = PostDetailView()
        self.assertEquals(view.model, Post)
        self.assertEquals(view.template_name, 'blog/post_detail.html')
        self.assertEquals(view.context_object_name, 'post')

    def test_publish_post_access(self):
        post = self.create_published_post()
        response = self.c.get(f'/blog/{post.slug}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['post'].status, StatusType.PUBLISHED)

    def test_draft_post_access(self):
        post = self.create_draft_post()
        response = self.c.get(f'/blog/{post.slug}')
        self.assertEqual(response.status_code, 404)

    def test_publish_post_access_as_author(self):
        self.c.force_login(self.user)
        post = self.create_published_post()
        response = self.c.get(f'/blog/{post.slug}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['post'].status, StatusType.PUBLISHED)

    def test_draft_post_access_as_author(self):
        self.c.force_login(self.user)
        post = self.create_draft_post()
        response = self.c.get(f'/blog/{post.slug}')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['post'].status, StatusType.DRAFT)


class TestPostCreateView(BaseTestCase):
    def test_view_template(self):
        self.c.force_login(self.user)
        response = self.c.get('/blog/create/')
        self.assertTemplateUsed(response, 'blog/post_create.html')

    def test_view_attrs(self):
        view = PostCreateView()
        self.assertEquals(view.model, Post)
        self.assertEquals(view.template_name, 'blog/post_create.html')
        self.assertEquals(view.fields, ['title', 'content', 'status'])

    def test_unauth_access(self):
        response = self.c.get('/blog/create/')
        self.assertEquals(response.status_code, 404)

    def test_auth_access(self):
        self.c.force_login(self.user)
        response = self.c.get('/blog/create/')
        print('alertalertalert', response.status_code)
        self.assertEquals(response.status_code, 200)

    def test_creating_post(self):
        self.c.force_login(self.user)
        initial_count = Post.objects.count()
        response = self.c.post('/blog/create/', data={'title': 'test',
                                                      'status': StatusType.PUBLISHED,
                                                      'author': self.user,
                                                      'content': 'Loren Ipsum'})
        final_count = Post.objects.count()

        # Verify that a new Post object has been created
        self.assertEqual(final_count, initial_count + 1)
        self.assertRedirects(response, '/blog/')

    def test_creating_post_auth(self):
        self.c.force_login(self.user)
        response = self.c.post('/blog/create/', data={'title': 'test',
                                                      'status': StatusType.PUBLISHED,
                                                      'author': self.user,
                                                      'content': 'Loren Ipsum'})

        self.assertEquals(response.status_code, 302)

    def test_creating_post_unauth(self):
        response = self.c.post('/blog/create/', data={'title': 'test',
                                                      'status': StatusType.PUBLISHED,
                                                      'author': self.user,
                                                      'content': 'Loren Ipsum'})
        self.assertEquals(response.status_code, 404)

    def test_invalid_status_selection(self):
        self.c.force_login(self.user)
        response = self.c.post('/blog/create/', data={'title': 'test',
                                                      'status': 'invalid status',
                                                      'author': self.user,
                                                      'content': 'Loren Ipsum'})
        self.assertFormError(response, 'form', 'status',
                             'Select a valid choice. invalid status is not one of the available choices.')


class TestPostUpdateView(BaseTestCase):
    def test_view_template(self):
        self.c.force_login(self.user)
        post = self.create_published_post()
        response = self.c.get(f'/blog/{post.slug}/update/')
        self.assertTemplateUsed(response, 'blog/post_update.html')

    def test_view_attrs(self):
        view = PostUpdateView()
        self.assertEquals(view.model, Post)
        self.assertEquals(view.template_name, 'blog/post_update.html')
        self.assertEquals(view.fields, ['title', 'content', 'status'])

    def test_unauth_access(self):
        post = self.create_published_post()
        response = self.c.get(f'/blog/{post.slug}/update/')
        self.assertEquals(response.status_code, 404)

    def test_auth_access(self):
        self.c.force_login(self.user)
        post = self.create_published_post()
        response = self.c.get(f'/blog/{post.slug}/update/')
        self.assertEquals(response.status_code, 200)

    def test_update_post(self):
        self.c.force_login(self.user)
        post = self.create_published_post()
        response = self.c.post(f'/blog/{post.slug}/update/', data={'title': 'Updated Title',
                                                                   'status': StatusType.DRAFT,
                                                                   'author': self.user,
                                                                   'content': 'Updated Content'})
        updated_post = Post.objects.get(id=post.id)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(updated_post.title, 'Updated Title')
        self.assertEquals(updated_post.status, StatusType.DRAFT)
        self.assertEquals(updated_post.content, 'Updated Content')
