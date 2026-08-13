from django.core.management.base import BaseCommand
from django.conf import settings
import random
from faker import Faker
import inventory.models as m
from inventory_auth.models import User


MIN_OWNERS = 10
MIN_LOCATIONS = 10
MIN_TAGS = 10
MIN_ITEMS = 3
MAX_ITEMS = 25
MIN_HISTORY_ITEMS = 0
MAX_HISTORY_ITEMS = 5


FAKE = Faker(locale=settings.LANGUAGE_CODE)


class Command(BaseCommand):
    help = "Generates dummy data"

    def log(self, entity, params):
        self.stdout.write(
            self.style.SUCCESS(
                f'Created {entity} "%s"' % params
            )
        )

    def random_item_count(self):
        return random.randint(MIN_ITEMS, MAX_ITEMS)

    def handle(self, *args, **options):
        self.generate_users()
        self.generate_locations()
        self.generate_tags()
        owners = m.InventoryOwner.active.all()
        if owners.count() < MIN_OWNERS:
            owners_to_create = MIN_OWNERS - owners.count()
            for _ in range(owners_to_create):
                params = {"fullname": FAKE.name()}
                m.InventoryOwner.objects.create(**params)
                self.log("inventory owner", params)

        for owner in owners.order_by('?')[:MIN_OWNERS]:
            self.generate_inventory_group(owner)

    def generate_users(self):
        users_needed = MIN_OWNERS - User.objects.count()
        users_needed = max(0, users_needed)
        for _ in range(users_needed):
            params = {
                "username": FAKE.user_name()
            }
            User.objects.create(**params)
            self.log("user", params)

    def generate_locations(self):
        locations_needed = MIN_LOCATIONS - m.Location.objects.count()
        locations_needed = max(0, locations_needed)
        for _ in range(locations_needed):
            params = {"name": FAKE.address()}
            m.Location.objects.create(**params)
            self.log("inventory location", params)

    def generate_tags(self):
        tags_needed = MIN_TAGS - m.Tag.objects.count()
        tags_needed = max(0, tags_needed)
        for _ in range(tags_needed):
            params = {"name": FAKE.cryptocurrency_code()}
            m.Tag.objects.create(**params)
            self.log("tag", params)

    def generate_inventory_group(self, owner):
        for _ in range(self.random_item_count()):
            params = {"owner": owner, "name": FAKE.text(10)}
            group = m.InventoryGroup.objects.create(**params)
            self.log("inventory group", params)
            self.generate_inventory_items(group)

    def generate_inventory_items(self, group):
        for _ in range(self.random_item_count()):
            params = {
                "group": group,
                "name": FAKE.text(20),
                "quantity": random.randint(1, 3)
            }
            if random.random() > 0.7:
                params["inventory_number"] = FAKE.pystr()

            if random.random() > 0.3:
                params["serial_number"] = FAKE.pystr()

            item = m.InventoryItem.objects.create(**params)
            self.log("inventory item", params)

            self.generate_location_history(item)
            self.generate_comments(item)
            self.maybe_attach_tags(item)

    def generate_location_history(self, item):
        history_items = random.randint(
            MIN_HISTORY_ITEMS, MAX_HISTORY_ITEMS
        )

        for _ in range(history_items):
            location = m.Location.objects.order_by('?').first()
            author = User.objects.order_by('?').first()
            params = {
                "location": location,
                "inventory_item": item,
                "author": author
            }
            m.LocationHistory.objects.create(**params)
            self.log("location history", params)
            item.location = location
            item.save()

    def generate_comments(self, item):
        comments = random.randint(
            MIN_HISTORY_ITEMS, MAX_HISTORY_ITEMS
        )

        for _ in range(comments):
            author = User.objects.order_by('?').first()
            text = " ".join(FAKE.sentences(self.random_item_count()))
            params = {
                "author": author,
                "content_object": item,
                "text": text
            }
            m.Comment.objects.create(**params)
            self.log("comment", params)

    def maybe_attach_tags(self, item):
        tags = random.randint(0, 2)
        for _ in range(tags):
            tag = m.Tag.objects.order_by('?').first()
            item.tags.add(tag)
