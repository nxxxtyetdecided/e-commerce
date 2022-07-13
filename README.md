# drf_task

#### user 앱 관련
> ✔ UserManager 테이블
- User를 custom 하기 위해 생성
- is_staff 추가 (판매자 구별)

> ✔ User 테이블
- PermissionMixin 상속
- is_active를 통한 활성화 판별
- jwt를 통한 인증 (`simple-jwt`)

#### product 앱 관련

> ✔ Category 테이블
- 관리자만 생성할 수 있도록 `IsAdminOrReadOnly`
- delete()시 `is_active=False`

> ✔ Product 테이블
- 판매자만 생성할 수 있도록 `IsStaffOrReadOnly`
- 쿼리 파라미터를 통한 검색, ProductListCreateAPI에 상속
  ```python
    class ProductSearchHandler:
        def get_query_params(self, request):
            q = Q(is_active=True)

            data = request.query_params.get
            title = data('title', None)
            if title:
                q &= Q(title__icontains=title)

            return q
    ```

> ✔ Order 테이블

> ✔ Review 테이블

#### utils 관련
> permissions.py

> timestamp.py


### 추가 예정
- Review 오류 수정
- Product exposure_date -> validator
- TestCode
- pep8, isort
- docker, docker-compose, nginx
- CICD(Git Action)