from django.utils.crypto import get_random_string
from app.models import Project, Program

from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isHomePage'] = False
        return context


class ProjectPageView(TemplateView):
    template_name = "app/project.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['isHomePage'] = True
        context['loadMenu'] = True
        return context


class ProgramPageView(TemplateView):
    template_name = "app/program.html"

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None) is not None:
            try:
                program = Program.objects.filter(pk=kwargs.get('pk', None))[0]
                context = self.get_context_data(**{**kwargs, 'program': program})
                password = self.request.GET.get('pass', None)
                if context['program'].password is not None and password is not None and password == program.password:
                    if context['program'].always_running:
                        response = redirect('alwaysRunningProgram', pk=kwargs['pk'])
                    else:
                        response = redirect('program', pk=kwargs['pk'])
                    response.set_cookie('haveProgramCredentials{}'.format(kwargs['pk']), True)
                    return response
                if context['program'].always_running:
                    response = redirect('alwaysRunningProgram', pk=kwargs['pk'])
                    return response
                return self.render_to_response(context)
            except:
                return redirect('not_found')
        else:
            return redirect('not_found')

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        have_cookie_credentials = self.request.COOKIES.get('haveProgramCredentials{}'.format(kwargs['pk']), 'False')
        password = self.request.GET.get('pass', None)
        program = kwargs['program']
        context = super().get_context_data(**kwargs)
        context['loadBackMenuOption'] = True
        context['loadMenu'] = True
        context['program'] = program
        context['passwordRequired'] = ((program.password is not None and password is None
                                        or not (program.password is not None
                                                and password is not None and password == program.password)
                                        ) and have_cookie_credentials == 'False') and not (
                have_cookie_credentials == 'False' and program.password is None)
        context['isHomePage'] = context['passwordRequired']
        context['thread'] = get_random_string(length=32)
        context[
            'warningPassword'] = program.password is not None and password is not None and password != program.password
        return context


class AlwaysProgramPageView(TemplateView):
    template_name = "app/alive-program.html"

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None) is not None:
            try:
                program = Program.objects.filter(pk=kwargs.get('pk', None))[0]
                context = self.get_context_data(**{**kwargs, 'program': program})
                password = self.request.GET.get('pass', None)
                if context['program'].password is not None and password is not None and password == program.password:
                    response = redirect('program', pk=kwargs['pk'])
                    response.set_cookie('haveProgramCredentials{}'.format(kwargs['pk']), True)
                    return response
                return self.render_to_response(context)
            except:
                return redirect('not_found')
        else:
            return redirect('not_found')

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        have_cookie_credentials = self.request.COOKIES.get('haveProgramCredentials{}'.format(kwargs['pk']), 'False')
        password = self.request.GET.get('pass', None)
        program = kwargs['program']
        context = super().get_context_data(**kwargs)
        context['loadBackMenuOption'] = True
        context['loadMenu'] = True
        context['program'] = program
        context['passwordRequired'] = ((program.password is not None and password is None
                                        or not (program.password is not None
                                                and password is not None and password == program.password)
                                        ) and have_cookie_credentials == 'False') and not (
                have_cookie_credentials == 'False' and program.password is None)
        context['isHomePage'] = context['passwordRequired']
        context['thread'] = get_random_string(length=32)
        context[
            'warningPassword'] = program.password is not None and password is not None and password != program.password
        return context


class NotFoundPageView(TemplateView):
    template_name = "app/not-found.html"
