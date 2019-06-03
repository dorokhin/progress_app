# progress_app

```bash
python manage.py shell
```

```python
import datetime
from progress.models import PassEntry


lastweek = datetime.datetime.now() - datetime.timedelta(days=7)
t = PassEntry(type_id=1, user_id=1)
t.save()
PassEntry.objects.filter(pk=t.id).update(date=lastweek)

```


### Used libraries:
+ [Calendar heatmap](https://cal-heatmap.com/)
