from django.core.management.base import BaseCommand
from courses.models import Language, CourseLevel


class Command(BaseCommand):
    help = 'Populate initial language and course data'

    def handle(self, *args, **options):
        languages_data = [
            {
                'name': 'Japanese',
                'flag_emoji': '🇯🇵',
                'description': 'Master the elegant Japanese language and immerse yourself in one of the world\'s most fascinating cultures.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Chinese',
                'flag_emoji': '🇨🇳',
                'description': 'Learn Mandarin Chinese and unlock opportunities in the world\'s most spoken language.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Hebrew',
                'flag_emoji': '🇮🇱',
                'description': 'Discover the ancient Hebrew language and connect with its rich historical and cultural heritage.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Korean',
                'flag_emoji': '🇰🇷',
                'description': 'Explore Korean language and dive into K-culture, K-pop, and modern Korean society.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Russian',
                'flag_emoji': '🇷🇺',
                'description': 'Master Russian and access the language of Tolstoy, Dostoyevsky, and rich Slavic culture.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Dutch',
                'flag_emoji': '🇳🇱',
                'description': 'Learn Dutch and open doors to opportunities in the Netherlands and Belgium.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Swedish',
                'flag_emoji': '🇸🇪',
                'description': 'Embrace Swedish and connect with Scandinavian culture, design, and innovation.',
                'category': 1,
                'levels': [
                    {'level': 'A1', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 24000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 26000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Arabic',
                'flag_emoji': '🇸🇦',
                'description': 'Learn Modern Standard Arabic and explore the rich cultural heritage of the Arab world.',
                'category': 2,
                'levels': [
                    {'level': 'A1', 'price': 14000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 24000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'French',
                'flag_emoji': '🇫🇷',
                'description': 'Master the language of love, diplomacy, and one of the world\'s most beautiful cultures.',
                'category': 2,
                'levels': [
                    {'level': 'A1', 'price': 14000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 24000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Spanish',
                'flag_emoji': '🇪🇸',
                'description': 'Learn Spanish and connect with over 500 million speakers across the globe.',
                'category': 2,
                'levels': [
                    {'level': 'A1', 'price': 14000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 24000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'Italian',
                'flag_emoji': '🇮🇹',
                'description': 'Discover Italian, the language of art, music, cuisine, and la dolce vita.',
                'category': 2,
                'levels': [
                    {'level': 'A1', 'price': 14000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 24000, 'duration_weeks': 12},
                ]
            },
            {
                'name': 'German',
                'flag_emoji': '🇩🇪',
                'description': 'Master German and access opportunities in Europe\'s largest economy and beyond.',
                'category': 2,
                'levels': [
                    {'level': 'A1', 'price': 14000, 'duration_weeks': 12},
                    {'level': 'A2', 'price': 16000, 'duration_weeks': 12},
                    {'level': 'B1', 'price': 18000, 'duration_weeks': 12},
                    {'level': 'B2', 'price': 20000, 'duration_weeks': 12},
                    {'level': 'C1', 'price': 22000, 'duration_weeks': 12},
                    {'level': 'C2', 'price': 24000, 'duration_weeks': 12},
                ]
            },
        ]

        for lang_data in languages_data:
            language, created = Language.objects.get_or_create(
                name=lang_data['name'],
                defaults={
                    'flag_emoji': lang_data['flag_emoji'],
                    'description': lang_data['description'],
                    'category': lang_data['category'],
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created language: {language.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Language already exists: {language.name}'))
            
            # Create course levels
            for level_data in lang_data['levels']:
                level, created = CourseLevel.objects.get_or_create(
                    language=language,
                    level=level_data['level'],
                    defaults={
                        'price': level_data['price'],
                        'duration_weeks': level_data['duration_weeks'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Created level: {level.get_level_display()}'))
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated language and course data!'))

