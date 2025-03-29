from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.text import slugify
import random
import string
import cyrtranslit
from django.core.exceptions import ValidationError
from django.core.cache import cache


# json validation
def json_field_validate(value):
    lang = cache.get('def_lang')

    if not lang:
        lang = Languages.objects.filter(active=True, default=True).first()
        cache.set("def_lang", lang)

    if value.get(lang.code, '') == '' or value.get(lang.code, '') is None:
        raise ValidationError(
            ("This field is required"),
            params={'value': value}
        )

# languages


class Languages(models.Model):
    name = models.CharField('Названия', max_length=255, blank=True, null=True)
    code = models.CharField('Код языка', max_length=255,
                            blank=True, null=True, unique=True)
    icon = ThumbnailerImageField(upload_to='lng_icon', blank=True, null=True)
    active = models.BooleanField(default=False)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'lang'

    def save(self, *args, **kwargs) -> None:
        if self.default:
            cache.set("def_lang", self)

            # make langs not default
            langs = Languages.objects.all()

            if self.pk:
                langs = langs.exclude(id=self.pk)

            for lng in langs:
                lng.default = False
                lng.save()

        cache.set('langs', Languages.objects.filter(
            active=True).order_by('-default'))

        return super().save(*args, **kwargs)


# random string generate
def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# unique string generate
def unique_slug_generator(instance, slug, id=None, extra_class=None, i=1):
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug)

    if id:
        qs_exists = qs_exists.exclude(id=id)
    qs_exists = qs_exists.exists()
    if qs_exists or (extra_class and extra_class.objects.filter(slug=slug)):
        slug_lst = slug.split('-')

        if str(i-1) == slug_lst[-1]:
            slug = '-'.join(slug_lst[:-1])

        new_slug = "{slug}-{int}".format(slug=slug, int=i)
        next = i + 1
        return unique_slug_generator(instance, new_slug,
                                     id=id,
                                     extra_class=extra_class,
                                     i=next)

    return slug


# === BASE SLUG FIELD MODEL | START | ===
class BaseModel(models.Model):
    """ Abstract model class for models with slug field """
    slug_fields: list = []

    slug = models.SlugField('Slug', editable=False, unique=True)

    class Meta:
        abstract = True

    def update_slug(self, instace):
        updated = False

        if not instace:
            return True

        for field in self.slug_fields:
            if instace.__dict__.get(field) != self.__dict__.get(field):
                updated = True

        return updated

    def save(self, *args, **kwargs):  # new
        lng = cache.get('def_lang')

        try:
            instace = self.__class__.objects.get(id=self.pk)
        except Exception:
            instace = None

        update_slug = self.update_slug(instace)

        if update_slug:
            if not lng:
                lng = Languages.objects.filter(
                    active=True, default=True).first()
                cache.set("def_lang", lng)

            data_dict = self.__dict__
            slug_string = ''
            slug_fields = self.slug_fields

            for field in slug_fields:
                value = data_dict.get(field, '')

                if value is None:
                    value = ''

                if isinstance(value, dict):
                    value = value.get(lng.code, '')

                slug_string += value

                if (len(slug_fields) > 1 and
                        slug_fields.index(field) != len(slug_fields)):
                    slug_string += '_'

            str = cyrtranslit.to_latin(slug_string[:40])
            slug = slugify(str)

            if not self.slug:
                self.slug = unique_slug_generator(self, slug)
            else:
                self.slug = unique_slug_generator(self, slug, id=self.pk)

        elif instace:
            self.slug = instace.slug

        return super().save(*args, **kwargs)

# === BASE SLUG FIELD MODEL | END | ===