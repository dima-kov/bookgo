from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect

from club.models import Club


class ClubSubDomainsMiddleware:
    local_hosts = ['127.0.0.1', 'localhost']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.club = None

        host = self.get_host(request)
        host_splited = host.split('.')
        if len(host_splited) > 2 and not self.is_localhost(host):
            sub_domain_name = ''.join(host_splited[:-2])
            club = self.load_club(sub_domain_name)
            if club is None:
                return redirect(self.get_global_site(request))

            request.club = club

        return self.get_response(request)

    def load_club(self, name):
        try:
            return Club.objects.get(slug=name)
        except Club.DoesNotExist:
            return None

    def get_global_site(self, request):
        site = get_current_site(request)
        return 'http://{}:{}'.format(site.domain, self.get_port(request))

    def get_port(self, request):
        return request.META.get('SERVER_PORT', 80)

    def is_localhost(self, hostname):
        return hostname in self.local_hosts

    def get_host(self, request):
        host = request.META.get('HTTP_HOST', '').replace('www.', '')
        host_and_port = host.split(':')
        return host_and_port[0] if len(host_and_port) > 1 else host
