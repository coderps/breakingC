from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from bc.choices import WHERE_CHOICES, MONTH_CHOICES
from datetime import date

# Create your models here.


class Stuff(models.Model):
    id = models.BigAutoField(primary_key=True)
    where = models.CharField(max_length=40, choices=WHERE_CHOICES)
    name = models.CharField(max_length=80)
    points = models.FloatField(default=0)
    frequency = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    last_done = models.DateField(default=date.today)

    def __str__(self):
        return self.where + ' ' + self.name


class StuffRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    player = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    record = models.ForeignKey(
        Stuff,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    value = models.FloatField(default=0)
    done_on = models.DateField(default=date.today)
    added_on = models.DateField(auto_now=True)

    # multiplier, so if the value is 40% of originial use 0.4 as reduction value
    reduction = models.FloatField(default=1)

    def save(self, *args, **kwargs):
        stuff = Stuff.objects.get(id=self.record.id)
        stuff.last_done = self.done_on
        stuff.save()
        super(StuffRecord, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("INFO: adjusting last_done for the stuff...")
        stuff = Stuff.objects.get(id=self.record.id)
        last_record = StuffRecord.objects.filter(
            record=stuff,
        ).exclude(id=self.id).order_by('-done_on').first()
        if last_record is not None:
            stuff.last_done = last_record.done_on
        else:
            stuff.last_done = date(2023, 6, 1)
        stuff.save()
        super(StuffRecord, self).delete(*args, **kwargs)

    def __str__(self):
        return self.player.username + ', ' + self.record.__str__()


class Shop(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.CharField(max_length=40, unique=True)
    cost = models.FloatField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.item


class ShopRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    item = models.ForeignKey(
        Shop,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    value = models.FloatField(default=0)
    redeemed = models.BooleanField(default=False)
    done_on = models.DateField(default=date.today)
    added_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.buyer.username + ', ' + self.item


class Stat(models.Model):
    id = models.BigAutoField(primary_key=True)
    player = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    points = models.FloatField(default=0)

    def __str__(self):
        return self.player.username + ', ' + str(self.points)


class Vacation(models.Model):
    id = models.BigAutoField(primary_key=True)
    player = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    month = models.IntegerField(
        choices=MONTH_CHOICES, default=timezone.now().month)
    year = models.IntegerField(default=2023)
    points = models.FloatField(default=0)

    def __str__(self):
        return self.player.username + ', ' + str(self.points)


class VacationRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    player = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.RESTRICT,
    )
    taken_on = models.DateField(default=date.today)

    def __str__(self):
        return self.player.username + ', ' + self.taken_on.__str__()


class Setting(models.Model):
    id = models.BigAutoField(primary_key=True)
    what = models.CharField(max_length=50)
    value = models.CharField(max_length=10)
    when = models.DateField(default=date.today)
    yad = models.DateField(default=date.today)
    active = models.BooleanField(default=True)

    def __str__(self):
        return ', '.join([self.what, self.value, self.when.__str__()])
