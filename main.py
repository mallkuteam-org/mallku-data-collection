import api_requests as req


def main():
    # json_result = req.request_breeds_by_name("pers", True)
    req.post_my_vote(image_id="8rm", sub_id="api-facu", value=3)
    json_votes = req.request_my_votes(sub_id="api-facu")
    print(json_votes)


if __name__ == '__main__':
    main()

