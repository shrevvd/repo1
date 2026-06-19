import datetime
from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    title = models.CharField(
        max_length=200, 
        blank=False, 
        verbose_name="Название книги"
    )
    author = models.CharField(
        max_length=150, 
        blank=False, 
        verbose_name="Автор"
    )
    publication_year = models.IntegerField(
        verbose_name="Год издания"
    )
    isbn = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="ISBN"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата и время создания"
    )

    def __str__(self):
        return self.title
    
    def clean(self):

        if not self.title or self.title.strip() == '':
            raise ValidationError({'title': 'Название книги не может быть пустым.'})
            
        if not self.author or self.author.strip() == '':
            raise ValidationError({'author': 'Автор не может быть пустым.'})
            
        current_year = datetime.datetime.now().year
        if self.publication_year is not None:
            if self.publication_year <= 0:
                raise ValidationError({'publication_year': 'Год издания должен быть целым положительным числом.'})
            if self.publication_year > current_year:
                raise ValidationError({'publication_year': f'Год издания не может быть больше текущего года ({current_year}).'})
        else:
            raise ValidationError({'publication_year': 'Пожалуйста, укажите год издания.'})

        if Book.objects.filter(isbn=self.isbn).exclude(pk=self.pk).exists(): 
            raise ValidationError({'isbn': 'Книга с таким ISBN уже существует.'})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
