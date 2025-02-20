from operator import concat

from authentication.models import Userr


class UserRepository:

    def get_user_by_id(self, user_id: int) -> str:
        try:
            name = Userr.objects.filter(user_id=user_id).values('first_name', 'last_name', 'middle_name')
            if name[0]['middle_name'] is None:
                return f'{name[0]['first_name']} {name[0]['last_name']}'
            else:
                return f'{name[0]['first_name']} {name[0]['middle_name']} {name[0]['last_name']}'
        except Exception as e:
            raise e