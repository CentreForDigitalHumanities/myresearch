"""
URL configuration for myresearch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path(
        "backend/",
        include(
            [
                path("admin/", admin.site.urls),
                path("api/", include("api.urls")),
                # Used for a healthcheck by the Docker container.
                path("healthcheck/", lambda r: HttpResponse()),
            ],
        ),
    )
]

# If SAML is enabled, add the required URL patterns for SAML
if hasattr(settings, "SAML_CONFIG"):
    from djangosaml2.views import LoginView
    from cdh.federated_auth.saml.views import LogoutInitView

    urlpatterns.extend(
        [
            path("saml/login/", LoginView.as_view(), name="saml-login"),
            # We can only have one logout view. Luckily, the SAML logout view can
            # handle local accounts as well.
            path("saml/logout/", LogoutInitView.as_view(), name="logout"),
            path("saml/", include("djangosaml2.urls")),
        ]
    )
