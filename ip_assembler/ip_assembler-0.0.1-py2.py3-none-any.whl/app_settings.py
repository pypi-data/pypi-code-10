from django.conf import settings


IP_ASSEMBLER_IP_CHANGED_THRESHOLD = getattr(settings, 'IP_ASSEMBLER_IP_CHANGED_THRESHOLD', 10)
IP_ASSEMBLER_IP_CHANGED_FILE = getattr(settings, 'IP_ASSEMBLER_IP_CHANGED_FILE', '/tmp/ipa.last')
