from __future__ import unicode_literals
import math

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse

TRANSACTION_TYPE_CHOICES = (
    (1, _('Приход с налогом')),
    (2, _('Приход без налога')),
    (3, _('Вывод через карту')),
    (4, _('Другой вывод'))
)

BANK_CHOISES = (
    ('Сбербанк', 'Сбер'),
    ('МодульБанк', 'Модуль')
)


class Transaction(models.Model):
    author = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='transactions')
    amount = models.DecimalField(_('Сумма'), max_digits=10, decimal_places=2)
    date = models.DateField(_('Дата операции'), default=timezone.now)
    comment = models.TextField(_('Комментарий'), blank=True, null=True)
    transaction_type = models.IntegerField(
        _('Тип операции'),
        choices=TRANSACTION_TYPE_CHOICES,
        default=1)
    bank = models.CharField(
        _('Банк зачисления / списания'),
        max_length=10,
        choices=BANK_CHOISES,
        default='Сбербанк')
    creation_time = models.DateTimeField(
        _('Время создания операции'),
        auto_now_add=True)
    change_time = models.DateTimeField(
        _('Время изменения операции'),
        auto_now=True)

    class Meta:
        verbose_name = 'Внешняя операция'
        verbose_name_plural = 'Внешние операции'
        ordering = ['-date', '-id']

    @property
    def tax(self):
        '''Returns the tax of the transaction'''
        if self.transaction_type == 1:
            return math.ceil(float(self.amount) * 6) / 100
        else:
            return 0

    def for_count(self):
        '''Returns the effect of a transaction on the balance'''
        if self.transaction_type < 3:
            return float(self.amount) - self.tax
        else:
            return math.floor(float(self.amount)) * (-1)

    def get_absolute_url(self):
        return reverse(
            'external_transaction_details_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse(
            'external_transaction_update_url', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse(
            'external_transaction_delete_url', kwargs={'id': self.id})


class InternalTransaction(models.Model):
    author = models.ForeignKey(
        to='users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_internal_transactions')
    amount = models.DecimalField(_('Сумма'), max_digits=10, decimal_places=2)
    donor_user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='internal_write_offs',
        verbose_name='Пользователь, у которого списываются деньги')
    donor_bank = models.CharField(
        _('Банк списания'),
        max_length=10,
        choices=BANK_CHOISES,
        default='Сбербанк')
    recipient_user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='internal_receipts',
        verbose_name='Пользователь, которому зачисляются деньги')
    recipient_bank = models.CharField(
        _('Банк зачисления'),
        max_length=10,
        choices=BANK_CHOISES,
        default='МодульБанк')
    comment = models.TextField(_('Комментарий'), blank=True, null=True)
    date = models.DateField(_('Дата операции'), default=timezone.now)
    creation_time = models.DateTimeField(
        _('Время создания операции'),
        auto_now_add=True)
    change_time = models.DateTimeField(
        _('Время изменения операции'),
        auto_now=True)

    class Meta:
        verbose_name = 'Внутренняя операция'
        verbose_name_plural = 'Внутренние операции'
        ordering = ['-date', '-id']

    def get_absolute_url(self):
        return reverse(
            'internal_transaction_details_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse(
            'internal_transaction_update_url', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse(
            'internal_transaction_delete_url', kwargs={'id': self.id})
