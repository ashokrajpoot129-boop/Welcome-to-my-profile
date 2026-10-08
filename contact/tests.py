import json

from django.core import mail
from django.test import TestCase, override_settings

from .models import ContactMessage


@override_settings(
	EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
	CONTACT_NOTIFY_EMAIL='site@example.com',
)
class ContactSubmissionTests(TestCase):
	def test_welcome_page_links_to_profile(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'WELCOME')
		self.assertContains(response, 'href="/home/"')

	def test_profile_links_to_mysql_backed_contact_form(self):
		profile_response = self.client.get('/home/')
		contact_response = self.client.get('/contact/')

		self.assertEqual(profile_response.status_code, 200)
		self.assertContains(profile_response, 'href="/contact/"')
		self.assertEqual(contact_response.status_code, 200)
		self.assertContains(contact_response, 'Send a message')
		self.assertContains(contact_response, 'id_mobile_number')
		self.assertContains(contact_response, 'contact/ashok%20kumar.jpeg')

	def test_contact_form_submission_is_saved(self):
		response = self.client.post('/submit/', {
			'name': 'Asha',
			'email': 'asha@example.com',
			'mobile_number': '+91 98765 43210',
			'message': 'Please contact me.',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Your message was saved successfully.')
		self.assertEqual(ContactMessage.objects.count(), 1)
		self.assertEqual(ContactMessage.objects.get().mobile_number, '+91 98765 43210')
		self.assertEqual(len(mail.outbox), 2)
		self.assertEqual(mail.outbox[0].to, ['site@example.com', 'ashokrajpoot129@gmail.com'])
		self.assertIn('Asha', mail.outbox[0].body)
		self.assertIn('asha@example.com', mail.outbox[0].body)
		self.assertIn('Please contact me.', mail.outbox[0].body)
		self.assertEqual(mail.outbox[1].to, ['asha@example.com'])
		self.assertIn('received your message', mail.outbox[1].body)

	def test_json_submission_notifies_site_and_sends_confirmation(self):
		response = self.client.post(
			'/api/contact/',
			data=json.dumps({
				'name': 'Asha',
				'email': 'asha@example.com',
				'mobile_number': '+91 98765 43210',
				'message': 'I would like to talk about a project.',
			}),
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['message'], 'Your message was saved successfully.')
		self.assertEqual(ContactMessage.objects.count(), 1)
		saved_message = ContactMessage.objects.get()
		self.assertEqual(saved_message.name, 'Asha')
		self.assertEqual(saved_message.email, 'asha@example.com')
		self.assertEqual(saved_message.mobile_number, '+91 98765 43210')
		self.assertEqual(saved_message.message, 'I would like to talk about a project.')
		self.assertEqual(len(mail.outbox), 2)
		self.assertEqual(mail.outbox[0].to, ['site@example.com', 'ashokrajpoot129@gmail.com'])
		self.assertIn('Asha', mail.outbox[0].body)
		self.assertIn('+91 98765 43210', mail.outbox[0].body)
		self.assertEqual(mail.outbox[1].to, ['asha@example.com'])

	def test_invalid_email_is_rejected_without_sending_mail(self):
		response = self.client.post(
			'/api/contact/',
			data=json.dumps({'name': 'Asha', 'email': 'not-an-email', 'message': 'Hello'}),
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(mail.outbox, [])
