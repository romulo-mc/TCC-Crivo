from django.apps import AppConfig
from django.db.models.signals import post_migrate

def criar_dados_iniciais(sender, **kwargs):
    from .models import Condicao, Gatilho

    condicoes_padrao = [
        # NEURODESENVOLVIMENTO
        {'nome': 'Autismo (TEA)', 'categoria': 'NEURO', 'tipo': 'INTELECTUAL'},
        {'nome': 'TDAH', 'categoria': 'NEURO', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Dislexia / Discalculia', 'categoria': 'NEURO', 'tipo': 'INTELECTUAL'},
        {'nome': 'Síndrome de Tourette', 'categoria': 'NEURO', 'tipo': 'OUTRO'},
        
        # NEUROLÓGICAS
        {'nome': 'Paralisia Cerebral', 'categoria': 'NEUROLOGICA', 'tipo': 'FISICA'},
        {'nome': 'Epilepsia', 'categoria': 'NEUROLOGICA', 'tipo': 'OUTRO'},
        {'nome': 'Esclerose Múltipla', 'categoria': 'NEUROLOGICA', 'tipo': 'FISICA'},
        {'nome': 'Esclerose Lateral Amiotrófica (ELA)', 'categoria': 'NEUROLOGICA', 'tipo': 'FISICA'},
        {'nome': 'Doença de Parkinson', 'categoria': 'NEUROLOGICA', 'tipo': 'FISICA'},
        
        # FÍSICAS / MOTORAS
        {'nome': 'Amputação / Agênesia', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        {'nome': 'Lesão Medular (Paraplegia / Tetraplegia)', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        {'nome': 'Nanismo / Acondroplasia', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        {'nome': 'Distrofia Muscular', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        {'nome': 'Osteogênese Imperfeita (Ossos de Vidro)', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        {'nome': 'Uso de Cadeira de Rodas', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        {'nome': 'Uso de Prótese / Órtese / Muletas', 'categoria': 'FISICA', 'tipo': 'FISICA'},
        
        # SENSORIAIS (AUDITIVA E VISUAL)
        {'nome': 'Surdez Profunda', 'categoria': 'AUDITIVA', 'tipo': 'SENSORIAL'},
        {'nome': 'Baixa Audição / Surdez Parcial', 'categoria': 'AUDITIVA', 'tipo': 'SENSORIAL'},
        {'nome': 'Cegueira', 'categoria': 'VISUAL', 'tipo': 'SENSORIAL'},
        {'nome': 'Baixa Visão / Visão Subnormal', 'categoria': 'VISUAL', 'tipo': 'SENSORIAL'},
        {'nome': 'Surdocegueira', 'categoria': 'VISUAL', 'tipo': 'MULTIPLA'},
        
        # GENÉTICAS / SÍNDROMES
        {'nome': 'Síndrome de Down (Trissomia 21)', 'categoria': 'GENETICA', 'tipo': 'INTELECTUAL'},
        {'nome': 'Síndrome de Williams', 'categoria': 'GENETICA', 'tipo': 'INTELECTUAL'},
        {'nome': 'Fibrose Cística', 'categoria': 'GENETICA', 'tipo': 'OUTRO'},
        
        # CRÔNICAS E INVISÍVEIS
        {'nome': 'Fibromialgia', 'categoria': 'CRONICA', 'tipo': 'FISICA'},
        {'nome': 'Doenças Autoimunes (Lúpus, etc)', 'categoria': 'CRONICA', 'tipo': 'FISICA'},
        {'nome': 'Fadiga Crônica (Encefalomielite Miálgica)', 'categoria': 'CRONICA', 'tipo': 'FISICA'},
        {'nome': 'Doença de Crohn / Retocolite', 'categoria': 'CRONICA', 'tipo': 'OUTRO'},
        {'nome': 'Endometriose Grave', 'categoria': 'CRONICA', 'tipo': 'OUTRO'},
        
        # PSICOSSOCIAIS
        {'nome': 'Depressão Maior', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Transtorno de Ansiedade Generalizada (TAG)', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Transtorno Bipolar', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Esquizofrenia / Transtornos Psicóticos', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Transtorno de Estresse Pós-Traumático (TEPT)', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Transtorno de Personalidade Borderline (TPB)', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
        {'nome': 'Transtornos Alimentares', 'categoria': 'PSICOSSOCIAL', 'tipo': 'PSICOSSOCIAL'},
    ]

    gatilhos_padrao = [
        # SAÚDE MENTAL
        {'nome': 'Suicídio / Ideação Suicida', 'categoria': 'SAUDE_MENTAL'},
        {'nome': 'Automutilação', 'categoria': 'SAUDE_MENTAL'},
        {'nome': 'Cenas de Transtorno Alimentar', 'categoria': 'SAUDE_MENTAL'},
        {'nome': 'Crise de Pânico / Ansiedade Extrema', 'categoria': 'SAUDE_MENTAL'},
        {'nome': 'Luto Profundo / Perda de Entes Queridos', 'categoria': 'SAUDE_MENTAL'},
        
        # VIOLÊNCIA E ABUSO
        {'nome': 'Violência Física / Tortura', 'categoria': 'VIOLENCIA'},
        {'nome': 'Violência Psicológica / Gaslighting', 'categoria': 'VIOLENCIA'},
        {'nome': 'Abuso Sexual / Estupro', 'categoria': 'VIOLENCIA'},
        {'nome': 'Assédio (Moral ou Sexual)', 'categoria': 'VIOLENCIA'},
        {'nome': 'Bullying Extremo / Humilhação Pública', 'categoria': 'VIOLENCIA'},
        {'nome': 'Gore / Violência Gráfica', 'categoria': 'VIOLENCIA'},
        
        # CONTEXTO MÉDICO
        {'nome': 'Trauma Médico / Negligência', 'categoria': 'MEDICO'},
        {'nome': 'Institucionalização / Internação Forçada', 'categoria': 'MEDICO'},
        {'nome': 'Cenas de Cirurgia / Sangue / Agulhas', 'categoria': 'MEDICO'},
        {'nome': 'Diagnóstico Terminal', 'categoria': 'MEDICO'},
        {'nome': 'Procedimentos Médicos Invasivos ou Sem Consentimento', 'categoria': 'MEDICO'},
        
        # EXCLUSÃO E PRECONCEITO
        {'nome': 'Capacitismo Explícito', 'categoria': 'EXCLUSAO'},
        {'nome': 'Uso de Slurs (Xingamentos Capacitistas)', 'categoria': 'EXCLUSAO'},
        {'nome': 'Eugenismo / Seleção Genética', 'categoria': 'EXCLUSAO'},
        {'nome': 'Abandono Familiar', 'categoria': 'EXCLUSAO'},
        {'nome': 'Isolamento Social Forçado', 'categoria': 'EXCLUSAO'},
        
        # OUTROS TEMAS SENSÍVEIS
        {'nome': 'Morte de Personagem PcD', 'categoria': 'OUTROS'},
        {'nome': 'Tropos Capacitistas (Ex: "Cura Mágica", "Pornografia Inspiracional")', 'categoria': 'OUTROS'},
        {'nome': 'Acidentes Graves', 'categoria': 'OUTROS'},
        {'nome': 'Uso de Drogas / Alcoolismo', 'categoria': 'OUTROS'},
        {'nome': 'Morte de Animais', 'categoria': 'OUTROS'},
    ]

    for c in condicoes_padrao:
        Condicao.objects.get_or_create(
            nome=c['nome'], 
            defaults={'categoria': c['categoria'], 'tipo': c['tipo']}
        )

    for g in gatilhos_padrao:
        Gatilho.objects.get_or_create(
            nome=g['nome'], 
            defaults={'categoria': g['categoria']}
        )

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        post_migrate.connect(criar_dados_iniciais, sender=self)