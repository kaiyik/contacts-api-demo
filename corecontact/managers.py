from django.db import models


class PeopleManager(models.Manager):
    def textsearch(self, name):
        if name is not None:
            return self.filter(name__icontains=name)
        else:
            return None


class ContactManager(models.Manager):
    def textsearchemailnum(self, email, number):
        if email is not None and number is not None:
            return self.filter(
                models.Q(email__icontains=email) |
                models.Q(number__icontains=number)
            )
        elif email is None and number is not None:
            return self.filter(
                models.Q(number__icontains=number)
            )
        elif email is not None and number is None:
            return self.filter(
                models.Q(email__icontains=email)
            )
        else:
            return None

    
   
