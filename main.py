import api_requests as req


def main():

    user_name = "user"
    user_password = "pass"
    response = req.make_query(username=user_name, password=user_password)
    print(response.content)


if __name__ == '__main__':
    main()

