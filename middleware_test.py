class PhoneOrDesktopTemplate:
    def __init__(self, get_responce):
        self.get_reponce = get_responce

    def __call__(self, request):
        responce = self.get_reponce(request)
        if request.user_agent.is_mobile:
            prefix ='mobile/'
        else:
            prefix ='full/'
        responce.template_name = prefix + responce.template_name
        return responce
