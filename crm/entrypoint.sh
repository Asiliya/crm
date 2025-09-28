#!/bin/bash
echo "Running from entrypoint.sh"

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
EOF

python manage.py runserver 0.0.0.0:8000