from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to='lms', verbose_name='изображение', **NULLABLE)
    content = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    content = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='lesson', verbose_name='изображение', **NULLABLE)
    url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
