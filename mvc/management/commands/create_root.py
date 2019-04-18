#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from mvc.models import User


class Command(BaseCommand):
    help = 'Create root for system'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(email="tranthaibinh111@gmail.com").exists():
                print("Begin create root")
                if options['username'] and options['password']:
                    user = User.objects.create_user(
                        first_name="root",
                        last_name="",
                        username=options['username'],
                        password=options['password'],
                        email="admin@yenvangmiennam.com",
                        is_superuser=True,
                        is_staff=True,
                        timezone="Asia/Ho_Chi_Minh"
                    )
                    print(user)
                print("End!")
        except Exception as ex:
            raise ex
