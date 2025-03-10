from dash.dependencies import Input, Output


def set_save_token_callback(app):
    app.clientside_callback(
    """
    function(url) {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        if (token) {
            // Сохраняем токен в localStorage
            localStorage.setItem('user_token', token);
            return token;  // Отображаем токен на фронте (например, в LEDDisplay)
        }
        return localStorage.getItem('user_token');  // Если токен уже сохранен в localStorage
    }
    """,
    Input('url', 'search')
    )

# Клиентский колбек для извлечения токена из localStorage
def set_get_token_callback(app):
    app.clientside_callback(
        """
        function() {
            // Извлекаем токен из localStorage
            const token = localStorage.getItem('user_token');
            return token || null;  // Возвращаем токен или null, если его нет
        }
        """,
        Output('stored-token', 'data'),  # Сохраняем токен в dcc.Store
        Input('url', 'pathname')  # Триггер — любой переход на страницу
    )

# @app.callback(
#     Output('user-message', 'children'),
#     Input('url', 'search')
# )
# def update_message(search):
#     print(search)
#     token = None
#     # Если query string содержит параметр 'token', сохраняем его
#     if search:
#         params = dict(x.split('=') for x in search[1:].split('&'))
#         token = params.get('token', None)
#     if token:
#         return f"Token received: {token}"
#     else:
#         # Попытаться получить токен из localStorage через JavaScript
#         return "No token found."