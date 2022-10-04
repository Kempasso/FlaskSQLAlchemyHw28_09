def put_and_delete(obj, request, db):
    if request.method == 'PUT':
        args = list(request.args.items())
        for i in args:
            setattr(obj, i[0], i[1])
        db.session.commit()
        return 'Запись обновлена'
    elif request.method == 'DELETE':

        db.session.delete(obj)
        db.session.commit()
        return 'Запись удалена'


def post(cls, db, request):
    args = list(request.args.items())
    try:
        with db.session.begin():
            item = cls()
            for i in args:
                setattr(item, i[0], i[1])
            db.session.add(item)
            db.session.commit()
    except Exception as e:
        return 'Такой ID уже существует'
    else:
        return 'Запись добавлена'


def get(db, obj):
    result = []
    with db.session.begin():
        all_users = obj.query.all()
        for i in all_users:
            result.append({
                'id': i.id,
                'first_name': i.first_name,
                'last_name': i.last_name,
                'age': i.age,
                'email': i.email,
                'role': i.role,
                'phone': i.phone
            })
