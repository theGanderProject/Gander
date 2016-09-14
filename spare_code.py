from django.db.models.signals import m2m_changed


def increment_or_decrement_favorite_count(sender, **kwargs):
    images = []
    if kwargs['reverse']:
        for pk in kwargs['pk_set']:
            images.append(Image.objects.get(pk=pk))
    else:
        images.append(kwargs['instance'])
    print(kwargs['action'])
    if kwargs['action'] == 'pre_add':
        for image in images:
            image.favorite_count += 1
            image.save()
    elif kwargs['action'] in ['pre_remove', 'pre_clear']:
        for image in images:
            image.favorite_count -= 1
            image.save()


m2m_changed.connect(increment_or_decrement_favorite_count, sender=Image.favorite.through)

#submit multiple files
def post(self, request, *args, **kwargs):
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    files = request.FILES.getlist('original')
    if form.is_valid(): #but it might not actually be valid! --or can i put on more constraints?
        print('files considered valid')
        for f in files:
            print('processing file ' + str(f))
            image = Image()
            image.original = f
            image.owner = self.request.user.username
            image.save()
        return self.form_valid(form)
    else:
        return self.form_invalid(form)