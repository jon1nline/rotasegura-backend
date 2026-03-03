from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Incident, Stop, Alert, TransportLine
from users.models import UserProfile, History


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populando banco de dados...')
        
        Incident.objects.all().delete()
        Stop.objects.all().delete()
        Alert.objects.all().delete()
        TransportLine.objects.all().delete()
        History.objects.all().delete()
        
        incidents = [
            {'type': 'Avaria', 'lat': -23.5505, 'lng': -46.6333, 'title': 'Trem Parado', 'description': 'Falha técnica na Linha 1-Azul'},
            {'type': 'Lotação', 'lat': -23.5489, 'lng': -46.6388, 'title': 'Superlotação', 'description': 'Estação Sé com acesso restringido'},
            {'type': 'Segurança', 'lat': -23.5550, 'lng': -46.6350, 'title': 'Assalto Relâmpago', 'description': 'Ocorrência próxima à saída A'},
            {'type': 'Avaria', 'lat': -23.5450, 'lng': -46.6310, 'title': 'Semáforo Quebrado', 'description': 'Cruzamento com Av. Paulista'},
            {'type': 'Lotação', 'lat': -23.5611, 'lng': -46.6558, 'title': 'Ônibus Cheio', 'description': 'Linha 875P-10'},
            {'type': 'Segurança', 'lat': -23.5520, 'lng': -46.6400, 'title': 'Vandalismo', 'description': 'Ponto de ônibus depredado'},
            {'type': 'Seguro', 'lat': -23.5420, 'lng': -46.6200, 'title': 'Caminho Seguro', 'description': 'Rotas bem movimentadas e claras'},
        ]
        
        for inc_data in incidents:
            Incident.objects.create(**inc_data)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(incidents)} incidentes criados'))
        
        stops = [
            {'type': 'bus', 'lat': -23.5515, 'lng': -46.6350, 'name': 'Parada Sé - Direita'},
            {'type': 'subway', 'lat': -23.5505, 'lng': -46.6333, 'name': 'Estação Sé'},
            {'type': 'bus', 'lat': -23.5600, 'lng': -46.6580, 'name': 'Parada MASP'},
            {'type': 'bus', 'lat': -23.5620, 'lng': -46.6540, 'name': 'Parada Gazeta'},
        ]
        
        for stop_data in stops:
            Stop.objects.create(**stop_data)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(stops)} paradas criadas'))
        
        alerts = [
            {
                'type': 'critical',
                'category': 'Segurança',
                'title': 'Assalto Recente - Ponto 12',
                'description': 'Relato de atividade suspeita próximo à entrada do metrô. Evite a área se possível.',
                'icon': 'shield-alert'
            },
            {
                'type': 'warning',
                'category': 'Lotação',
                'title': 'Lotação Alta - Linha 404',
                'description': 'Ônibus operando com capacidade máxima. Previsão de espera de 15 minutos.',
                'icon': 'account-group'
            }
        ]
        
        for alert_data in alerts:
            Alert.objects.create(**alert_data)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(alerts)} alertas criados'))
        
        metro_lines = [
            {'type': 'metro', 'name': 'Linha 1 - Azul', 'color': '#005599'},
            {'type': 'metro', 'name': 'Linha 2 - Verde', 'color': '#007C5F'},
            {'type': 'metro', 'name': 'Linha 3 - Vermelha', 'color': '#EF4123'},
            {'type': 'metro', 'name': 'Linha 4 - Amarela', 'color': '#FFF000'},
            {'type': 'metro', 'name': 'Linha 5 - Lilás', 'color': '#9B3894'},
            {'type': 'metro', 'name': 'Linha 15 - Prata', 'color': '#9E9E9E'},
        ]
        
        for line_data in metro_lines:
            TransportLine.objects.create(**line_data)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(metro_lines)} linhas de metrô criadas'))
        
        trem_lines = [
            {'type': 'trem', 'name': 'Linha 7 - Rubi', 'color': '#A61324'},
            {'type': 'trem', 'name': 'Linha 8 - Diamante', 'color': '#999A9E'},
            {'type': 'trem', 'name': 'Linha 9 - Esmeralda', 'color': '#00A78E'},
            {'type': 'trem', 'name': 'Linha 10 - Turquesa', 'color': '#0082A0'},
            {'type': 'trem', 'name': 'Linha 11 - Coral', 'color': '#E87D1C'},
            {'type': 'trem', 'name': 'Linha 12 - Safira', 'color': '#034888'},
            {'type': 'trem', 'name': 'Linha 13 - Jade', 'color': '#33BCAD'},
        ]
        
        for line_data in trem_lines:
            TransportLine.objects.create(**line_data)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(trem_lines)} linhas de trem criadas'))

        bus_lines = [
            {'type': 'bus', 'name': 'Linha 404 - Sé → Tatuapé', 'color': '#FF6B6B'},
            {'type': 'bus', 'name': 'Linha 875P - Pinheiros → Estação Sé', 'color': '#4ECDC4'},
            {'type': 'bus', 'name': 'Linha 5002 - Expresso Imigrantes', 'color': '#FFE66D'},
            {'type': 'bus', 'name': 'Linha 3010 - Paulista → Itim', 'color': '#95E1D3'},
            {'type': 'bus', 'name': 'Linha 702-10 - Estação Sé → Guaianazes', 'color': '#A8D8EA'},
            {'type': 'bus', 'name': 'Linha 475A - Consolação → Sacomã', 'color': '#F38181'},
            {'type': 'bus', 'name': 'Linha 60 - Vila Madalena → Centro', 'color': '#AA96DA'},
            {'type': 'bus', 'name': 'Linha 7004 - Zona Leste → Centro', 'color': '#FCBAD3'},
        ]
        
        for line_data in bus_lines:
            TransportLine.objects.create(**line_data)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(bus_lines)} linhas de ônibus criadas'))

        demo_user, created = User.objects.get_or_create(
            email='usuario@email.com',
            defaults={
                'username': 'usuario_demo',
                'first_name': 'Usuário',
            },
        )
        if created:
            demo_user.set_password('123456')
            demo_user.save()

        profile, profile_created = UserProfile.objects.get_or_create(
            user=demo_user,
            defaults={
                'phone': '(11) 98765-4321',
                'level': 12,
                'xp': 2840,
                'max_xp': 5000,
            },
        )
        if not profile_created:
            profile.phone = '(11) 98765-4321'
            profile.level = 12
            profile.xp = 2840
            profile.max_xp = 5000
            profile.save()

        history_data = [
            {
                'title': 'Lotação – Linha 404',
                'location': 'Av. Paulista, 1500',
                'status': 'Ativo',
                'icon': 'account-group',
                'color': '#2563EB',
                'likes': 12,
                'views': 45,
                'verified': False,
            },
            {
                'title': 'Atraso – Linha 875A',
                'location': 'Term. Perdizes',
                'status': 'Resolvido',
                'icon': 'bus-clock',
                'color': '#FBBF24',
                'likes': 8,
                'views': 32,
                'verified': True,
            },
        ]
        for item in history_data:
            History.objects.create(user=demo_user, **item)
        self.stdout.write(self.style.SUCCESS(f'✓ {len(history_data)} itens de histórico criados'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Banco de dados populado com sucesso!'))
