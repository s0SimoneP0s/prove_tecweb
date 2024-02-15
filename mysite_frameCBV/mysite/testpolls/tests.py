from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from .models import Question

# test model
class QuestionMethodTests(TestCase):
  def test_was_published_recently_with_future_question(self):
    """
    was_published_recently() should return False for questions whose
    pub_date is in the future
    """
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(“Question?”, pub_date=time)
    self.assertEqual(future_question.was_published_recently(), False)


# si esegue con python manage.py test polls



  def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() should return False for
    questions whose pub_date is older than 1 day
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Question(“Old”, pub_date=time)
    self.assertEqual(old_question.was_published_recently(), False)



  def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() should return True for
    questions whose pub_date is within the last day
    """
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_question = Question(“Recent”, pub_date=time)
    self.assertEqual(recent_question.was_published_recently(), True)


# test view

from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question

def create_question(question_text, days):
  """
  Creates a question: days represent the offset to now: negative
  for questions published in the past, positive for those in the future
  """
  time = timezone.now() + datetime.timedelta(days=days) # days è un offset rispetto ad oggi
  return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionViewTests(TestCase):
  def test_index_view_with_no_questions(self):
    """
    No questions --> "No polls are available"
    message should be displayed.
    controlla codice, messaggio, latest_questions_list==None
    """
    response = self.client.get(reverse('polls:index'))  # elf.client (ereditato da classe TestCase)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [ ]) # Accetta Queryset → liste

    



