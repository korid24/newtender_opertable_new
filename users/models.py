from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

BANKS = ['Сбербанк', 'МодульБанк']


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    telegram_id = models.IntegerField(_('telegram id'), null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        '''Returns the first_name plus the last_name,
            with a space in between.'''
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''Returns the short name for the user.'''
        return self.first_name

    def in_stock_by_banks(self):
        '''Returns the current balance by banks,
        includes external and internal transactions results'''
        result = {}
        for bank in BANKS:
            amount_in_bank_by_externals = sum(
                [tr.for_count() for tr in self.transactions.filter(bank=bank)])
            internal_receipts = sum(
                [tr.amount for tr in self.internal_receipts.filter(
                    recipient_bank=bank)])
            internal_write_offs = sum(
                [tr.amount for tr in self.internal_write_offs.filter(
                    donor_bank=bank)])
            result[bank] = (amount_in_bank_by_externals +
                            float(internal_receipts) -
                            float(internal_write_offs))
        return result

    def in_stock_total(self):
        '''Returns the total balance'''
        return sum(self.in_stock_by_banks().values())
