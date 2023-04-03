from django.core.management.base import BaseCommand, CommandError
from content.models import *


class Command(BaseCommand):
    help = ''''
    Delete all data from the model accroding to category you have chosen.
    Syntax: python manage.py delcat <category_name>.
    '''
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for category_name in options['category_name']:
            self.stdout.write("Do you really want to delete chosen category from the models? Write yes/no")
            answer = input()
            if answer == 'yes':
                try:
                    category_id = Category.objects.filter(category=category_name).get().id
                    posts = PostCategory.objects.filter(category_id=category_id)
                    for post in posts:
                        Post.objects.get(pk=post.post_id).delete()
                    PostCategory.objects.filter(category_id=category_id).delete()
                    self.stdout.write(self.style.SUCCESS('All posts with chosen category were succesfully deleted!'))
                except:
                    self.stdout.write(self.style.ERROR('Unknown category name!'))
            else:
                self.stdout.write(self.style.ERROR('Operation was denied!'))
                    