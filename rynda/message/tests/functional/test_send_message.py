# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from core.factories import FuzzyGeometryCollection
from geozones.models import Location
from message.models import Message
from message.factories import MessageFactory
from test.factories import UserFactory


class MessageDataMixin():
    def generate_message(self):
        contacts = {
            'first_name': 'test',
            'last_name': 'user',
            'email': 'me@local.host',
            'phone': '1234567890',
        }
        loc_data = {
            'coordinates': FuzzyGeometryCollection().fuzz(),
            'address': 'test address',
        }
        data = MessageFactory.attributes(create=False)
        data.update(contacts)
        data.update(loc_data)
        return data

    def fill_form(self):
        """ Вспомогательный метод заполнения формы данными """
        form = self.page.forms['mainForm']
        form['title'] = self.data['title']
        form['message'] = self.data['message']
        form['is_anonymous'] = self.data['is_anonymous']
        form['allow_feedback'] = self.data['allow_feedback']
        form['email'] = self.data['email']
        form['address'] = self.data['address']
        form['coordinates'] = self.data['coordinates']
        return form


class TestAnonymousMessage(WebTest, MessageDataMixin):
    """ Отправка сообщения незарегистрированным пользователем """

    def setUp(self):
        self.page = self.app.get(reverse('create-request'))
        self.data = self.generate_message()

    def test_store_anonymous_message(self):
        """ Проверка сохранения данных анонимного сообщения """
        before = Message.objects.count()
        form = self.fill_form()
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())

    def test_creator_data(self):
        form = self.fill_form()
        form.submit()
        msg = Message.objects.get()
        self.assertEqual(msg.user_id, settings.ANONYMOUS_USER_ID)

    def test_message_is_anonymous(self):
        form = self.fill_form()
        form.submit()
        msg = Message.objects.get()
        self.assertEqual(msg.user_id, settings.ANONYMOUS_USER_ID)


class TestSendRequestMessage(WebTest, MessageDataMixin):
    """ Функционал создания просьбы о помощи """

    def setUp(self):
        self.user = UserFactory()
        self.page = self.app.get(
            reverse('create-request'),
            user=self.user.username)
        self.data = self.generate_message()

    def test_get_form(self):
        form = self.page.forms['mainForm']
        self.assertIsNotNone(form)

    def test_message_saved(self):
        before = Message.objects.count()
        form = self.fill_form()
        form.submit()
        self.assertEquals(before + 1, Message.objects.count())


class TestRequestMessageParameters(WebTest, MessageDataMixin):
    """ Tests for new request parameters """
    def setUp(self):
        self.user = UserFactory()
        self.data = self.generate_message()
        self.form = self.app.get(
            reverse('create-request'), user=self.user.username
        ).forms['mainForm']

    def send_form(self):
        self.form['title'] = self.data['title']
        self.form['message'] = self.data['message']
        self.form['is_anonymous'] = self.data['is_anonymous']
        self.form['allow_feedback'] = self.data['allow_feedback']
        self.form['email'] = self.data['email']
        self.form['address'] = self.data['address']
        self.form['coordinates'] = self.data['coordinates']
        self.form.submit()

    def test_message_user(self):
        """ Test message author """
        self.send_form()
        msg = Message.objects.get()
        self.assertEquals(msg.user, self.user)

    def test_message_flags(self):
        """ Test default message flags """
        self.send_form()
        msg = Message.objects.get()
        self.assertEquals(Message.NEW, msg.status)
        self.assertFalse(msg.is_removed)
        self.assertTrue(msg.is_anonymous)
        self.assertTrue(msg.allow_feedback)
        self.assertFalse(msg.is_virtual)
        self.assertFalse(msg.is_important)
        self.assertFalse(msg.is_active)

    def test_nonanonymous_message(self):
        """ Send non-anonymous message """
        self.data['is_anonymous'] = False
        self.send_form()
        msg = Message.objects.get()
        self.assertFalse(msg.is_anonymous)

    def test_no_feedback(self):
        """ Send message and do not want feedback """
        self.data['allow_feedback'] = False
        self.send_form()
        msg = Message.objects.get()
        self.assertFalse(msg.allow_feedback)

    def test_message_location(self):
        loc_cnt = Location.objects.count()
        self.send_form()
        self.assertEqual(loc_cnt + 1, Location.objects.count())