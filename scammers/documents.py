from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from .models import Scammer, ScammerProfile, ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, Tag
from elasticsearch_dsl import analyzer, tokenizer

edge_ngram_analyzer = analyzer(
    'edge_ngram_analyzer',
    tokenizer=tokenizer('edge_ngram_tokenizer', 'edge_ngram', min_gram=2, max_gram=15, token_chars=['letter', 'digit']),
    filter=['lowercase']
)

@registry.register_document
class ScammerDocument(Document):
    names = fields.NestedField(properties={
        'name': fields.TextField(
            analyzer=edge_ngram_analyzer,
            search_analyzer='standard'
        ),
    })
    phone_numbers = fields.NestedField(properties={
        'phone_number': fields.TextField(),
    })
    emails = fields.NestedField(properties={
        'email': fields.TextField(),
    })
    websites = fields.NestedField(properties={
        'website': fields.TextField(),
    })
    tags = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    class Index:
        name = 'scammers'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Scammer
        fields = [
            'description',
        ]
        related_models = [ScammerName, ScammerPhoneNumber, ScammerEmail, ScammerWebsite, Tag]

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'names', 'phone_numbers', 'emails', 'websites', 'tags'
        )

    def get_indexing_queryset(self):
        return self.get_queryset().iterator(chunk_size=1000)

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, ScammerName):
            return related_instance.scammer
        if isinstance(related_instance, ScammerPhoneNumber):
            return related_instance.scammer
        if isinstance(related_instance, ScammerEmail):
            return related_instance.scammer
        if isinstance(related_instance, ScammerWebsite):
            return related_instance.scammer
        if isinstance(related_instance, Tag):
            return related_instance.scammer_set.all()

@registry.register_document
class ScammerProfileDocument(Document):
    name = fields.TextField(
        analyzer=edge_ngram_analyzer,
        search_analyzer='standard'
    )

    class Index:
        name = 'scammer_profiles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = ScammerProfile
        fields = []