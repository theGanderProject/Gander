from django.test import TestCase, TransactionTestCase, RequestFactory
from django.core.urlresolvers import resolve
from .views import HomePageView, post_favorite, EditView
from .models import Image, ImageForm, Tag
import os
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage

def create_user(username, password):
    user = User.objects.create_user(username)
    user.set_password(password)
    user.save()
    return user

class AllTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = create_user('username', 'password')
        with open('media_for_tests/testImage1.jpg', 'rb') as f:
            original = SimpleUploadedFile(  name='testImage1.jpg', 
                                            content=f.read(),
                                            content_type='image/jpeg')

            image = Image.objects.create(   title="title",
                                    description="description",
                                    owner=user,
                                    original=original)

        t1 = Tag.objects.create(text="tag 1")
        t2 = Tag.objects.create(text="tag 2")
        t3 = Tag.objects.create(text="tag 3")
        t4 = Tag.objects.create(text="tag 4")
        image.tag.add(t1, t2, t3, t4)


    def test_image_model_was_saved(self):
        saved_items = Image.objects.all()
        self.assertEqual(saved_items.count(), 1)
        image = saved_items[0]
        self.assertTrue(image.original)
        self.assertTrue(image.title)
        self.assertTrue(image.description)
        self.assertTrue(image.owner)
        self.assertTrue(image.thumbnail)
        self.assertTrue(image.small)
        self.assertTrue(image.medium)
        self.assertTrue(image.large)
        self.assertFalse(image.huge)
        self.assertEqual(image.favorite.count(), 0)
        self.assertEqual(image.md5, "3a6f83fa96c06fbed484dfa8b9f69ac1")
        self.assertEqual(image.tag.count(), 4)

    def test_user_can_favorite(self):
        user = User.objects.first()
        image = Image.objects.first()

        user_favorite_count = user.image_favorite.all().count()
        self.assertEqual(user_favorite_count, 0)

        image_favorite_count = image.favorite.count()
        self.assertEqual(image_favorite_count, 0)

        user.image_favorite.add(image)

        user_favorite_count = user.image_favorite.all().count()
        self.assertEqual(user_favorite_count, 1)

        image_favorite_count = image.favorite.count()
        self.assertEqual(image_favorite_count, 1)

    def test_view_page_loads_template(self):
        image = Image.objects.first()
        response = self.client.get('/art/view/%s/' % (image.pk,))
        self.assertTemplateUsed(response, 'visual_art/view.html')

    def test_art_page_loads_template(self):
        response = self.client.get('/user/username/art/')
        self.assertTemplateUsed(response, 'visual_art/gallery.html')

    def test_gallery_page_loads_template(self):
        response = self.client.get('/art/')
        self.assertTemplateUsed(response, 'visual_art/art.html')

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.__name__, HomePageView.__name__)

    def test_submit_page_loads_template_when_logged_in(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/art/submit/')
        self.assertTemplateUsed(response, 'submit.html')

    def test_submit_page_redirects_to_login_when_logged_out(self):
        response = self.client.get('/art/submit/')
        self.assertRedirects(response, '/accounts/login/?next=/art/submit/')

    def test_saving_a_single_image_after_a_POST_request(self):
        self.client.login(username='username', password='password')
        with open('media_for_tests/testImage1.jpg', 'rb') as upload_image:
            response = self.client.post(
                '/art/submit/',
                data={  'original': upload_image,
                    })
        self.assertEqual(Image.objects.count(), 2)
    
    
    def test_not_allowed_to_favorite_via_POST_if_not_logged_in(self):
        self.client.post('/art/view/1/favorite')
        image = Image.objects.first()
        self.assertEqual(0, image.favorite.count())

    def test_can_favorite_via_POST_when_logged_in(self):
        user = create_user('hsgjfrsagfdhf', 'password')
        self.client.login(username='hsgjfrsagfdhf', password='password')
        self.client.post('/art/view/1/favorite')
        image = Image.objects.first()
        self.assertEqual(1, image.favorite.count())
        user.refresh_from_db()
        self.assertEqual(1, user.image_favorite.count())

    def test_user_cannot_favorite_their_own_art_via_POST(self):
        self.client.login(username='username', password='password')
        self.client.post('/art/view/1/favorite')
        image = Image.objects.first()
        self.assertEqual(0, image.favorite.count())
        user = User.objects.first()
        self.assertEqual(0, user.image_favorite.count())

    def test_favorite_url_resolves_to_post_favorite_view(self):
        found = resolve('/art/view/1/favorite')
        self.assertEqual(found.func, post_favorite)

    def test_user_can_remove_favorite(self):
        user = create_user('hsgjfrsagfdhf', 'password')
        self.client.login(username='hsgjfrsagfdhf', password='password')
        self.client.post('/art/view/1/favorite')
        user.refresh_from_db()
        self.assertEqual(1, user.image_favorite.count())
        self.client.post('/art/view/1/favorite')
        user.refresh_from_db()
        self.assertEqual(0, user.image_favorite.count())

    def test_edit_url_resolves_to_edit_view(self):
        found = resolve('/art/edit/1/')
        self.assertEqual(found.func.__name__, EditView.__name__)

    def test_edit_template_is_used_for_edit_page(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/art/edit/1/')
        self.assertTemplateUsed(response, 'visual_art/edit.html')

    def test_owner_can_edit_image_submission(self):
        self.client.login(username='username', password='password')
        self.client.post(
            '/art/edit/1/',
            data={  'title': '',
                    'description': '',
                    #'tag': [1, 2, 3, 4]
                })
        image = Image.objects.first()
        self.assertEqual(image.title, '')
        self.assertEqual(image.description, '')


    def test_nonowner_cannot_edit_image_submission(self):
        user = create_user('hsgjfrsagfdhf', 'password')
        self.client.login(username='hsgjfrsagfdhf', password='password')
        self.client.post(
            '/art/edit/1/',
            data={  'title': '',
                    'description': '',
                })
        image = Image.objects.first()
        self.assertEqual(image.title, 'title')
        self.assertEqual(image.description, 'description')


        """
    def test_favoriting_an_existing_image(self):
        self.client.login(username='username', password='password')
        response = self.client.post('/art/view/1/favorite')
        image = Image.objects.first()
        self.assertEqual(1, image.favorite_count)

    def test_removing_favorite_from_an_image(self):
        self.client.login(username='username', password='password')
        response = self.client.post('/art/view/1/favorite')
        response = self.client.post('/art/view/1/favorite')
        image = Image.objects.first()
        self.assertEqual(0, image.favorite_count)
        """