import jwt

from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views.generic import View
from django.http import JsonResponse

from accounts.models import TimtecUser
from timtec import settings
from django.contrib.auth.models import Group


class IntegrationController(View):

    def post(self, request, *args, **kwargs):

        token = request.POST['token']
        payload = jwt.decode(token, settings.INTEGRATION_JWT_SECRET, algorithms=['HS256'])

        if not payload['sub']:
            return JsonResponse({'status': 'invalid_jwt', 'missing': 'sub'})
        if not payload['uid']:
            return JsonResponse({'status': 'invalid_jwt', 'missing': 'uid'})
        if not payload['name']:
            return JsonResponse({'status': 'invalid_jwt', 'missing': 'name'})
        if not payload['email']:
            return JsonResponse({'status': 'invalid_jwt', 'missing': 'email'})

        external_user_id = int(payload['uid'])

        try:

            user = TimtecUser.objects.get(id=external_user_id)

        except TimtecUser.DoesNotExist:
            user = TimtecUser.objects.create(
                id=external_user_id,
                username=('ead_' + str(external_user_id)),
                first_name=payload['name'],
                # Generate '+' alias email to avoid uniqueness clashing on future editions
                email='ead_' + str(external_user_id) + '+' + payload['email']
            )
            user.groups.add(Group.objects.get(name="students"))

        if not user:
            return JsonResponse({'error': 'connect_failed'})

        logout_user_id = False
        if request.user.is_authenticated:
            logout_user_id = request.user.id
            logout(request)

        user.backend = 'django.contrib.auth.backends.ModelBackend'

        login(request, user)
        response = redirect('home_view')

        if logout_user_id:
            response.delete_cookie('banner_showed_' + str(logout_user_id))

        return response
