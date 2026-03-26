from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):

        from django.db import connection
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        # Try Django ORM deletion, fallback to raw MongoDB drop if needed
        for model, collection in [
            (Activity, 'activities'),
            (Leaderboard, 'leaderboard'),
            (User, 'users'),
            (Team, 'teams'),
            (Workout, 'workouts'),
        ]:
            try:
                model.objects.all().delete()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'ORM delete failed for {collection}, dropping collection: {e}'))
                db = connection.cursor().db_conn
                db.drop_collection(collection)

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel')
            dc = Team.objects.create(name='DC')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User.objects.create(name='Captain America', email='cap@marvel.com', team=marvel),
                User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User.objects.create(name='Batman', email='batman@dc.com', team=dc),
                User.objects.create(name='Superman', email='superman@dc.com', team=dc),
                User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            ]

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=users[0], type='Running', duration=30, calories=300)
            Activity.objects.create(user=users[1], type='Cycling', duration=45, calories=400)
            Activity.objects.create(user=users[2], type='Swimming', duration=60, calories=500)
            Activity.objects.create(user=users[3], type='Yoga', duration=40, calories=200)
            Activity.objects.create(user=users[4], type='Boxing', duration=50, calories=450)
            Activity.objects.create(user=users[5], type='HIIT', duration=35, calories=350)

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            Workout.objects.create(name='Hero Strength', description='Full body strength workout', suggested_for='Marvel')
            Workout.objects.create(name='Justice Cardio', description='High intensity cardio', suggested_for='DC')

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(team=marvel, points=1200)
            Leaderboard.objects.create(team=dc, points=1100)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
