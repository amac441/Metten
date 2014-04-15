from django.db import models
import re
from gooser import Gooser


#

CONTENT_CHOICES = (
    ('Article', 'Article'),
    ('Podcast', 'Podcast'),
    ('Course', 'Course'),
    ('Meeting', 'Meeting')
                   )

class AddersManager(models.Manager):
    def items_for_user(self, user):
        return super(AddersManager, self).get_queryset().filter(
            Q(user_id=user.id))               
    
    def new_adder(self, user, title, description):
        adder = Adder(user = user,
                      title = title,
                      description = description
                      )        
        return adder                                         

class Adder(models.Model):
    user = models.ForeignKey('auth.User', related_name='adder')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text=(
        "If omitted, the description will be the post's title."))
    is_completed = models.BooleanField(default=True, blank=True)
    content_type = models.CharField(max_length=10, default='Article', choices = CONTENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = AddersManager()

    class Meta:
        get_latest_by = 'timestamp'

    #python manage.py sql appname
    #python manage.py syndb  - doesnt do DB migration
        #it will not alter tables  - in Django 1.7 they will have migrations

    #python manage.py dbshell
        #drop table posts_adder
        #exit
        #then run syncdb again

    def __str__(self):
        return "{0}".format(self.title)


    def email_in(self, data, user):
        
        g = Gooser()
        
        #---parse data---
        
        sender    = data.get('sender')
        recipient = data.get('recipient')
        subject   = data.get('subject', '')
        body_plain = data.get('body-plain', '')


        #---perform logic---
        
        # bounce sender address off users table to find match (later)
        user_email = user

        # check recipient

        if recipient == 'loggit@mettentot.com':
         
        # check if article was read
            if subject == 'done':
                is_comp_email = True
            elif subject == 'later':
                is_comp_email = False
            else:
                return 'Bad Subject'

        # check if the description is a website
        
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body_plain)

            if len(urls) > 1:
            #do something  - like call the GOOSE and SAVE methods twice for each thing
                a = 1

                #query = Adder.objects.create(user = user_email, 
                #title=title_email, 
                #description = des_email, 
                #is_completed = is_comp_email
                #)

               #query.save()

            else:
            #call goose

                response = g.goosing(str(urls[0]))
                title_email = response['title']
                des_email = response['text']

            
            #save it       
                query = Adder.objects.create(user = user_email, 
                          title=title_email, 
                          description = des_email, 
                          is_completed = is_comp_email
                          )
               #query.save()

        else:
            return 'Bad Recipient'

        return 'OK'

