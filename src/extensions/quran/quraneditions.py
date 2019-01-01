def parse_editions(response):
    if response['code'] != 200:
        return "Bad request. Is the language in 2-letter format?"

    data = response['data']

    return "```\n" + "\n".join(dct['identifier'] for dct in data) + "```"
