from django.test import TestCase, TransactionTestCase
from .models import Audio
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


def create_user(username, password):
    user = User.objects.create_user(username)
    user.set_password(password)
    user.save()
    return user

# Create your tests here.
class AllTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_user('username', 'password')
        new_audio = Audio(title="title", description="description", owner="owner")
        with open('media_for_tests/audio1.mp3', 'rb') as f:
            new_audio.original = SimpleUploadedFile(name='audio1.mp3', 
                                                    content=f.read(),
                                                    content_type='audio/mp3')
            new_audio.save()

    def test_audio_model_was_saved(self):
        saved_items = Audio.objects.all()
        self.assertEqual(saved_items.count(), 1)
        self.assertTrue(saved_items[0].original)
        self.assertTrue(saved_items[0].title)
        self.assertTrue(saved_items[0].description)
        self.assertTrue(saved_items[0].owner)

    def test_view_page_loads_template(self):
        audio = Audio.objects.first()
        response = self.client.get('/audio/view/%s/' % (audio.pk,))
        self.assertTemplateUsed(response, 'audio/view.html')

    def test_submit_page_loads_template_when_logged_in(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/audio/submit/')
        self.assertTemplateUsed(response, 'submit.html')

    def test_submit_page_redirects_to_login_when_logged_out(self):
        response = self.client.get('/audio/submit/')
        self.assertRedirects(response, '/accounts/login/?next=/audio/submit/')

    def test_saving_after_a_POST_request(self):
        self.client.login(username='username', password='password')
        with open('media_for_tests/Audio1.mp3', 'rb') as upload_audio:
            response = self.client.post(
                '/audio/submit/',
                data={  'original': upload_audio,
                        'title': 'title',
                        'description': 'description',
                    })
        self.assertEqual(Audio.objects.count(), 2)