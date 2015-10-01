from django.apps import AppConfig

class PodcastConfig(AppConfig):
    name = 'podcast'
    verbose_name = "Podcasts App"

    def ready(self):
        import podcast.signals.handlers #noqa
