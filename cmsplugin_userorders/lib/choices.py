
import os

from django.template.loaders.app_directories import app_template_dirs
from django.core.exceptions import ImproperlyConfigured

from cms.models import Placeholder, Page

from .formatting import deslugify

class DynamicChoice(object):
	"""
	Trivial example of creating a dynamic choice
	"""
	blank_option = "- Not Selected -"

	def __iter__(self, *args, **kwargs):
		for choice in self.generate():
			if hasattr(choice,'__iter__'):
				yield (choice[0], choice[1])
			else:
				yield choice, choice

	def __init__(self, *args, **kwargs):
		""" If you do it here it is only initialized once. Then just return generated. """
		self.generated = range(10)

	def generate(self, *args, **kwargs):
		""" If you do it here it is  initialized every time the iterator is used. """
		return range(10)


class PageAttributeDynamicChoices(DynamicChoice):

	def __init__(self, *args, **kwargs):
		super(PageAttributeDynamicChoices, self).__init__(self, *args, **kwargs)

	def generate(self,*args, **kwargs):
		choices = list()
		return choices


class PlaceholdersDynamicChoices(DynamicChoice):

	def __init__(self, *args, **kwargs):
		super(PlaceholdersDynamicChoices, self).__init__(self, *args, **kwargs)

	def generate(self,*args, **kwargs):
		choices = list()
		for item in Placeholder.objects.all().values("slot").distinct():
			choices.append( (
			item['slot'],
			deslugify(item['slot'])
			), )

		return choices

class PageIDsDynamicChoices(DynamicChoice):

	def __init__(self, *args, **kwargs):
		super(PageIDsDynamicChoices, self).__init__(self, *args, **kwargs)

	def generate(self,*args, **kwargs):
		choices = list()
		for item in Page.objects.all():
			if not item.reverse_id :
				continue

			choices.append( (
			item.reverse_id,
			"{0} [{1}]".format(item.get_title(), item.reverse_id)
			), )

		return choices

class DynamicTemplateChoices(DynamicChoice):

	def __init__(self, path=None, include=None, exclude=None, *args, **kwargs):

		super(DynamicTemplateChoices, self).__init__(self, *args, **kwargs)
		self.path = path
		self.include = include # if isinstance(include, (list,tuple)) else (include,)
		self.exclude = exclude # if isinstance(include, (list,tuple)) else (exclude,)

	def generate(self,*args, **kwargs):
		choices = set()
		for template_dir in app_template_dirs:
			choices |= set(self.walkdir(os.path.join(template_dir, self.path)))
		return choices

	def walkdir(self, path=None):

		if not os.path.exists(path):
			return

		for root, dirs, files in os.walk(path):

			if self.include:
				files = filter(lambda x: self.include in x, files)

			if self.exclude:
				files = filter(lambda x: not self.exclude in x, files)

			for item in files :
				fragment = os.path.relpath(os.path.join(root, item), path)
				yield (
				os.path.join(self.path, fragment),
				deslugify(os.path.splitext(item)[0]),
				)
