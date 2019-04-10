from .models import UserProfile
# code retrieved from https://stackoverflow.com/questions/29575713/retrieving-profile-picture-from-google-and-facebook-in-python-social-auth/29576422
def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = response['picture']

        # .get('url')
        ext = url.split('.')[-1]
    if url:
        #Sometimes the user doesn't have a userprofile. This works for now but there may be a larger problem
        try:
            user.userprofile.avatar = url
            user.save()
        except:
            user.save()
        # user.userprofile.avatar = "static/images/blank_profile.png"
        #     UserProfile.objects.create(user=user)
        #     user.userprofile.avatar = url
        #     user.save()
