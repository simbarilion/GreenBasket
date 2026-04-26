# from rest_framework import viewsets
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     """Вьюсет привычки"""
#
#     queryset = Habit.objects.all()
#     serializer_class = HabitsSerializer
#     filter_backends = [OrderingFilter]
#     ordering_fields = ["periodicity", "habit_time"]
#     pagination_class = HabitsPaginator
#
#     def get_queryset(self):
#         """
#         Возвращает только привычки текущего пользователя.
#         Суперпользователь видит все привычки
#         """
#         user = self.request.user
#         if user.is_superuser:
#             return Habit.objects.all()
#         if user.is_authenticated:
#             return Habit.objects.filter(Q(user=user) | Q(is_public=True))
#         return Habit.objects.none()
