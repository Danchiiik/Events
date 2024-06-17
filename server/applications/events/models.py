from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


REGION = (
    ('Бишкек', 'Бишкек'),
    ('Чуй', 'Чуй'),
    ('Талас', 'Талас'),
    ('Иссык-Куль', 'Иссык-Куль'),
    ('Нарын', 'Нарын'),
    ('Жалал-Абад', 'Жалал-Абад'),
    ('Ош', 'Ош'),
    ('Баткен', 'Баткен')
)

TYPE_OF_EVENT = (
    ('Открытие', 'Открытие'),
    ('Выставка', 'Выставка'),
    ('Ярмарка', 'Ярмарка'),
    ('Презентация', 'Презентация'),
    ('Праздник', 'Праздник'),
    ('Пресс-мероприятие', 'Пресс-мероприятие'),
    ('Тренинг/семинар', 'Тренинг/семинар'),
    ('Фестиваль/концерт', 'Фестиваль/концерт'),
)

TYPE = (
    ('Вход свободный', 'Вход свободный'),
    ('Вход закрытый', 'Вход закрытый')
)


class Events(models.Model):
    name = models.CharField(max_length=150)
    image = models.FileField(upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    description = models.TextField(null=True, blank=True, max_length=2500)
    region = models.CharField(max_length=50, choices=REGION)
    address = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    type_of_event = models.CharField(max_length=50, choices=TYPE_OF_EVENT)
    type = models.CharField(max_length=50, choices=TYPE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        
        
class Image(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    
    def __str__(self) -> str:
        return str(self.image.url)
        