#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.db.models import Q
from mvc.models import *
from shop_yen.models import *


class Command(BaseCommand):
    help = 'Create Cron Data which help run advertisement email'

    def add_arguments(self, parser):
        parser.add_argument('advertisement_id', type=int)

    def handle(self, *args, **options):
        print("Bắt đầu khởi tạo cron data")
        try:
            advertisement = Advertisement.objects.filter(pk=options['advertisement_id']).first()
            if advertisement:
                crons = list()
                admin = User.objects.filter(email="admin@yenvangmiennam.com").first()

                customers = Customer.objects.filter(contact_type=ContactChoice.E.name)
                for cus in customers:
                    cron = CronAdvertisement.objects.filter(
                        Q(advertisement=advertisement) &
                        Q(customer=cus) &
                        Q(start_at=advertisement.start_at)
                    )
                    if not cron.exists():
                        crons.append(CronAdvertisement(
                            advertisement=advertisement,
                            customer=cus,
                            start_at=advertisement.start_at,
                            created_by=admin,
                            modified_by=admin
                        ))
                        # Create cron advertisement when count = 100
                        if len(crons) >= 100:
                            CronAdvertisement.objects.bulk_create(crons)
                            crons.clear()
                # Case crons > 0 and crons < 100
                if len(crons) > 0:
                    CronAdvertisement.objects.bulk_create(crons)
                    crons.clear()
        except Exception as ex:
            print(ex)
        print("Kết thúc tạo cron data")
