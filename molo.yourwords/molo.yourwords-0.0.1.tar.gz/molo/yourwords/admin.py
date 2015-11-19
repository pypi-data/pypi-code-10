import json

from molo.core.models import ArticlePage, LanguagePage
from molo.yourwords.models import YourWordsCompetitionEntry
from django.contrib import admin


def convert_to_article(model_admin, request, entry):
    english = LanguagePage.objects.get(code='en')
    article = ArticlePage(
        title=entry.story_name,
        body=json.dumps([{"type": "paragraph", "value": entry.story_text}]))
    english.add_child(instance=article)
    article.save_revision()


convert_to_article.short_description = "Convert competition entry to article"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['title']
    actions = [convert_to_article]

admin.site.register(YourWordsCompetitionEntry)
# admin.site.register(ArticleAdmin)
